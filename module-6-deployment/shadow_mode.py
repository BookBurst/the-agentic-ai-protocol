import sqlite3
import datetime

# The master toggle. Setting this to True keeps the entire system in quarantine.
SHADOW_MODE_ACTIVE = True

# We connect to a local ledger to store the agent's intended actions.
db = sqlite3.connect("shadow_logs.db")
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS shadow_decisions
                  (date TEXT, input_data TEXT, intended_action TEXT, tool_used TEXT)''')
db.commit()

def execute_agent_decision(input_text: str, agent_decision: str, selected_tool: str):
    # The routing logic checks the master toggle before doing anything.
    if SHADOW_MODE_ACTIVE:
        # The agent is quarantined. We write the intention to the silent ledger.
        current_time = datetime.datetime.now().isoformat()
        cursor.execute("INSERT INTO shadow_decisions VALUES (?, ?, ?, ?)",
                       (current_time, input_text, agent_decision, selected_tool))
        db.commit()
        
        # We return a fake success message so the agent thinks the job finished.
        print(f"[SHADOW MODE] Logged intention: {agent_decision}")
        return "Success: Action completed virtually."
        
    # If the toggle is False, the code escapes the quarantine and hits the real world.
    print(f"[LIVE MODE] Executing action on real APIs: {agent_decision}")
    # return trigger_live_api(selected_tool, agent_decision)

# ======== SIMULATING THE WORKFLOW ========

# The agent decides to send a refund based on an angry email.
inbound_email = "My order arrived broken. I want my money back immediately."
ai_generated_response = "Issue a full refund for the broken item."

# The system catches the dangerous decision and routes it to the shadow ledger.
execute_agent_decision(inbound_email, ai_generated_response, "Stripe_Refund_API")
