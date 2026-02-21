import sqlite3 # We use the standard library to build a local, structured database.

def get_user_preference(username: str) -> str:
    # We open a direct connection to our local memory file.
    connection = sqlite3.connect("agent_memory.db")
    
    # We create a tool to send commands to the database.
    cursor = connection.cursor()
    
    # We create a table for user preferences if it does not already exist.
    cursor.execute('''CREATE TABLE IF NOT EXISTS preferences 
                      (user TEXT PRIMARY KEY, file_format TEXT)''')
    
    # We insert a test rule to simulate a past conversation with a specific client.
    # The 'IGNORE' command prevents an error if the user is already in the system.
    cursor.execute("INSERT OR IGNORE INTO preferences VALUES ('user_882', 'PDF')")
    connection.commit()
    
    # We ask the database for the exact preferred file format of this user.
    cursor.execute("SELECT file_format FROM preferences WHERE user=?", (username,))
    result = cursor.fetchone()
    
    # We close the connection to keep the database secure and fast.
    connection.close()
    
    # We hand the definitive answer back to the agent.
    return result[0] if result else "Standard Text"

# We run the memory check before the AI starts generating the report.
client_format = get_user_preference("user_882")
print(f"System Directive: Generate the final report strictly as a {client_format} file.")
