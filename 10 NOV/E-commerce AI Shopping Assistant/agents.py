
import os
from dotenv import load_dotenv

from agent_framework import Agent
from agent_framework.openai import OpenAIChatCompletionClient

from tools import search_products, calculate_order_total

load_dotenv()


def create_agents():

    # Shared OpenRouter client using Chat Completions API
    client = OpenAIChatCompletionClient(
        model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    # Agent 1: Inventory Agent
    inventory_agent = Agent(
        client=client,
        name="InventoryAgent",
        instructions=(
            "You are an inventory specialist. "
            "Use search_products to find matching products. "
            "Return product ID, name, price, rating and stock. "
            "Only use verified product information."
        ),
        tools=[search_products]
    )

    # Agent 2: Pricing Agent
    pricing_agent = Agent(
        client=client,
        name="PricingAgent",
        instructions=(
            "You are a pricing specialist. "
            "Review the inventory results. "
            "Use calculate_order_total for matching products. "
            "Validate requested quantities against stock. "
            "Compare verified totals against the customer's budget. "
            "Never invent prices or totals."
        ),
        tools=[calculate_order_total]
    )

    # Agent 3: Recommendation Agent
    recommendation_agent = Agent(
        client=client,
        name="RecommendationAgent",
        instructions=(
            "You are a product recommendation specialist. "
            "Recommend the highest-rated product that meets "
            "the customer's budget and quantity requirements. "
            "Only recommend products with sufficient stock. "
            "If ratings are equal, choose the lower-cost product. "
            "If no product meets the requirements, clearly say so. "
            "Use only verified inventory and pricing results."
        )
    )

    return inventory_agent, pricing_agent, recommendation_agent
