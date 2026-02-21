import os
from notion_client import Client

# We initialize the client using an environment variable.
# Hardcoding secrets is the fastest way to lose control of your infrastructure.
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def save_to_notion(title: str, content: str):
    """
    This tool allows the agent to write research directly to a database.
    We define the structure so the agent knows exactly which 'keys' to fill.
    """
    parent_id = os.getenv("NOTION_DATABASE_ID")
    
    # We build the page structure using the standard Notion schema.
    # This prevents the model from sending raw text that the API would reject.
    notion.pages.create(
        parent={"database_id": parent_id},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Status": {"select": {"name": "Agent Generated"}}
        },
        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": content}}]}
            }
        ]
    )
    return "Successfully saved to Notion."
