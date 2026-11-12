
import asyncio
import json
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Never

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agent_framework import (
    Agent,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    executor,
    handler,
    response_handler,
)

from agent_framework.openai import OpenAIChatClient


# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


def read_setting(name: str) -> str:

    value = os.getenv(name, "").strip()

    if (
        not value
        or value.startswith("PASTE_")
        or value.startswith("YOUR_")
    ):
        raise ValueError(
            f"Set {name} correctly in your .env file"
        )

    return value


# =====================================================
# 2. HUMAN-IN-THE-LOOP APPROVAL REQUEST
# =====================================================

@dataclass
class ManagerApprovalRequest:

    return_request: dict
    prompt: str


# =====================================================
# 3. APPROVAL GATEWAY
# =====================================================

class ApprovalGateway(Executor):

    def __init__(self):

        super().__init__(id="approval_gateway")

    # -------------------------------------------------
    # APPROVAL GATEWAY HANDLER
    # -------------------------------------------------

    @handler
    async def review(
        self,
        return_request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print("\n[Approval Gateway] Checking approval conditions...")

        eligibility_passed = (
            return_request.get("eligibility_passed") is True
        )

        risk_level = return_request.get(
            "risk_level",
            "UNKNOWN"
        )

        # -------------------------------------------------
        # AUTOMATIC APPROVAL
        # -------------------------------------------------

        if eligibility_passed and risk_level == "LOW":

            return_request["approval_route"] = "Automatic"

            return_request["final_decision"] = "AUTO_APPROVED"

            return_request["decision_by"] = (
                "Automatic Business Rules"
            )

            print(
                "\n[Approval Gateway] "
                "All conditions satisfied."
            )

            print("[Approval Gateway] AUTO_APPROVED")

            await ctx.send_message(return_request)

            return

        # -------------------------------------------------
        # HUMAN-IN-THE-LOOP APPROVAL
        # -------------------------------------------------

        return_request["approval_route"] = "Human Review"

        print(
            "\n[Approval Gateway] "
            "PAUSED - Manager approval required."
        )

        # Prepare information for the manager

        issues = return_request.get(
            "eligibility_issues",
            []
        )

        risk_assessment = return_request.get(
            "risk_result",
            "No risk assessment available"
        )

        prompt = (
            f"Request ID: {return_request.get('request_id', 'N/A')}\n"
            f"Order ID: {return_request.get('order_id', 'N/A')}\n"
            f"Product: {return_request.get('product', 'N/A')}\n"
            f"Amount: INR {return_request.get('amount_inr', 'N/A')}\n"
            f"Eligibility Issues: {', '.join(issues) if issues else 'None'}\n"
            f"Risk Assessment: {risk_assessment}\n"
        )

        # Pause workflow and request manager input

        await ctx.request_info(
            request_data=ManagerApprovalRequest(
                return_request=return_request,
                prompt=prompt,
            ),
            response_type=str,
        )

    # -------------------------------------------------
    # MANAGER RESPONSE HANDLER
    # -------------------------------------------------

    @response_handler
    async def on_manager_decision(
        self,
        original_request: ManagerApprovalRequest,
        response: str,
        ctx: WorkflowContext[dict],
    ) -> None:

        print("\n[Approval Gateway] Processing manager decision...")

        # Preserve the original request information

        return_request = dict(
            original_request.return_request
        )

        decision = response.strip().lower()

        # Validate manager response

        if decision not in {"approve", "reject"}:

            raise ValueError(
                "Invalid manager decision. "
                "Enter approve or reject."
            )

        # Assign final decision

        if decision == "approve":

            return_request["final_decision"] = (
                "MANAGER_APPROVED"
            )

        else:

            return_request["final_decision"] = (
                "MANAGER_REJECTED"
            )

        return_request["approval_route"] = "Human Review"

        return_request["decision_by"] = "Human Manager"

        return_request["manager_decision"] = decision.upper()

        print(
            f"\n[Approval Gateway] "
            f"Manager Decision: {decision.upper()}"
        )

        print(
            f"[Approval Gateway] "
            f"Final Decision: {return_request['final_decision']}"
        )

        # Resume the paused workflow

        await ctx.send_message(return_request)


# =====================================================
# 4. CREATE AGENTS AND WORKFLOW
# =====================================================

def build_workflow(chat_client: OpenAIChatClient):

    # -------------------------------------------------
    # AGENT 1: ELIGIBILITY AGENT
    # -------------------------------------------------

    eligibility_agent = Agent(
        client=chat_client,
        name="EligibilityAgent",
        instructions=(

            "You are an E-commerce Return Eligibility Agent. "

            "Review customer return requests against the "
            "company's automatic approval policy. "

            "Evaluate these five conditions: "

            "1. Product amount must be below INR 25,000. "

            "2. Return request must be within 30 days "
            "of delivery. "

            "3. Customer invoice must be available. "

            "4. Item must be unopened OR damaged with "
            "supporting photographs. "

            "5. Customer must have fewer than three "
            "previous returns in 90 days. "

            "Explain which conditions pass and fail. "

            "Identify missing information and policy violations. "

            "Do not make the final approval decision. "

            "Use only the information supplied in the request."
        ),
    )

    # -------------------------------------------------
    # AGENT 2: RISK AGENT
    # -------------------------------------------------

    risk_agent = Agent(
        client=chat_client,
        name="RiskAgent",
        instructions=(

            "You are an E-commerce Return Risk Assessment Agent. "

            "Analyze customer return requests for potential risks. "

            "Consider unusual return frequency, missing evidence, "
            "high-value requests, and suspicious return patterns. "

            "Return HIGH if significant risk indicators "
            "are identified. "

            "Return LOW if no significant risk indicators "
            "are identified. "

            "Do not assume fraud without sufficient evidence. "

            "Your response must start with exactly one word: "
            "HIGH or LOW. "

            "Provide a short explanation after the first line. "

            "Use only the information supplied in the request."
        ),
    )

    # -------------------------------------------------
    # AGENT 3: CUSTOMER RESPONSE AGENT
    # -------------------------------------------------

    customer_response_agent = Agent(
        client=chat_client,
        name="CustomerResponseAgent",
        instructions=(

            "You are an E-commerce Customer Support Agent. "

            "Generate a professional and polite customer-facing "
            "message using the final workflow decision. "

            "The final decision has already been determined "
            "by the workflow. You must never change or override it. "

            "If AUTO_APPROVED, inform the customer that the "
            "return request has been automatically approved. "

            "If MANAGER_APPROVED, inform the customer that the "
            "manager has approved the return request. "

            "If MANAGER_REJECTED, politely inform the customer "
            "that the return request has been rejected. "

            "If the request is approved, explain the next steps "
            "for the return or replacement where appropriate. "

            "Do not claim that a refund has been processed "
            "or a replacement has already been shipped. "

            "Do not expose internal risk assessments or "
            "suspicious activity details. "

            "Use the supplied customer and order information only. "

            "Keep the response concise and professional."
        ),
    )

    # =================================================
    # 5. DEFINE WORKFLOW EXECUTORS
    # =================================================

    # -------------------------------------------------
    # EXECUTOR 1: ELIGIBILITY
    # -------------------------------------------------

    @executor(id="eligibility")
    async def eligibility(
        return_request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print("\n[Eligibility Agent] Analyzing return request...")

        # AI-based policy assessment

        result = await eligibility_agent.run(
            "Review this customer return request against "
            "the automatic return approval policy. "

            "Evaluate all five eligibility conditions. "
            "Explain which conditions pass, fail, or have "
            "missing information. "

            "Do not make the final approval decision.\n\n"

            "Customer Return Request:\n"
            + json.dumps(
                return_request,
                ensure_ascii=False,
            )
        )

        eligibility_result = result.text.strip()

        print(
            f"\n[Eligibility Agent] Assessment:\n"
            f"{eligibility_result}"
        )

        # -------------------------------------------------
        # DETERMINISTIC PYTHON BUSINESS RULES
        # -------------------------------------------------

        checks = {}

        # 1. Product amount must be below ₹25,000

        amount = return_request.get("amount_inr")

        checks["amount"] = (
            isinstance(amount, (int, float))
            and not isinstance(amount, bool)
            and amount >= 0
            and amount < 25000
        )

        # 2. Return must be within 30 days

        days = return_request.get(
            "days_since_delivery"
        )

        checks["return_window"] = (
            isinstance(days, int)
            and not isinstance(days, bool)
            and 0 <= days <= 30
        )

        # 3. Invoice must be available

        checks["invoice"] = (
            return_request.get("invoice_available") is True
        )

        # 4. Item must be unopened OR damaged with photos

        condition = str(
            return_request.get("item_condition", "")
        ).strip().upper()

        photos_available = return_request.get(
            "photo_evidence_available"
        )

        checks["item_condition"] = (
            condition == "UNOPENED"
            or (
                condition == "DAMAGED"
                and photos_available is True
            )
        )

        # 5. Fewer than three previous returns in 90 days

        previous_returns = return_request.get(
            "previous_returns_90_days"
        )

        checks["return_history"] = (
            isinstance(previous_returns, int)
            and not isinstance(previous_returns, bool)
            and 0 <= previous_returns < 3
        )

        # -------------------------------------------------
        # IDENTIFY ELIGIBILITY ISSUES
        # -------------------------------------------------

        condition_descriptions = {
            "amount": "Product amount must be below INR 25,000.",
            "return_window": "Return request must be within 30 days of delivery.",
            "invoice": "Customer invoice is missing or unavailable.",
            "item_condition": "Item must be unopened or damaged with supporting photographs.",
            "return_history": "Customer must have fewer than three previous returns in 90 days.",
        }

        eligibility_issues = [
            condition_descriptions[key]
            for key, passed in checks.items()
            if not passed
        ]

        eligibility_passed = all(checks.values())

        # -------------------------------------------------
        # DISPLAY BUSINESS RULE RESULTS
        # -------------------------------------------------

        print("\n[Eligibility Agent] Python Validation:")

        for key, passed in checks.items():

            status = "PASS" if passed else "FAIL"

            print(f"{key}: {status}")

        print(
            f"\nEligibility Passed: {eligibility_passed}"
        )

        if eligibility_issues:

            print("\nEligibility Issues:")

            for issue in eligibility_issues:
                print(f"- {issue}")

        # -------------------------------------------------
        # FORWARD INFORMATION TO RISK AGENT
        # -------------------------------------------------

        await ctx.send_message({
            **return_request,

            "eligibility_result": eligibility_result,

            "eligibility_checks": checks,

            "eligibility_issues": eligibility_issues,

            "eligibility_passed": eligibility_passed,
        })

    # -------------------------------------------------
    # EXECUTOR 2: RISK
    # -------------------------------------------------

    @executor(id="risk")
    async def risk(
        return_request: dict,
        ctx: WorkflowContext[dict],
    ) -> None:

        print("\n[Risk Agent] Analyzing return risks...")

        result = await risk_agent.run(
            "Analyze this e-commerce return request for risks. "

            "Consider product amount, return history, "
            "item condition, return reason, and available evidence. "

            "Identify unusual return frequency, missing evidence, "
            "high-value requests, and suspicious patterns. "

            "Your FIRST line must contain exactly HIGH or LOW. "

            "Follow it with a short explanation.\n\n"

            "Customer Return Request:\n"
            + json.dumps(
                return_request,
                ensure_ascii=False,
            )
        )

        risk_result = result.text.strip()

        print(
            f"\n[Risk Agent] Assessment:\n{risk_result}"
        )

        # Extract risk classification

        first_line = (
            risk_result.splitlines()[0]
            .strip()
            .upper()
            .strip("*` .:")
            if risk_result
            else ""
        )

        # Invalid response defaults to HIGH for safety

        if first_line not in {"HIGH", "LOW"}:

            risk_level = "HIGH"

            risk_result = (
                "HIGH\n"
                "Risk classification could not be validated. "
                "Manual review is required.\n"
                + risk_result
            )

        else:

            risk_level = first_line

        print(
            f"\n[Risk Agent] Risk Level: {risk_level}"
        )

        # Forward request and risk assessment

        await ctx.send_message({
            **return_request,

            "risk_result": risk_result,

            "risk_level": risk_level,
        })

    # -------------------------------------------------
    # EXECUTOR 3: CUSTOMER RESPONSE
    # -------------------------------------------------

    @executor(id="response")
    async def response(
        return_request: dict,
        ctx: WorkflowContext[Never, str],
    ) -> None:

        print(
            "\n[Customer Response Agent] "
            "Generating customer communication..."
        )

        final_decision = return_request.get(
            "final_decision"
        )

        # Validate final decision

        allowed_decisions = {
            "AUTO_APPROVED",
            "MANAGER_APPROVED",
            "MANAGER_REJECTED",
        }

        if final_decision not in allowed_decisions:

            raise ValueError(
                f"Invalid final decision: {final_decision}"
            )

        # Generate customer communication

        result = await customer_response_agent.run(
            "Generate a customer-facing message for this "
            "return request. "

            "Respect the exact final decision supplied. "
            "Do not change it. "

            "Use the product name, order ID, and request type. "

            "Do not claim that any refund or replacement "
            "has already been completed.\n\n"

            "Final Return Information:\n"
            + json.dumps(
                return_request,
                ensure_ascii=False,
            )
        )

        customer_message = result.text.strip()

        # -------------------------------------------------
        # CREATE STRUCTURED FINAL OUTPUT
        # -------------------------------------------------

        final_record = {

            "request_id": return_request.get(
                "request_id"
            ),

            "order_id": return_request.get(
                "order_id"
            ),

            "product": return_request.get(
                "product"
            ),

            "requested_amount_inr": return_request.get(
                "amount_inr"
            ),

            "eligibility_findings": {

                "agent_assessment": return_request.get(
                    "eligibility_result"
                ),

                "business_rule_checks": return_request.get(
                    "eligibility_checks"
                ),

                "issues": return_request.get(
                    "eligibility_issues"
                ),
            },

            "risk_assessment": {

                "risk_level": return_request.get(
                    "risk_level"
                ),

                "explanation": return_request.get(
                    "risk_result"
                ),
            },

            "approval_route": return_request.get(
                "approval_route"
            ),

            "final_decision": final_decision,

            "decision_by": return_request.get(
                "decision_by"
            ),

            "customer_communication_draft": customer_message,
        }

        print(
            "\n[Customer Response Agent] "
            "Final structured record generated."
        )

        # Yield final workflow output

        await ctx.yield_output(
            json.dumps(
                final_record,
                indent=4,
                ensure_ascii=False,
            )
        )

    # =================================================
    # 6. CREATE GRAPH WORKFLOW
    # =================================================

    gateway = ApprovalGateway()

    workflow = (

        WorkflowBuilder(
            start_executor=eligibility
        )

        .add_edge(
            eligibility,
            risk,
        )

        .add_edge(
            risk,
            gateway,
        )

        .add_edge(
            gateway,
            response,
        )

        .build()
    )

    return workflow


# =====================================================
# 7. EXECUTE WORKFLOW WITH HUMAN APPROVAL
# =====================================================

async def run_one(
    workflow,
    return_request: dict,
) -> None:

    responses = None

    first_run = True

    while True:

        # -------------------------------------------------
        # INITIAL EXECUTION OR WORKFLOW RESUMPTION
        # -------------------------------------------------

        if first_run:

            stream = workflow.run(
                return_request,
                stream=True,
            )

            first_run = False

        else:

            stream = workflow.run(
                stream=True,
                responses=responses,
            )

        pending = {}

        completed = False

        # -------------------------------------------------
        # COLLECT WORKFLOW EVENTS
        # -------------------------------------------------

        async for event in stream:

            if event.type == "request_info":

                pending[event.request_id] = event.data

            elif event.type == "output":

                print("\n" + "=" * 60)

                print("FINAL RETURN PROCESSING RESULT")

                print("=" * 60)

                print(event.data)

                print("=" * 60)

                completed = True

        # Workflow completed

        if completed:
            return

        # Check whether workflow is waiting for approval

        if not pending:

            raise RuntimeError(
                "Workflow stopped without final output "
                "or manager approval request."
            )

        # -------------------------------------------------
        # COLLECT MANAGER RESPONSES
        # -------------------------------------------------

        responses = {}

        for request_id, request in pending.items():

            print("\n" + "=" * 60)

            print("HUMAN-IN-THE-LOOP: MANAGER APPROVAL REQUIRED")

            print("=" * 60)

            # Display request information

            print(request.prompt)

            print(
                "\nEligibility Findings:"
            )

            for issue in request.return_request.get(
                "eligibility_issues",
                [],
            ):

                print(f"- {issue}")

            if not request.return_request.get(
                "eligibility_issues"
            ):

                print("No eligibility issues.")

            print(
                "\nRisk Assessment:"
            )

            print(
                request.return_request.get(
                    "risk_result",
                    "Not available",
                )
            )

            print("\nManager Decision:")

            # Validate manager input

            while True:

                answer = input(
                    "Enter approve or reject: "
                ).strip().lower()

                if answer in {"approve", "reject"}:

                    break

                print(
                    "Invalid response. "
                    "Please enter approve or reject."
                )

            # Store manager response using request ID

            responses[request_id] = answer

        # Loop continues and resumes the paused workflow


# =====================================================
# 8. MAIN APPLICATION
# =====================================================

async def main() -> None:

    print("=" * 60)

    print("MICROSOFT AGENT FRAMEWORK")

    print("E-COMMERCE RETURNS & REFUND PROCESSING SYSTEM")

    print("Authentication: Azure Foundry API Key")

    print("=" * 60)

    # -------------------------------------------------
    # LOAD AZURE FOUNDRY CREDENTIALS
    # -------------------------------------------------

    api_key = read_setting(
        "AZURE_OPENAI_API_KEY"
    )

    base_url = read_setting(
        "AZURE_OPENAI_BASE_URL"
    )

    model = read_setting(
        "AZURE_OPENAI_MODEL"
    )

    print("\nAzure Foundry configuration loaded.")

    print(f"Endpoint: {base_url}")

    print(f"Deployment: {model}")

    # -------------------------------------------------
    # LOAD CUSTOMER RETURN DATA
    # -------------------------------------------------

    returns_file = BASE_DIR / "returns.json"

    with returns_file.open(
        encoding="utf-8"
    ) as file:

        returns = json.load(file)

    # Allow either one JSON object or a list of requests

    if isinstance(returns, dict):

        returns = [returns]

    if not isinstance(returns, list):

        raise ValueError(
            "returns.json must contain a JSON object "
            "or a list of return requests."
        )

    if not returns:

        print("\nNo return requests found.")

        return

    # Validate request IDs

    request_ids = [
        request.get("request_id")
        for request in returns
        if isinstance(request, dict)
    ]

    if (
        len(request_ids) != len(returns)
        or any(
            not isinstance(request_id, str)
            or not request_id.strip()
            for request_id in request_ids
        )
        or len(request_ids) != len(set(request_ids))
    ):

        raise ValueError(
            "Every return request must have a unique, "
            "non-empty request_id."
        )

    print(
        f"\nTotal return requests loaded: {len(returns)}"
    )

    # -------------------------------------------------
    # CONNECT TO AZURE FOUNDRY
    # -------------------------------------------------

    async with AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    ) as sdk_client:

        chat_client = OpenAIChatClient(
            model=model,
            async_client=sdk_client,
        )

        print(
            "\nAzure Foundry client initialized."
        )

        # -------------------------------------------------
        # PROCESS RETURN REQUESTS
        # -------------------------------------------------

        for return_request in returns:

            print("\n" + "=" * 60)

            print(
                f"Processing Return Request: "
                f"{return_request.get('request_id')}"
            )

            print(
                f"Order ID: "
                f"{return_request.get('order_id', 'N/A')}"
            )

            print(
                f"Product: "
                f"{return_request.get('product', 'N/A')}"
            )

            print(
                f"Amount: INR "
                f"{return_request.get('amount_inr', 'N/A')}"
            )

            print("=" * 60)

            # Build a fresh workflow for every request

            workflow = build_workflow(
                chat_client
            )

            # Run workflow with Human-in-the-Loop support

            await run_one(
                workflow,
                return_request,
            )

        print("\n" + "=" * 60)

        print("ALL RETURN REQUESTS PROCESSED")

        print("=" * 60)


# =====================================================
# 9. APPLICATION ENTRY POINT
# =====================================================

if __name__ == "__main__":

    asyncio.run(main())
