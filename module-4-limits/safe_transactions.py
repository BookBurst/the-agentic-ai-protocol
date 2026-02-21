import sqlite3

def update_inventory_safely(db_path: str, inventory_updates: list):
    # We establish a connection to the local database.
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    
    try:
        # We explicitly tell the database to start tracking our changes.
        # This creates our protective all-or-nothing envelope.
        connection.execute("BEGIN TRANSACTION")
        
        for item in inventory_updates:
            # The script attempts to modify multiple rows one by one.
            cursor.execute(
                "UPDATE inventory SET quantity = ? WHERE item_id = ?", 
                (item['new_quantity'], item['id'])
            )
            
            # We simulate a catastrophic software failure halfway through the list.
            if item['id'] == "TRIGGER_CRASH":
                raise ValueError("Network connection lost mid-update.")
                
        # If the loop finishes without errors, we make the changes permanent.
        connection.commit()
        print("All updates applied perfectly. Data is safe.")
        
    except Exception as crash_report:
        # The script caught a critical error during the execution.
        # We command the database to undo every single change made so far.
        connection.rollback()
        print(f"Catastrophic failure detected. Rolling back changes. Log: {crash_report}")
        
    finally:
        # We always close the connection to prevent memory leaks on the server.
        connection.close()

# We test the system with a poisoned data list that forces a mid-task crash.
bad_data = [
    {"id": "apple", "new_quantity": 100}, 
    {"id": "TRIGGER_CRASH", "new_quantity": 0},
    {"id": "banana", "new_quantity": 50}
]

# The script hits the bad data, crashes, and un-does the change to "apple".
# update_inventory_safely("my_warehouse.db", bad_data)
