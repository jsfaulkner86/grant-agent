from crewai import Crew, Task
from agents.discovery_agent import discovery_agent, DISCOVERY_QUERIES
from agents.matching_agent import matching_agent, MATCHING_PROMPT
from agents.summarizer_agent import summarizer_agent
from agents.draft_agent import draft_agent, DRAFT_PROMPT
from db.supabase_client import (
    upsert_grant, get_existing_grant_ids, upsert_grant_match, get_matched_grants
)
from delivery.notion_push import push_grant_to_notion
from delivery.email_digest import send_grant_digest
from profiles.founder_profiles import FOUNDER_PROFILES
import json

def run_pipeline():
    print("[GrantAgent] Starting bi-weekly grant pipeline run...")
    existing_ids = get_existing_grant_ids()

    # Step 1: Discover grants
    discovery_task = Task(
        description=f"Search all sources for open women's health grant opportunities using these queries: {DISCOVERY_QUERIES}",
        agent=discovery_agent,
        expected_output="A list of grant opportunities with name, funder, type, award range, deadline, and URL.",
    )
    summarize_task = Task(
        description="Summarize requirements and eligibility for each discovered grant opportunity.",
        agent=summarizer_agent,
        expected_output="Structured grant summaries with all key fields populated or marked null.",
    )
    discovery_crew = Crew(
        agents=[discovery_agent, summarizer_agent],
        tasks=[discovery_task, summarize_task],
        verbose=True,
    )
    raw_grants = discovery_crew.kickoff()

    try:
        grants = json.loads(raw_grants) if isinstance(raw_grants, str) else raw_grants
    except Exception as e:
        print(f"[GrantAgent] Grant parse error: {e}")
        grants = []

    # Step 2: Persist new grants
    new_grants = [g for g in grants if g.get("grant_id") not in existing_ids]
    for grant in new_grants:
        upsert_grant(grant)

    # Step 3: Match + draft per founder
    for profile in FOUNDER_PROFILES:
        matching_task = Task(
            description=(
                f"Score each grant for this founder profile:\n{json.dumps(profile, indent=2)}\n"
                f"Use this rubric:\n{MATCHING_PROMPT}"
            ),
            agent=matching_agent,
            expected_output="List of grant matches with match_score and match_rationale per grant.",
        )
        draft_task = Task(
            description=(
                f"For grants with match_score >= {55}, draft an application outline.\n"
                f"Founder profile:\n{json.dumps(profile, indent=2)}\n"
                f"Use this structure:\n{DRAFT_PROMPT}"
            ),
            agent=draft_agent,
            expected_output="Application outlines keyed by grant_id.",
        )
        match_crew = Crew(
            agents=[matching_agent, draft_agent],
            tasks=[matching_task, draft_task],
            verbose=True,
        )
        match_results = match_crew.kickoff()

        try:
            matches = json.loads(match_results) if isinstance(match_results, str) else match_results
        except Exception as e:
            print(f"[GrantAgent] Match parse error for {profile['client_id']}: {e}")
            matches = []

        grants_with_matches = []
        for match in matches:
            match["client_id"] = profile["client_id"]
            upsert_grant_match(match)
            grant = next((g for g in grants if g.get("grant_id") == match.get("grant_id")), {})
            draft = match.get("draft_outline", "See Notion for outline.")
            if grant and match.get("match_score", 0) >= 55:
                push_grant_to_notion(grant, match, draft)
                grants_with_matches.append((grant, match))

        send_grant_digest(
            recipient_email=profile["email"],
            founder_name=profile["founder_name"],
            grants_with_matches=grants_with_matches,
        )

    print("[GrantAgent] Pipeline run complete.")

if __name__ == "__main__":
    run_pipeline()
