# 💰 Grant Agent — Non-Dilutive Funding Intelligence

An agentic AI system built for **The Faulkner Group** advisory clients — women's health tech founders seeking grants, SBIR/STTR awards, ARPA-H funding, NIH programs, and private foundation opportunities.

This agent continuously monitors, matches, and drafts application outlines for non-dilutive funding — delivered bi-weekly to each founder based on their stage, indication, and product type.

---

## 🎯 Purpose

Non-dilutive capital is critical in women's health where only 2% of healthcare VC flows to the space. This agent ensures founders never miss an opportunity and always have a head start on applications.

---

## 📦 Grant Sources Monitored

| Source | Type |
|---|---|
| NIH SBIR/STTR | Federal — Small Business |
| ARPA-H | Federal — High-Risk Innovation |
| NSF SBIR | Federal — Tech Innovation |
| HRSA Programs | Federal — Health Services |
| Gates Foundation | Private Foundation |
| Robert Wood Johnson Foundation | Private Foundation |
| Wellcome Trust | Private Foundation |
| State-level SBIR matching programs | State / Regional |
| Women's health-focused prize competitions | Competitions |

---

## 🏗 Architecture

```
grant-agent/
├── agents/
│   ├── discovery_agent.py        # Finds new grant opportunities
│   ├── matching_agent.py         # Matches grants to founder profiles
│   ├── summarizer_agent.py       # Summarizes requirements + eligibility
│   └── draft_agent.py            # Drafts application outline per grant
├── tools/
│   ├── grants_gov_tool.py        # Grants.gov API search
│   ├── nih_reporter_tool.py      # NIH Reporter API
│   ├── sbir_tool.py              # SBIR.gov API
│   └── perplexity_tool.py        # Web research for foundations + prizes
├── pipelines/
│   └── biweekly_grant_run.py     # Full orchestration pipeline
├── db/
│   └── supabase_client.py        # Dedup store for grants + founder profiles
├── delivery/
│   ├── email_digest.py           # Resend HTML digest per client
│   └── notion_push.py            # Notion CRM grant tracker
├── profiles/
│   └── founder_profiles.py       # Founder stage + indication config
├── scheduler/
│   └── cron_runner.py
├── config/
│   └── settings.py
├── .github/
│   └── workflows/
│       ├── grant-pipeline.yml
│       └── manual-test-run.yml
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Setup

```bash
git clone https://github.com/jsfaulkner86/grant-agent
cd grant-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python pipelines/biweekly_grant_run.py
```

---

*Built by The Faulkner Group — Agentic AI for Women's Health Founders*
