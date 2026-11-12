C:\Users\Trainer\PycharmProjects\PythonProject3\.venv\Scripts\python.exe C:\Users\Trainer\PycharmProjects\PythonProject3\graph_workflow.py 
============================================================
MICROSOFT AGENT FRAMEWORK
IT INCIDENT ROUTING SYSTEM
Authentication: Azure Foundry API Key
============================================================

Azure Foundry configuration loaded.
Endpoint: https://jahnavifoundry.openai.azure.com/openai/v1
Deployment: gpt-4o

Total incidents loaded: 4

Azure Foundry client initialized.
Graph workflow built successfully.

============================================================
Processing Incident: INC101
Description: The corporate email service is unavailable for every employee across the company.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: HIGH

[Escalation Agent] Handling HIGH-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC101
Severity: HIGH
Assigned Agent: EscalationAgent

### Incident Escalation Plan: INC101

1. **Incident Summary**  
   The corporate email service is fully unavailable, impacting all employees and disrupting business communication across the company.

2. **Responsible Support Team**  
   Messaging & Collaboration Team (Email Services Team)

3. **Immediate Containment Actions**  
   - Verify if the issue is caused by server outages or network disruptions.  
   - Restart affected email servers or services if applicable.  
   - Check for potential DNS issues, authentication errors, or external dependencies (e.g., cloud service providers).

4. **Escalation Procedure**  
   - Escalate immediately to the Email Services Team manager if resolution is unclear within 15 minutes.  
   - Engage third-party vendors (e.g., Microsoft, Google, AWS) if the service relies on external providers, following critical incident support agreements.  
   - Notify IT leadership for resource allocation if the issue appears prolonged.  

5. **Communication Recommendations**  
   - Send internal alerts via alternate channels (e.g., SMS, collaboration platforms like Teams/Slack) to notify employees of the outage.  
   - Provide status updates every 30 minutes to leadership and employees.  
   - Communicate a timeline for resolution as soon as diagnostic results are available.
------------------------------------------------------------

============================================================
Processing Incident: INC102
Description: One employee's wireless mouse stopped working.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: LOW

[Resolution Agent] Handling LOW-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC102
Severity: LOW
Assigned Agent: ResolutionAgent

**Troubleshooting Steps for Incident INC102: Wireless Mouse Not Working**

1. **Check the Battery**  
   - Replace the batteries in the mouse if it uses replaceable batteries.  
   - If it has a rechargeable battery, ensure it’s charged.  

2. **Reconnect the Mouse**  
   - Turn off the mouse and turn it back on.  
   - If the mouse connects via Bluetooth, go to your computer's Bluetooth settings, disconnect the mouse, and then reconnect it.  
   - For USB receivers, unplug the receiver and plug it back into a different USB port.  

3. **Check for Interference**  
   - Ensure there are no physical obstructions or other wireless devices nearby that might interfere with the connection.  
   - Try moving the mouse closer to the computer or receiver to ensure proper functionality.  

4. **Restart the Computer**  
   - Fully restart your computer to clear out any temporary issues that may be affecting the connection.  

5. **Verify Compatibility**  
   - Confirm that the mouse is compatible with your device and operating system—check the documentation or manufacturer’s website if needed.

**When to Escalate:**  
If the mouse still doesn’t work after these steps, report the issue to the IT help desk. Mention any troubleshooting steps you've tried and whether the issue persists (e.g., if the mouse doesn’t connect, or it connects but doesn’t function properly).
------------------------------------------------------------

============================================================
Processing Incident: INC103
Description: The company-wide payment processing system is down and transactions are failing.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: HIGH

[Escalation Agent] Handling HIGH-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC103
Severity: HIGH
Assigned Agent: EscalationAgent

**Incident Escalation Plan for INC103**  

1. **Incident Summary**:  
The company-wide payment processing system is down, causing all transactions to fail. This impacts revenue and customer satisfaction.  

2. **Responsible Support Team**:  
Payment Systems Team (primary), IT Infrastructure Team (secondary).  

3. **Immediate Containment Actions**:  
- Disable automated payment retries to prevent system overload.  
- Notify impacted users/customers and share a general announcement about disruptions.  
- Check payment gateway connectivity, API configurations, and related server health.  

4. **Escalation Procedure**:  
- Notify the Payment Systems Team lead and escalate to the IT Operations Manager and Director of IT if unresolved within 30 minutes.  
- Involve third-party vendors (e.g., payment processors) if external systems are implicated.  
- Stand up an emergency bridge call with relevant stakeholders, including senior management if resolution exceeds 1 hour.  

5. **Communication Recommendations**:  
- Inform leadership (CEO, CTO, and CFO) immediately due to business-critical impact.  
- Issue hourly updates to stakeholders, emphasizing remediation progress.  
- Share a timeline for resolution and follow up with a postmortem report to customers once resolved.
------------------------------------------------------------

============================================================
Processing Incident: INC104
Description: One employee cannot print to the nearby office printer.
============================================================

[Triage Agent] Analyzing incident...
[Triage Agent] Severity: LOW

[Resolution Agent] Handling LOW-severity incident...

------------------------------------------------------------
FINAL INCIDENT RESPONSE
------------------------------------------------------------

Incident ID: INC104
Severity: LOW
Assigned Agent: ResolutionAgent

Here are simple troubleshooting steps to help you resolve the printing issue:

### Steps to Check:
1. **Check Printer Status**
   - Make sure the printer is powered on and showing a "Ready" status on its display.
   - If the printer shows an error message, take note of it to share with the help desk, if needed.

2. **Confirm Printer Connection**
   - Ensure the printer is properly connected to the network via the Ethernet cable or Wi-Fi.
   - If it’s a USB printer, confirm the cable is securely plugged into your computer and the printer.

3. **Verify Print Queue**
   - Check your computer's print queue for stuck print jobs. Look for the printer icon near the clock on your screen, click it, and cancel any jobs that may have an error.

4. **Test the Printer**
   - Try printing a different file or document to rule out issues with the file you’re attempting to print.
   - Restart the printer and your computer, then try printing again.

5. **Check Printer Settings**
   - Ensure the correct printer is selected in your computer's print menu. It’s possible the print job is being sent to the wrong printer.

### When to Escalate:
- If the issue persists after completing these steps.
- If the printer shows an error message you don’t understand or cannot resolve.
- If the printer is offline or unresponsive despite verifying connections and restarting devices.

Share the details of what you tried and any error messages with the help desk when escalating the issue.
------------------------------------------------------------

============================================================
ALL INCIDENTS PROCESSED
============================================================

Process finished with exit code 0
