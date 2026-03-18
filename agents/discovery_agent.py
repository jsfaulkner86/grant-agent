from crewai import Agent
from tools.grants_gov_tool import search_grants_gov
from tools.nih_reporter_tool import search_nih_funding
from tools.sbir_tool import search_sbir_solicitations
from tools.perplexity_tool import search_grants

DISCOVERY_QUERIES = [
    "women's health digital health maternal health",
    "femtech reproductive health innovation",
    "menopause endometriosis fertility technology",
    "women's health SBIR small business",
    "ARPA-H women's health program",
    "private foundation grants women's health startups 2025 2026",
    "prize competition women's health tech innovation",
]

discovery_agent = Agent(
    role="Grant Discovery Specialist",
    goal=(
        "Discover all open, forecasted, and upcoming non-dilutive funding opportunities "
        "relevant to women's health tech startups. Cover federal grants, SBIR/STTR, "
        "ARPA-H, NSF, private foundations, and prize competitions."
    ),
    backstory=(
        "You are a federal grant and foundation funding specialist with deep expertise "
        "in women's health. You know every funding mechanism available and you find "
        "opportunities others miss. You work for The Faulkner Group to give women's "
        "health founders a decisive non-dilutive funding advantage."
    ),
    tools=[search_grants_gov, search_nih_funding, search_sbir_solicitations, search_grants],
    verbose=True,
    allow_delegation=False,
)
