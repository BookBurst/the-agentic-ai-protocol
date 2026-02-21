import os
from notion_client import Client

notion = Client(auth=os.getenv("NOTION_TOKEN"))

def save_to_notion(title: str, content: str):
    parent_id = os.getenv("NOTION_DATABASE_ID")
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
