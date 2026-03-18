from supabase import create_client, Client
from config.settings import settings

supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

def upsert_grant(grant: dict) -> dict:
    """Insert or update a grant opportunity. Deduplicates by grant_id."""
    result = (
        supabase.table("grants")
        .upsert(grant, on_conflict="grant_id")
        .execute()
    )
    return result.data

def get_existing_grant_ids() -> list[str]:
    result = supabase.table("grants").select("grant_id").execute()
    return [row["grant_id"] for row in result.data]

def get_matched_grants(client_id: str, min_score: int = 55) -> list[dict]:
    result = (
        supabase.table("grant_matches")
        .select("*")
        .eq("client_id", client_id)
        .gte("match_score", min_score)
        .order("match_score", desc=True)
        .execute()
    )
    return result.data

def upsert_grant_match(match: dict) -> dict:
    result = (
        supabase.table("grant_matches")
        .upsert(match, on_conflict="grant_id,client_id")
        .execute()
    )
    return result.data
