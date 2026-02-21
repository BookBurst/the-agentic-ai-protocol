import sqlite3
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key="your_api_key_here")

# We establish a connection to a local database file to store our financial logs.
db_connection = sqlite3.connect("agent_finances.db")
cursor = db_connection.cursor()

# We create a simple table to hold the exact token counts for every single action.
cursor.execute('''CREATE TABLE IF NOT EXISTS token_logs
                  (timestamp TEXT, task_name TEXT, input_count INT, output_count INT)''')
db_connection.commit()

def monitored_agent_action(task_name: str, prompt_text: str) -> str:
    # The system sends the request to the language model.
    response = client.chat.completions.create(
        model="<LATEST_REASONING_MODEL>",
        messages=[{"role": "user", "content": prompt_text}]
    )
    
    # We extract the hidden metadata attached to the official API response.
    usage_data = response.usage
    input_tokens = usage_data.prompt_tokens
    output_tokens = usage_data.completion_tokens
    
    # We write the exact consumption numbers into our permanent ledger.
    cursor.execute("INSERT INTO token_logs VALUES (?, ?, ?, ?)", 
                   (datetime.now().isoformat(), task_name, input_tokens, output_tokens))
    db_connection.commit()
    
    return response.choices[0].message.content

# ======== EXECUTING THE MONITORED TASK ========

# We run a standard background process with full financial tracking enabled.
# result = monitored_agent_action("market_analysis", "Summarize the latest tech trends.")
# print("Task complete. Finances logged securely.")
