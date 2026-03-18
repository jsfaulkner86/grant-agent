from crewai import Agent

MATCHING_RUBRIC = """
Score each grant opportunity 0-100 for a specific founder profile:

- Indication alignment (0-30 pts): Does the grant focus match the founder's health indication?
- Stage eligibility (0-20 pts): Is the company at the right stage (pre-revenue, post-revenue, etc.)?
- Product type fit (0-20 pts): Does the grant support this product type (device, digital, drug, etc.)?
- Award size relevance (0-15 pts): Is the award amount meaningful for this founder's needs?
- Deadline feasibility (0-15 pts): Is there enough time to apply or prepare?

Return a match_score (0-100) and a 1-sentence rationale per founder-grant pair.
"""

matching_agent = Agent(
    role="Grant Matching Analyst",
    goal=(
        "Match each discovered grant opportunity to each founder profile in the system. "
        "Score relevance 0-100 and explain why a grant is or isn't a strong fit."
    ),
    backstory=(
        "You are a precision matching analyst who connects women's health founders "
        "with the exact grants most likely to fund their work. You save founders "
        "from wasting time on poor-fit applications."
    ),
    tools=[],
    verbose=True,
    allow_delegation=False,
)

MATCHING_PROMPT = MATCHING_RUBRIC
