from notion_client import Client
from config.settings import settings

notion = Client(auth=settings.notion_api_key)

def push_grant_to_notion(grant: dict, match: dict, draft_outline: str) -> str:
    """
    Write a matched grant opportunity + draft outline to Notion.
    Returns the URL of the created page.
    """
    props = {
        "Grant Name": {"title": [{"text": {"content": grant.get("name", "Unknown")}}]},
        "Funder": {"rich_text": [{"text": {"content": grant.get("funder", "Unknown")}}]},
        "Award Range": {"rich_text": [{"text": {"content": grant.get("award_range", "Unknown")}}]},
        "Deadline": {"rich_text": [{"text": {"content": grant.get("deadline", "Unknown")}}]},
        "Match Score": {"number": match.get("match_score", 0)},
        "Client": {"rich_text": [{"text": {"content": match.get("client_id", "")}}]},
        "Application URL": {"url": grant.get("url")},
        "Grant Type": {"select": {"name": grant.get("type", "Federal")}},
        "Status": {"select": {"name": "New"}},
    }
    page = notion.pages.create(
        parent={"database_id": settings.notion_database_id},
        properties=props,
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Application Outline"}}]},
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": draft_outline}}]},
            },
        ],
    )
    return page["url"]
