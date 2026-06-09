"""
design.py — Enterprise AI Decision Intelligence Platform
=========================================================
Run: streamlit run design.py

One file. Shows the ENTIRE platform end-to-end with realistic simulated outputs.
Every click produces real-looking data — costs, models, debate transcripts,
RAG sources, Prometheus metrics, Langfuse traces, governance queue, FinOps.

Take screenshots of every page/state for your GitHub README.
"""

import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Enterprise AI Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Sora:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }

.main { background: #0a0a0f; }
.block-container { padding: 1.5rem 2rem; max-width: 1400px; }

.hero-title {
    font-size: 2.1rem; font-weight: 700; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.1rem;
}
.hero-sub {
    font-size: 0.85rem; color: #64748b; letter-spacing: 0.05em;
    text-transform: uppercase; font-weight: 400; margin-bottom: 1.5rem;
}

.card {
    background: #111118; border: 1px solid #1e1e2e;
    border-radius: 10px; padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.card-accent { border-left: 3px solid #6366f1; }
.card-green  { border-left: 3px solid #22c55e; }
.card-yellow { border-left: 3px solid #f59e0b; }
.card-red    { border-left: 3px solid #ef4444; }
.card-blue   { border-left: 3px solid #3b82f6; }
.card-purple { border-left: 3px solid #a855f7; }

.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em;
    text-transform: uppercase; margin-right: 6px;
}
.badge-simple  { background: #052e16; color: #86efac; border: 1px solid #166534; }
.badge-medium  { background: #431407; color: #fdba74; border: 1px solid #9a3412; }
.badge-complex { background: #2d1b69; color: #c4b5fd; border: 1px solid #4c1d95; }
.badge-low     { background: #052e16; color: #86efac; border: 1px solid #166534; }
.badge-medium-risk { background: #431407; color: #fdba74; border: 1px solid #9a3412; }
.badge-high    { background: #450a0a; color: #fca5a5; border: 1px solid #7f1d1d; }
.badge-hit     { background: #042f2e; color: #5eead4; border: 1px solid #0f766e; }
.badge-miss    { background: #1c1917; color: #78716c; border: 1px solid #292524; }

.model-tag {
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    background: #1e1e2e; color: #818cf8; padding: 3px 8px;
    border-radius: 4px; border: 1px solid #2d2d42;
}
.cost-tag {
    font-family: 'DM Mono', monospace; font-size: 0.78rem;
    color: #f59e0b; font-weight: 500;
}
.pipeline-step {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 12px; margin: 3px 0;
    background: #111118; border-radius: 6px; border: 1px solid #1e1e2e;
    font-size: 0.82rem; color: #94a3b8;
}
.pipeline-step .icon { font-size: 1rem; min-width: 22px; }
.pipeline-step .label { flex: 1; }
.pipeline-step .timing {
    font-family: 'DM Mono', monospace; font-size: 0.70rem;
    color: #475569;
}
.agent-card {
    background: #0d0d14; border: 1px solid #1e1e2e;
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.6rem;
}
.agent-advocate { border-top: 2px solid #22c55e; }
.agent-critic   { border-top: 2px solid #ef4444; }
.agent-judge    { border-top: 2px solid #f59e0b; }
.agent-header {
    font-size: 0.80rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; margin-bottom: 0.5rem;
}
.agent-advocate .agent-header { color: #22c55e; }
.agent-critic   .agent-header { color: #ef4444; }
.agent-judge    .agent-header { color: #f59e0b; }
.source-chip {
    display: inline-block; background: #1e1e2e;
    border: 1px solid #2d2d42; border-radius: 4px;
    padding: 4px 10px; margin: 3px; font-size: 0.73rem; color: #94a3b8;
    font-family: 'DM Mono', monospace;
}
.metric-number {
    font-family: 'DM Mono', monospace; font-size: 1.8rem;
    font-weight: 500; color: #e2e8f0; line-height: 1;
}
.metric-label { font-size: 0.75rem; color: #64748b; margin-top: 3px; }
.trace-line {
    font-family: 'DM Mono', monospace; font-size: 0.72rem;
    color: #475569; padding: 4px 0; border-bottom: 1px solid #1e1e2e;
}
.trace-line span { color: #818cf8; }
.pii-tag {
    background: #450a0a; color: #fca5a5;
    border: 1px solid #7f1d1d; border-radius: 4px;
    padding: 2px 8px; font-size: 0.72rem; font-family: 'DM Mono', monospace;
}
.gov-pending {
    background: #431407; border: 1px solid #9a3412;
    border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.6rem;
}
.section-label {
    font-size: 0.70rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.08em; color: #4b5563; margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA — All realistic simulation data
# ══════════════════════════════════════════════════════════════════════════════

QUERIES = {
    "simple": {
        "text": "What is the total headcount across all departments?",
        "complexity": "simple", "risk": "low", "debate": False,
        "model": "claude-3-haiku-20240307",
        "cost_inr": 0.08, "latency_ms": 1840,
        "rewritten": "total employee headcount all departments workforce size",
        "answer": """Based on the HR Annual Report FY2024 (Section 2.1 — Workforce Summary):

**Total Headcount: 2,847 employees** as of December 31, 2024.

**Breakdown by department:**
- Engineering & Technology: 834 (29.3%)
- Sales & Business Development: 521 (18.3%)
- Operations & Supply Chain: 467 (16.4%)
- Finance & Accounting: 312 (11.0%)
- Human Resources: 189 (6.6%)
- Marketing & Communications: 246 (8.6%)
- Legal & Compliance: 98 (3.4%)
- Executive & Administration: 180 (6.3%)

Year-over-year growth: +312 employees (+12.3%) from FY2023's 2,535.
""",
        "sources": [
            {"doc": "HR_Annual_Report_FY2024.pdf", "section": "Workforce Summary", "score": 0.94},
            {"doc": "HR_Annual_Report_FY2024.pdf", "section": "Department Breakdown", "score": 0.89},
            {"doc": "HR_Policy_Manual_v3.pdf", "section": "Org Structure", "score": 0.71},
        ],
        "confidence": 0.91, "hal_risk": "low",
        "costs": [
            {"stage": "classification", "model": "groq/llama3-70b", "tokens": 428, "cost": 0.003},
            {"stage": "rewrite", "model": "groq/llama3-70b", "tokens": 352, "cost": 0.003},
            {"stage": "rag_generation", "model": "claude-3-haiku", "tokens": 1640, "cost": 0.074},
        ],
        "cache_hit": False,
        "pii_found": False,
    },
    "medium": {
        "text": "Analyse our Q3 and Q4 revenue trends and identify the top 3 growth drivers.",
        "complexity": "medium", "risk": "medium", "debate": False,
        "model": "claude-3-5-sonnet-20241022",
        "cost_inr": 0.52, "latency_ms": 4120,
        "rewritten": "Q3 Q4 revenue trend analysis growth drivers financial performance quarterly",
        "answer": """Based on the Annual Report FY2024 (Section 4 — Financial Performance) and the Q3/Q4 Financial Summary:

**Revenue Overview:**
- Q3 FY2024: ₹847 crore (+18.2% YoY)
- Q4 FY2024: ₹923 crore (+22.7% YoY)
- Full Year: ₹3,241 crore (+19.4% YoY)

**Top 3 Growth Drivers:**

**1. Enterprise SaaS Subscriptions (+34.2% YoY)**
Recurring revenue from enterprise licenses grew from ₹410 cr to ₹550 cr. The shift to annual contracts (cited in Section 4.3) improved predictability and reduced churn from 8.2% to 5.7%.

**2. Geographic Expansion — Tier 2 & 3 Cities (+28.7% YoY)**
New market penetration strategy launched in Q1 contributed ₹187 crore in incremental revenue by Q4. Section 5.1 highlights 14 new city offices opened.

**3. Professional Services & Implementation (+19.1% YoY)**
As the enterprise customer base grew, implementation and consulting revenue scaled proportionally. Average contract value increased from ₹42L to ₹58L per enterprise client.

**Margin impact:** Gross margin improved 210bps to 68.4% due to operating leverage on the SaaS business.
""",
        "sources": [
            {"doc": "Annual_Report_FY2024.pdf", "section": "Financial Performance", "score": 0.96},
            {"doc": "Annual_Report_FY2024.pdf", "section": "Revenue Breakdown", "score": 0.92},
            {"doc": "Annual_Report_FY2024.pdf", "section": "Geographic Expansion", "score": 0.87},
            {"doc": "Q4_Financial_Summary.pdf", "section": "Quarterly Results", "score": 0.83},
        ],
        "confidence": 0.88, "hal_risk": "low",
        "costs": [
            {"stage": "classification", "model": "groq/llama3-70b", "tokens": 441, "cost": 0.003},
            {"stage": "rewrite", "model": "groq/llama3-70b", "tokens": 368, "cost": 0.003},
            {"stage": "rag_generation", "model": "claude-3-5-sonnet", "tokens": 2210, "cost": 0.514},
        ],
        "cache_hit": False,
        "pii_found": False,
    },
    "complex": {
        "text": "Should we acquire TechStartup XYZ for ₹200 crore given their ₹40 crore ARR and 60% growth rate? What are the risks?",
        "complexity": "complex", "risk": "high", "debate": True,
        "model": "claude-3-opus-20240229",
        "cost_inr": 12.40, "latency_ms": 47200,
        "rewritten": "acquisition valuation ₹200 crore ARR growth rate due diligence risk analysis fintech startup",
        "answer": """**JUDGE'S FINAL SYNTHESIS & RECOMMENDATION**

After reviewing both the Advocate and Critic positions and conducting additional document research:

**Recommendation: CONDITIONAL PROCEED** *(Confidence: 71%)*

**Valuation Assessment:**
The ₹200 crore price represents a 5.0x ARR multiple. Per our M&A Framework Guide (Section 3.2), the acceptable range for high-growth SaaS in Indian markets is 4x–8x ARR. At 60% growth, 5x is defensible but leaves limited margin of safety.

**Three Non-Negotiable Conditions Before Signing:**

1. **Customer Concentration Verification** — Critic correctly identifies this as the primary risk. If top 3 customers exceed 35% of ARR, effective risk-adjusted multiple exceeds 7x. Require full customer breakdown in due diligence (M&A Checklist, Item 7.3).

2. **Growth Rate Confirmation** — 60% must be verified as trailing-twelve-month YoY, not MoM or cherry-picked period. Request monthly MRR cohort data for 24 months.

3. **Technology Compatibility Audit** — Our Technology Integration Policy (Section 8) requires architecture review before any acquisition. Estimated 3-month integration timeline if stack is compatible.

**Action Items:**
- Week 1–2: Customer concentration analysis + MRR cohort review
- Week 2–4: Technical due diligence
- Week 4–6: Legal & IP review, negotiate earnout (20% of deal value, 2-year performance clause)
- Decision deadline: 6 weeks from today
""",
        "advocate_output": """**ADVOCATE POSITION — The Case For Acquisition**

The acquisition of TechStartup XYZ at ₹200 crore represents a strategically compelling opportunity that I recommend proceeding with.

**Valuation is Attractive:**
At 5.0x ARR, this acquisition sits at the lower end of the acceptable range for high-growth SaaS per our M&A Framework Guide (Section 3.2 cites 4x–8x for growth-stage companies). With 60% ARR growth, the forward multiple drops to 3.1x, making this a potential value acquisition.

**Strategic Fit:**
The target's product complements our existing enterprise suite (Section 6.1 of our Strategic Plan identifies fintech integration as a priority for FY25). Cross-sell opportunity across our 847 enterprise customers could add ₹28–35 crore incremental ARR within 18 months.

**Market Timing:**
Fintech valuations have compressed 40% since 2022. This is a buyer's market. Waiting 12 months risks the window closing as the target approaches profitability and commands a premium re-rating.

**Recommendation:** APPROVE with standard due diligence. The financial profile is sound.""",

        "critic_output": """**CRITIC POSITION — Risks and Challenges**

While the Advocate presents a reasonable bull case, I identify several material risks that require resolution before any recommendation.

**Risk 1 — Customer Concentration (HIGH)**
The 60% growth rate and ₹40 crore ARR sound impressive, but we have no visibility into customer concentration. If 3 customers represent 50%+ of revenue (common in early-stage B2B), the actual risk-adjusted ARR is ₹20–25 crore — changing the multiple to 8–10x. This is not in the acceptable range.

**Risk 2 — Growth Rate Sustainability (MEDIUM)**
60% YoY growth at ₹40 crore ARR is achievable but not automatically repeatable. Without cohort retention data, we cannot distinguish between genuine product-market fit and one-time enterprise deals. I have seen 3 similar acquisitions where growth halved in the year post-acquisition.

**Risk 3 — Integration Cost Underestimation (MEDIUM)**
Our last two acquisitions underestimated integration costs by an average of 34% (Finance Report, Acquisition Post-Mortems section). At ₹200 crore deal size, a 34% cost overrun on a ₹30 crore integration budget adds ₹10 crore of unplanned expense.

**Risk 4 — Opportunity Cost (LOW-MEDIUM)**
₹200 crore deployed in an acquisition is ₹200 crore not available for organic R&D where our ROI has historically been 2.3x over 3 years (Strategic Plan, Capital Allocation section).

**Recommendation:** DO NOT APPROVE without resolving customer concentration and growth cohort data first.""",

        "sources": [
            {"doc": "MA_Framework_Guide.pdf", "section": "Valuation Methodology", "score": 0.97},
            {"doc": "MA_Framework_Guide.pdf", "section": "Due Diligence Checklist", "score": 0.94},
            {"doc": "Annual_Report_FY2024.pdf", "section": "Strategic Priorities FY25", "score": 0.88},
            {"doc": "Finance_Policy_Manual.pdf", "section": "Acquisition Post-Mortems", "score": 0.81},
            {"doc": "Technology_Integration_Policy.pdf", "section": "Acquisition Protocol", "score": 0.76},
        ],
        "confidence": 0.71, "hal_risk": "medium",
        "costs": [
            {"stage": "classification", "model": "groq/llama3-70b", "tokens": 462, "cost": 0.004},
            {"stage": "rewrite", "model": "groq/llama3-70b", "tokens": 389, "cost": 0.003},
            {"stage": "rag_generation", "model": "claude-3-opus", "tokens": 2580, "cost": 2.303},
            {"stage": "debate_advocate", "model": "claude-3-5-sonnet", "tokens": 2840, "cost": 3.012},
            {"stage": "debate_critic", "model": "gpt-4o", "tokens": 2910, "cost": 3.478},
            {"stage": "debate_judge", "model": "gemini-1.5-pro", "tokens": 3200, "cost": 3.600},
        ],
        "cache_hit": False,
        "pii_found": False,
    },
    "cached": {
        "text": "How many employees do we have?",
        "complexity": "simple", "risk": "low", "debate": False,
        "model": "cache",
        "cost_inr": 0.00, "latency_ms": 183,
        "answer": "Based on the HR Annual Report FY2024 (Section 2.1): **Total Headcount: 2,847 employees** as of December 31, 2024.",
        "sources": [],
        "confidence": 0.91, "hal_risk": "low",
        "costs": [],
        "cache_hit": True,
        "pii_found": False,
        "rewritten": "",
    },
    "pii": {
        "text": "What is the salary of Rajesh Kumar (Aadhaar: 1234 5678 9012) in the finance team?",
        "complexity": "medium", "risk": "high", "debate": False,
        "model": "GOVERNANCE PAUSED",
        "cost_inr": 0.003, "latency_ms": 310,
        "answer": "⏸️ Query held for governance review.",
        "sources": [],
        "confidence": 0.0, "hal_risk": "high",
        "costs": [{"stage": "classification", "model": "groq/llama3-70b", "tokens": 441, "cost": 0.003}],
        "cache_hit": False,
        "pii_found": True,
        "pii_types": ["AADHAAR", "PERSON_NAME"],
        "redacted": "What is the salary of <PERSON> (Aadhaar: <AADHAAR_NUMBER>) in the finance team?",
        "triggered_rule": "pii_detected + sensitive_employee_data",
        "rewritten": "",
    },
}

DOCUMENTS = [
    {"name": "Annual_Report_FY2024.pdf", "type": "PDF", "size": "4.2 MB", "chunks": 94, "status": "ready"},
    {"name": "HR_Policy_Manual_v3.docx", "type": "DOCX", "size": "1.8 MB", "chunks": 67, "status": "ready"},
    {"name": "MA_Framework_Guide.pdf", "type": "PDF", "size": "2.1 MB", "chunks": 51, "status": "ready"},
    {"name": "Q4_Financial_Summary.xlsx", "type": "XLSX", "size": "0.9 MB", "chunks": 38, "status": "ready"},
    {"name": "Technology_Integration_Policy.pdf", "type": "PDF", "size": "1.1 MB", "chunks": 28, "status": "ready"},
]

GOVERNANCE_QUEUE = [
    {
        "id": "gov_8f2a1c9d",
        "query": "What is the salary of Rajesh Kumar (Aadhaar: 1234 5678 9012) in the finance team?",
        "risk": "high", "pii": True, "pii_types": ["AADHAAR", "PERSON_NAME"],
        "rule": "pii_detected + sensitive_employee_data",
        "time": "2 minutes ago",
    },
    {
        "id": "gov_3b7e4f12",
        "query": "Should I invest my personal savings of ₹25 lakh in company equity before the IPO?",
        "risk": "high", "pii": False, "pii_types": [],
        "rule": "financial_advice_request + insider_trading_risk",
        "time": "18 minutes ago",
    },
    {
        "id": "gov_c91d5a77",
        "query": "What are the confidential terms of the merger agreement with GlobalCorp?",
        "risk": "high", "pii": False, "pii_types": [],
        "rule": "sensitive_financial_data + confidential_ma_information",
        "time": "1 hour ago",
    },
]

def make_finops_data():
    models = {
        "claude-3-haiku": 18.42,
        "claude-3-5-sonnet": 67.83,
        "claude-3-opus": 31.20,
        "gpt-4o": 44.17,
        "gemini-1.5-pro": 28.91,
        "groq/llama3-70b": 2.14,
    }
    dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]
    daily = [round(random.uniform(4.2, 18.7), 2) for _ in dates]
    return models, dates, daily

EVAL_DATA = {
    "queries": [
        "What is the company's revenue growth strategy?",
        "What are the key financial risks mentioned?",
        "What HR policies are described?",
        "What are the vendor selection criteria?",
        "What is the investment timeline?",
        "Summarise the executive team structure",
        "What cost reduction initiatives are planned?",
        "What technology stack does the company use?",
        "What are the compliance requirements mentioned?",
        "What market expansion plans exist?",
    ],
    "answer_relevance":  [0.91, 0.87, 0.89, 0.78, 0.82, 0.94, 0.81, 0.76, 0.83, 0.88],
    "context_relevance": [0.88, 0.82, 0.79, 0.71, 0.76, 0.91, 0.74, 0.68, 0.85, 0.83],
    "groundedness":      [0.93, 0.89, 0.85, 0.74, 0.81, 0.88, 0.79, 0.77, 0.84, 0.86],
}

PROMETHEUS_METRICS = """# HELP enterprise_ai_requests_total Total queries processed
# TYPE enterprise_ai_requests_total counter
enterprise_ai_requests_total{complexity="simple",risk_level="low",cache_hit="False"} 847
enterprise_ai_requests_total{complexity="simple",risk_level="low",cache_hit="True"} 1243
enterprise_ai_requests_total{complexity="medium",risk_level="medium",cache_hit="False"} 312
enterprise_ai_requests_total{complexity="complex",risk_level="high",cache_hit="False"} 89

# HELP enterprise_ai_cost_inr_total Cumulative cost in INR
# TYPE enterprise_ai_cost_inr_total counter
enterprise_ai_cost_inr_total{model="claude-3-haiku-20240307"} 18.42
enterprise_ai_cost_inr_total{model="claude-3-5-sonnet-20241022"} 67.83
enterprise_ai_cost_inr_total{model="claude-3-opus-20240229"} 31.20
enterprise_ai_cost_inr_total{model="gpt-4o"} 44.17
enterprise_ai_cost_inr_total{model="gemini/gemini-1.5-pro"} 28.91
enterprise_ai_cost_inr_total{model="groq/llama3-70b-8192"} 2.14

# HELP enterprise_ai_cache_hits_total Semantic cache hits
# TYPE enterprise_ai_cache_hits_total counter
enterprise_ai_cache_hits_total 1243

# HELP enterprise_ai_governance_pending Queries awaiting review
# TYPE enterprise_ai_governance_pending gauge
enterprise_ai_governance_pending 3

# HELP enterprise_ai_debates_total Three-agent debates triggered
# TYPE enterprise_ai_debates_total counter
enterprise_ai_debates_total 89

# HELP enterprise_ai_request_latency_seconds Request latency
# TYPE enterprise_ai_request_latency_seconds histogram
enterprise_ai_request_latency_seconds_bucket{complexity="simple",le="2.0"} 821
enterprise_ai_request_latency_seconds_bucket{complexity="simple",le="5.0"} 847
enterprise_ai_request_latency_seconds_bucket{complexity="medium",le="5.0"} 289
enterprise_ai_request_latency_seconds_bucket{complexity="medium",le="10.0"} 312
enterprise_ai_request_latency_seconds_bucket{complexity="complex",le="60.0"} 89

# HELP enterprise_ai_errors_total Errors by stage
# TYPE enterprise_ai_errors_total counter
enterprise_ai_errors_total{stage="rag_generation"} 3
enterprise_ai_errors_total{stage="debate"} 1
enterprise_ai_errors_total{stage="classification"} 0"""

LANGFUSE_TRACES = [
    {"id": "trc_8f2a1c9d3e", "query": "What is total headcount?", "model": "claude-3-haiku", "tokens": 2068, "cost": "₹0.08", "latency": "1.84s", "status": "success"},
    {"id": "trc_3b7e4f1290", "query": "Analyse Q3 Q4 revenue trends...", "model": "claude-3-5-sonnet", "tokens": 3019, "cost": "₹0.52", "latency": "4.12s", "status": "success"},
    {"id": "trc_c91d5a77ff", "query": "Should we acquire TechStartup...", "model": "claude-3-opus+debate", "tokens": 12381, "cost": "₹12.40", "latency": "47.2s", "status": "success"},
    {"id": "trc_a44f2b81cc", "query": "How many employees do we have?", "model": "cache", "tokens": 0, "cost": "₹0.00", "latency": "0.18s", "status": "cache_hit"},
    {"id": "trc_d77e9c3412", "query": "What is salary of Rajesh Kumar...", "model": "BLOCKED", "tokens": 441, "cost": "₹0.003", "latency": "0.31s", "status": "governance_paused"},
]

AUDIT_LOG = [
    {"id": "gov_1a2b3c", "query": "What are merger terms with ABC Corp?", "action": "rejected", "reviewer": "compliance_01", "risk": "high", "rule": "confidential_ma_data", "note": "Rejected — NDA in place, restricted to deal team only", "time": "2024-12-18 14:23"},
    {"id": "gov_4d5e6f", "query": "Should I sell my ESOPs before earnings?", "action": "rejected", "reviewer": "compliance_01", "risk": "high", "rule": "financial_advice + insider_risk", "note": "Potential insider trading risk — escalated to Legal", "time": "2024-12-18 11:07"},
    {"id": "gov_7g8h9i", "query": "What is the Q4 revenue forecast?", "action": "approved", "reviewer": "compliance_02", "risk": "medium", "rule": "sensitive_financial_data", "note": "Approved — user is CFO, authorized access", "time": "2024-12-17 16:45"},
    {"id": "gov_j1k2l3", "query": "Analyse vendor contract with XYZ Pvt Ltd", "action": "approved", "reviewer": "compliance_02", "risk": "medium", "rule": "sensitive_financial_data", "note": "Approved — procurement team, standard request", "time": "2024-12-17 09:12"},
    {"id": "gov_m4n5o6", "query": "Employee list with salary bands", "action": "rejected", "reviewer": "compliance_01", "risk": "high", "rule": "pii_detected + employee_data", "note": "Rejected — bulk PII request requires HR Director approval", "time": "2024-12-16 15:33"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def complexity_badge(c):
    cls = {"simple": "badge-simple", "medium": "badge-medium", "complex": "badge-complex"}.get(c, "badge-simple")
    return f'<span class="badge {cls}">{c}</span>'

def risk_badge(r):
    cls = {"low": "badge-low", "medium": "badge-medium-risk", "high": "badge-high"}.get(r, "badge-low")
    return f'<span class="badge {cls}">Risk: {r}</span>'

def cache_badge(hit):
    if hit:
        return '<span class="badge badge-hit">⚡ Cache HIT</span>'
    return '<span class="badge badge-miss">Cache MISS</span>'

def model_tag(m):
    return f'<span class="model-tag">{m}</span>'

def render_pipeline_steps(query_type):
    q = QUERIES[query_type]
    steps = [
        ("🔒", "PII Scan (Presidio + Indian ID Regex)", "83ms", q["pii_found"]),
        ("🤖", f"Classification — Groq/Llama3-70b (function calling)", "312ms", False),
        ("⚡", "Semantic Cache Lookup — Weaviate nearText", "91ms", False),
        ("🛡️", "Guardrail Check — Pattern matching", "12ms", False),
        ("✏️", "Query Rewriting — Groq/Llama3-70b", "281ms", False),
        ("🔍", "Hybrid Search — Weaviate (BM25 + Vector, alpha=0.5)", "143ms", False),
        ("📊", "Reranking — Cohere Rerank v3", "418ms", False),
        ("🧭", "Routing Decision — Complexity → Model Tier", "1ms", False),
        ("🧠", f"RAG Generation — {q['model']}", "2,710ms" if query_type != "complex" else "8,700ms", False),
    ]
    if query_type == "complex":
        steps += [
            ("🎭", "Debate: Advocate — claude-3-5-sonnet-20241022", "12,400ms", False),
            ("⚔️", "Debate: Critic — gpt-4o", "13,100ms", False),
            ("⚖️", "Debate: Judge — gemini-1.5-pro (+ tools)", "15,800ms", False),
        ]
    steps += [
        ("📏", "Confidence Scoring — Word overlap heuristic", "8ms", False),
        ("💾", "Write to PostgreSQL (query_logs + debate_records)", "68ms", False),
        ("🗄️", "Cache Store — Weaviate SemanticCache", "82ms", False),
        ("📈", "Prometheus Metrics Update", "2ms", False),
        ("🔭", "Langfuse Trace Flush", "async", False),
    ]
    html = '<div style="margin: 0.5rem 0;">'
    for icon, label, timing, is_pii in steps:
        color = "#ef4444" if is_pii else "#22c55e"
        dot = f'<span style="color:{color};font-size:0.55rem;margin-right:6px;">●</span>'
        html += f'''<div class="pipeline-step">
            <span class="icon">{icon}</span>
            <span class="label">{dot}{label}</span>
            <span class="timing">{timing}</span>
        </div>'''
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_sources(sources):
    html = '<div style="margin: 0.4rem 0;">'
    for s in sources:
        score_color = "#22c55e" if s["score"] > 0.85 else "#f59e0b" if s["score"] > 0.70 else "#94a3b8"
        html += f'<span class="source-chip">📄 {s["doc"]} › {s["section"]} <span style="color:{score_color}">▸ {s["score"]:.2f}</span></span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def confidence_bar(score, risk):
    color = {"low": "#22c55e", "medium": "#f59e0b", "high": "#ef4444"}.get(risk, "#94a3b8")
    pct = int(score * 100)
    st.markdown(f"""
    <div style="margin: 0.6rem 0;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
            <span style="font-size:0.75rem;color:#64748b;">Grounding Confidence</span>
            <span style="font-family:'DM Mono',monospace;font-size:0.85rem;color:{color};font-weight:600;">{pct}%</span>
            <span style="font-size:0.75rem;color:{color};">● Hallucination Risk: <strong>{risk.upper()}</strong></span>
        </div>
        <div style="background:#1e1e2e;border-radius:4px;height:6px;">
            <div style="background:{color};width:{pct}%;height:100%;border-radius:4px;transition:width 0.5s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def cost_table(costs):
    if not costs:
        return
    df = pd.DataFrame(costs)
    df.columns = ["Stage", "Model", "Tokens", "Cost (₹)"]
    df["Cost (₹)"] = df["Cost (₹)"].apply(lambda x: f"₹{x:.4f}")
    st.dataframe(df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem;">
        <div style="font-size:1.1rem;font-weight:700;color:#e2e8f0;letter-spacing:-0.02em;">🧠 Enterprise AI</div>
        <div style="font-size:0.7rem;color:#475569;letter-spacing:0.05em;text-transform:uppercase;">Decision Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🔍 Query Engine",
        "📄 Documents",
        "🛡️ Governance Queue",
        "📋 Audit Log",
        "💰 FinOps Dashboard",
        "🧪 Evaluation",
        "🔭 Observability",
        "📊 System Health",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="section-label">Session</div>', unsafe_allow_html=True)
    user_id = st.text_input("User ID", value="user_cfo_001", label_visibility="collapsed")
    st.caption(f"👤 `{user_id}`   🔑 `sess_a3f8`")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.68rem;color:#374151;">
    <div style="color:#4b5563;font-weight:600;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.05em;">Services</div>
    <div>🟢 FastAPI Backend <code style="color:#374151">:8000</code></div>
    <div>🟢 Weaviate Cloud</div>
    <div>🟢 Neon PostgreSQL</div>
    <div>🟢 Langfuse Cloud</div>
    <div>🟢 Groq API</div>
    <div>🟢 Anthropic API</div>
    <div>🟢 OpenAI API</div>
    <div>🟢 Google AI API</div>
    <div>🟢 Cohere API</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: QUERY ENGINE
# ══════════════════════════════════════════════════════════════════════════════

if page == "🔍 Query Engine":
    st.markdown('<div class="hero-title">Query Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">RAG · PII Protection · Multi-Agent Debate · Cost Tracking</div>', unsafe_allow_html=True)

    # Query selector
    st.markdown('<div class="section-label">Select a demo query to simulate</div>', unsafe_allow_html=True)
    scenario = st.selectbox("", [
        "1️⃣  Simple — Headcount query (Haiku, ₹0.08, cache miss)",
        "2️⃣  Medium — Revenue analysis (Sonnet, ₹0.52)",
        "3️⃣  Complex + Debate — M&A Acquisition (Opus + 3 agents, ₹12.40)",
        "4️⃣  Cache HIT — Same question rephrased (₹0.00, 183ms)",
        "5️⃣  PII Detected — Aadhaar in query → Governance Paused",
    ], label_visibility="collapsed")

    qmap = {
        "1️⃣  Simple — Headcount query (Haiku, ₹0.08, cache miss)": "simple",
        "2️⃣  Medium — Revenue analysis (Sonnet, ₹0.52)": "medium",
        "3️⃣  Complex + Debate — M&A Acquisition (Opus + 3 agents, ₹12.40)": "complex",
        "4️⃣  Cache HIT — Same question rephrased (₹0.00, 183ms)": "cached",
        "5️⃣  PII Detected — Aadhaar in query → Governance Paused": "pii",
    }
    qt = qmap[scenario]
    q = QUERIES[qt]

    col_q, col_btn = st.columns([5, 1])
    with col_q:
        st.text_area("", value=q["text"], height=80, label_visibility="collapsed", key="qinput")
    with col_btn:
        force_debate = st.checkbox("Force Debate", value=(qt=="complex"))
        force_fresh  = st.checkbox("Skip Cache",   value=False)
        submit = st.button("🚀 Submit", type="primary", use_container_width=True)

    if submit:
        with st.status("⚙️ Processing...", expanded=True) as status:
            steps_display = [
                "🔒 Scanning for PII and sensitive content...",
                "🤖 Classifying query complexity and risk level...",
                "⚡ Checking semantic cache...",
                "🛡️ Running guardrail checks...",
                "✏️ Rewriting query for optimal retrieval...",
                "🔍 Hybrid search across document corpus...",
                "📊 Reranking with Cohere v3...",
                "🧠 Generating grounded answer...",
            ]
            if qt == "complex":
                steps_display += [
                    "🎭 Advocate building the case...",
                    "⚔️ Critic identifying risks...",
                    "⚖️ Judge synthesising both positions...",
                ]
            for step in steps_display:
                st.write(step)
                time.sleep(0.15)
            status.update(label="✅ Complete", state="complete", expanded=False)

    st.markdown("---")

    # Results header badges
    badges = complexity_badge(q["complexity"]) + " " + risk_badge(q["risk"]) + " " + cache_badge(q["cache_hit"])
    if q["debate"]:
        badges += ' <span class="badge badge-complex">🎭 Debate</span>'
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:1rem;">
        {badges}
        <span style="margin-left:auto;font-family:'DM Mono',monospace;font-size:0.75rem;color:#475569;">
            ⏱ {q['latency_ms']:,}ms &nbsp;|&nbsp; {model_tag(q['model'])} &nbsp;|&nbsp;
            <span class="cost-tag">₹{q['cost_inr']:.2f}</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # PII Governance Hold
    if qt == "pii":
        st.markdown("""
        <div class="card card-red">
            <div style="font-size:0.8rem;font-weight:600;color:#ef4444;margin-bottom:0.5rem;">🔒 PII DETECTED — QUERY HELD FOR GOVERNANCE REVIEW</div>
            <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.6rem;">The following entities were detected and redacted before any AI processing:</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f'<span class="pii-tag">AADHAAR_NUMBER</span> <span class="pii-tag">PERSON_NAME</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin:0.6rem 0;padding:0.8rem;background:#1a0a0a;border-radius:6px;border:1px solid #450a0a;">
            <div style="font-size:0.7rem;color:#7f1d1d;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:4px;">Redacted Query Sent for Review</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.78rem;color:#94a3b8;">{q['redacted']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.info(f"Governance ID: `{GOVERNANCE_QUEUE[0]['id']}` — Check the Governance Queue page to approve or reject.")

        st.markdown("---")
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("**15-Step Pipeline Execution**")
            render_pipeline_steps("pii")
        with col_r:
            st.markdown("**Cost Breakdown**")
            cost_table(q["costs"])
            st.markdown(f'<div style="margin-top:0.5rem;"><span class="cost-tag">Total: ₹{q["cost_inr"]:.4f}</span> <span style="font-size:0.72rem;color:#475569;">(only classification ran before governance pause)</span></div>', unsafe_allow_html=True)

    # Cache Hit
    elif qt == "cached":
        st.markdown("""
        <div class="card card-accent" style="border-left-color:#0f766e;">
            <div style="font-size:0.8rem;font-weight:600;color:#5eead4;margin-bottom:0.4rem;">⚡ SEMANTIC CACHE HIT — Zero AI Cost</div>
            <div style="font-size:0.78rem;color:#94a3b8;">Weaviate found a semantically identical previous query with certainty score <strong style="color:#5eead4;">0.947</strong> (threshold: 0.92). Answer served in <strong>183ms</strong> at ₹0.00.</div>
        </div>
        """, unsafe_allow_html=True)
        confidence_bar(q["confidence"], q["hal_risk"])
        st.markdown(q["answer"])
        st.markdown(f'<div style="margin-top:1rem;padding:0.6rem;background:#042f2e;border-radius:6px;border:1px solid #0f766e;font-size:0.75rem;color:#5eead4;">💡 Cache ROI: This query cost ₹0.00 vs ₹0.08 for a live request. At 1,243 cache hits/month → <strong>₹99.44 saved</strong></div>', unsafe_allow_html=True)

    # Normal query result
    else:
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown("**Answer**")
            confidence_bar(q["confidence"], q["hal_risk"])
            st.markdown(f'<div class="card" style="font-size:0.83rem;line-height:1.6;color:#cbd5e1;">{q["answer"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

            if q["sources"]:
                st.markdown("**Source Citations**")
                render_sources(q["sources"])

        with col_right:
            st.markdown("**15-Step Pipeline**")
            render_pipeline_steps(qt)

            st.markdown("**Cost Breakdown**")
            cost_table(q["costs"])
            total = sum(c["cost"] for c in q["costs"])
            st.markdown(f'<div style="text-align:right;margin-top:4px;"><span class="cost-tag">Total: ₹{total:.4f}</span></div>', unsafe_allow_html=True)

        # Debate transcript
        if q.get("debate") and q.get("advocate_output"):
            st.markdown("---")
            st.markdown("### 🎭 Three-Agent Debate Transcript")
            st.markdown(f'<div style="font-size:0.75rem;color:#64748b;margin-bottom:0.8rem;">3 AI models from 3 providers debating the answer — Advocate (Claude) → Critic (GPT-4o) → Judge (Gemini)</div>', unsafe_allow_html=True)

            with st.expander("✅ Advocate — claude-3-5-sonnet-20241022 (The Case For)"):
                st.markdown(f'<div style="font-size:0.82rem;color:#cbd5e1;line-height:1.6;">{q["advocate_output"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top:0.5rem;">{model_tag("claude-3-5-sonnet-20241022")} <span class="cost-tag" style="margin-left:8px;">₹3.012</span></div>', unsafe_allow_html=True)

            with st.expander("⚠️ Critic — gpt-4o (The Case Against)"):
                st.markdown(f'<div style="font-size:0.82rem;color:#cbd5e1;line-height:1.6;">{q["critic_output"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top:0.5rem;">{model_tag("gpt-4o")} <span class="cost-tag" style="margin-left:8px;">₹3.478</span></div>', unsafe_allow_html=True)

            with st.expander("⚖️ Judge — gemini-1.5-pro (Final Synthesis + Tools)", expanded=True):
                st.markdown("""
                <div style="margin-bottom:0.5rem;">
                    <span style="font-size:0.72rem;color:#f59e0b;">🔧 Tools called: </span>
                    <span class="model-tag" style="color:#f59e0b;border-color:#78350f;background:#1c0a00;">calculator</span>
                    <span class="model-tag" style="color:#f59e0b;border-color:#78350f;background:#1c0a00;margin-left:4px;">current_date</span>
                    <span class="model-tag" style="color:#f59e0b;border-color:#78350f;background:#1c0a00;margin-left:4px;">document_search</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f'<div style="font-size:0.82rem;color:#cbd5e1;line-height:1.6;">{q["answer"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="margin-top:0.5rem;">{model_tag("gemini/gemini-1.5-pro")} <span class="cost-tag" style="margin-left:8px;">₹3.600</span></div>', unsafe_allow_html=True)

    # Feedback
    st.markdown("---")
    fb1, fb2, _ = st.columns([1, 1, 5])
    if fb1.button("👍 Helpful"):
        st.success("Feedback recorded!")
    if fb2.button("👎 Not helpful"):
        st.info("Feedback recorded. We'll improve.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "📄 Documents":
    st.markdown('<div class="hero-title">Document Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">PDF · DOCX · XLSX · PPTX · CSV · URL ingestion via Unstructured</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📁 Upload File", "🌐 Upload URL", "📋 Indexed Documents"])

    with tab1:
        st.markdown("### Ingest a Document")
        st.file_uploader("Choose file", type=["pdf","docx","xlsx","pptx","csv","txt"], help="Max 50MB")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card card-accent" style="font-size:0.8rem;">
                <div style="color:#818cf8;font-weight:600;margin-bottom:6px;">What happens when you upload:</div>
                <div style="color:#94a3b8;line-height:1.8;">
                1. Unstructured extracts text by section<br>
                2. Text split into 512-char overlapping chunks (64 overlap)<br>
                3. Chunks vectorised via OpenAI text-embedding-ada-002<br>
                4. Stored in Weaviate DocumentChunk collection<br>
                5. Indexed for hybrid BM25 + vector search
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("⬆️ Simulate Ingest", type="primary"):
                with st.spinner("Processing Annual_Report_FY2024.pdf..."):
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress.progress(i+1)
                st.success("✅ **Annual_Report_FY2024.pdf** ingested → **94 chunks** created and indexed in Weaviate")
                st.markdown("""
                <div class="card card-green" style="font-size:0.78rem;">
                    <div style="color:#22c55e;font-weight:600;">Ingestion Summary</div>
                    <div style="color:#94a3b8;margin-top:4px;">
                    File: Annual_Report_FY2024.pdf &nbsp;·&nbsp; 4.2 MB &nbsp;·&nbsp; 47 pages<br>
                    Sections found: 12 &nbsp;·&nbsp; Chunks created: 94 &nbsp;·&nbsp; Vectors: 94<br>
                    Collection: DocumentChunk &nbsp;·&nbsp; Vectoriser: text2vec-openai<br>
                    Time: 8.3s &nbsp;·&nbsp; Status: <strong style="color:#22c55e;">READY</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        url_in = st.text_input("URL", placeholder="https://example.com/annual-report.pdf")
        if st.button("🌐 Ingest URL", type="primary"):
            with st.spinner("Fetching and ingesting..."):
                time.sleep(1.2)
            st.success("✅ URL ingested — 28 chunks created")

    with tab3:
        st.markdown(f"**{len(DOCUMENTS)} documents indexed** — {sum(d['chunks'] for d in DOCUMENTS)} total chunks in Weaviate")
        st.markdown("---")
        for doc in DOCUMENTS:
            col1, col2, col3, col4, col5 = st.columns([4, 1, 1, 1, 1])
            col1.markdown(f'<div style="font-size:0.83rem;color:#e2e8f0;font-weight:500;">📄 {doc["name"]}</div>', unsafe_allow_html=True)
            col2.markdown(f'<span style="font-size:0.72rem;color:#64748b;">{doc["type"]}</span>', unsafe_allow_html=True)
            col3.markdown(f'<span style="font-size:0.72rem;color:#64748b;">{doc["size"]}</span>', unsafe_allow_html=True)
            col4.markdown(f'<span style="font-size:0.72rem;color:#818cf8;">{doc["chunks"]} chunks</span>', unsafe_allow_html=True)
            col5.markdown(f'<span style="font-size:0.72rem;color:#22c55e;">✅ {doc["status"]}</span>', unsafe_allow_html=True)
            st.markdown('<div style="border-bottom:1px solid #1e1e2e;margin:4px 0;"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: GOVERNANCE QUEUE
# ══════════════════════════════════════════════════════════════════════════════

elif page == "🛡️ Governance Queue":
    st.markdown('<div class="hero-title">Governance Review Queue</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Human-in-the-loop compliance review for flagged queries</div>', unsafe_allow_html=True)

    reviewer = st.text_input("Reviewer ID", value="compliance_reviewer_01")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pending Review", "3", delta="↑ 1 new")
    m2.metric("Approved Today", "4")
    m3.metric("Rejected Today", "3")
    m4.metric("Avg Review Time", "6.2 min")

    st.markdown(f"### 📬 {len(GOVERNANCE_QUEUE)} queries awaiting review")
    st.markdown("---")

    for item in GOVERNANCE_QUEUE:
        risk_col = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}.get(item["risk"], "#94a3b8")
        st.markdown(f"""
        <div class="gov-pending">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                <span style="font-family:'DM Mono',monospace;font-size:0.72rem;color:#64748b;">ID: {item['id']}</span>
                <span class="badge badge-high" style="border-color:{risk_col};color:{risk_col};">Risk: {item['risk'].upper()}</span>
                {'<span class="pii-tag">PII DETECTED</span>' if item['pii'] else ''}
                <span style="margin-left:auto;font-size:0.72rem;color:#4b5563;">{item['time']}</span>
            </div>
            <div style="font-size:0.82rem;color:#e2e8f0;margin-bottom:6px;font-weight:500;">"{item['query'][:100]}{'...' if len(item['query'])>100 else ''}"</div>
            <div style="font-size:0.72rem;color:#64748b;">Triggered: <code style="color:#f59e0b;background:#1c0a00;padding:1px 5px;border-radius:3px;">{item['rule']}</code></div>
            {f'<div style="margin-top:4px;font-size:0.72rem;color:#64748b;">PII Types: {" ".join([f"<span class=pii-tag>{p}</span>" for p in item["pii_types"]])}</div>' if item['pii'] else ''}
        </div>
        """, unsafe_allow_html=True)

        note = st.text_input("Note", placeholder="Reason for decision...", key=f"note_{item['id']}", label_visibility="collapsed")
        c1, c2, _ = st.columns([1, 1, 4])
        if c1.button("✅ Approve", key=f"app_{item['id']}", type="primary"):
            st.success(f"Approved — `{item['id']}`")
        if c2.button("❌ Reject", key=f"rej_{item['id']}"):
            st.warning(f"Rejected — query will not be processed")
        st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AUDIT LOG
# ══════════════════════════════════════════════════════════════════════════════

elif page == "📋 Audit Log":
    st.markdown('<div class="hero-title">Governance Audit Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Immutable record of all compliance decisions</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    approved = sum(1 for e in AUDIT_LOG if e["action"] == "approved")
    rejected = sum(1 for e in AUDIT_LOG if e["action"] == "rejected")
    m1.metric("Total Decisions", len(AUDIT_LOG))
    m2.metric("Approved", approved)
    m3.metric("Rejected", rejected)
    m4.metric("Approval Rate", f"{approved/len(AUDIT_LOG)*100:.0f}%")

    filter_act = st.selectbox("Filter", ["All", "approved", "rejected"])
    shown = [e for e in AUDIT_LOG if filter_act == "All" or e["action"] == filter_act]

    df = pd.DataFrame([{
        "Timestamp": e["time"],
        "Action": "✅ APPROVED" if e["action"] == "approved" else "❌ REJECTED",
        "Query Preview": e["query"][:70] + "...",
        "Risk": e["risk"].upper(),
        "Rule": e["rule"],
        "Reviewer": e["reviewer"],
        "Note": e["note"][:60],
    } for e in shown])
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("📥 Export CSV", df.to_csv(index=False), "audit_log.csv", "text/csv")

    st.markdown("---")
    for e in shown[:3]:
        icon = "✅" if e["action"] == "approved" else "❌"
        with st.expander(f"{icon} {e['time']} | {e['reviewer']} | Risk: {e['risk'].upper()}"):
            st.markdown(f"**Query:** {e['query']}")
            st.markdown(f"**Decision:** `{e['action'].upper()}`")
            st.markdown(f"**Rule:** `{e['rule']}`")
            st.markdown(f"**Note:** {e['note']}")
            st.caption(f"Governance ID: `{e['id']}`")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FINOPS
# ══════════════════════════════════════════════════════════════════════════════

elif page == "💰 FinOps Dashboard":
    st.markdown('<div class="hero-title">FinOps Cost Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Real-time AI spend by model · complexity · cache savings</div>', unsafe_allow_html=True)

    days = st.selectbox("Range", [7, 14, 30, 90], index=2, format_func=lambda x: f"Last {x} days")

    models, dates, daily = make_finops_data()
    total_cost = sum(models.values())
    total_q = 2491
    cache_hits = 1243
    cache_rate = cache_hits / total_q
    avg_cost = total_cost / total_q

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Cost (INR)", f"₹{total_cost:.2f}")
    m2.metric("Total Queries", f"{total_q:,}")
    m3.metric("Avg Cost / Query", f"₹{avg_cost:.4f}")
    m4.metric("Cache Hit Rate", f"{cache_rate*100:.1f}%")
    m5.metric("Saved by Cache", f"₹{cache_hits * avg_cost:.2f}")

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        df_m = pd.DataFrame(list(models.items()), columns=["Model", "Cost (₹)"]).sort_values("Cost (₹)", ascending=False)
        fig = px.bar(df_m, x="Model", y="Cost (₹)", title="Cost by AI Model",
                     color="Model", color_discrete_sequence=["#6366f1","#8b5cf6","#a855f7","#3b82f6","#06b6d4","#22c55e"])
        fig.update_layout(paper_bgcolor="#0a0a0f", plot_bgcolor="#111118", font_color="#94a3b8",
                          showlegend=False, height=320, title_font_color="#e2e8f0")
        fig.update_xaxes(tickangle=20, tickfont_size=9)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        df_d = pd.DataFrame({"date": dates[-days:], "cost": daily[-days:]})
        fig2 = px.line(df_d, x="date", y="cost", title=f"Daily Spend — Last {days} Days", markers=True)
        fig2.update_traces(line_color="#6366f1", marker_color="#818cf8")
        fig2.update_layout(paper_bgcolor="#0a0a0f", plot_bgcolor="#111118", font_color="#94a3b8",
                           height=320, title_font_color="#e2e8f0")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig3 = px.pie(values=list(models.values()), names=list(models.keys()),
                      title="Spend Distribution", hole=0.45,
                      color_discrete_sequence=["#6366f1","#8b5cf6","#a855f7","#3b82f6","#06b6d4","#22c55e"])
        fig3.update_layout(paper_bgcolor="#0a0a0f", font_color="#94a3b8", height=300, title_font_color="#e2e8f0")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=cache_rate * 100,
            title={"text": "Cache Hit Rate (%)", "font": {"color": "#94a3b8"}},
            delta={"reference": 30, "valueformat": ".1f"},
            number={"font": {"color": "#5eead4"}, "suffix": "%"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#475569"},
                "bar": {"color": "#5eead4"},
                "bgcolor": "#111118",
                "steps": [
                    {"range": [0, 30], "color": "#1a0a0a"},
                    {"range": [30, 60], "color": "#1c1000"},
                    {"range": [60, 100], "color": "#052e16"},
                ],
            }
        ))
        gauge.update_layout(paper_bgcolor="#0a0a0f", font_color="#94a3b8", height=300)
        st.plotly_chart(gauge, use_container_width=True)

    st.markdown("#### 💸 Top 5 Most Expensive Queries")
    top_q = pd.DataFrame([
        {"Query": "Should we acquire TechStartup XYZ...", "Cost (₹)": 12.40, "Model": "opus+debate", "Complexity": "complex"},
        {"Query": "Build a 3-year financial model for...", "Cost (₹)": 11.82, "Model": "opus+debate", "Complexity": "complex"},
        {"Query": "What are the strategic implications...", "Cost (₹)": 10.91, "Model": "opus+debate", "Complexity": "complex"},
        {"Query": "Analyse Q3 and Q4 revenue trends...", "Cost (₹)": 0.52, "Model": "sonnet", "Complexity": "medium"},
        {"Query": "What is the investment timeline?", "Cost (₹)": 0.49, "Model": "sonnet", "Complexity": "medium"},
    ])
    st.dataframe(top_q, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EVALUATION
# ══════════════════════════════════════════════════════════════════════════════

elif page == "🧪 Evaluation":
    st.markdown('<div class="hero-title">RAG Evaluation Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">TruLens RAG Triad · Answer Relevance · Context Relevance · Groundedness</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🚀 Run Evaluation", "📊 History & Benchmarks"])

    with tab1:
        st.markdown("### Evaluation Configuration")
        st.markdown("""
        <div class="card card-blue" style="font-size:0.8rem;color:#94a3b8;">
        Runs <strong style="color:#93c5fd;">10 default queries</strong> through the full RAG pipeline and scores each using TruLens feedback functions backed by GPT-4o-mini.<br>
        Metrics: <strong>Answer Relevance</strong> (does the answer address the question?) · <strong>Context Relevance</strong> (did retrieval find useful chunks?) · <strong>Groundedness</strong> (is the answer traceable to documents?)
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Run Evaluation", type="primary"):
            with st.spinner("Running TruLens evaluation across 10 queries..."):
                prog = st.progress(0)
                for i in range(10):
                    time.sleep(0.2)
                    prog.progress((i+1)*10)
            st.success("✅ Evaluation complete — 10 queries scored")

        st.markdown("---")
        st.markdown("### Latest Run Results")

        avg_ar = sum(EVAL_DATA["answer_relevance"]) / 10
        avg_cr = sum(EVAL_DATA["context_relevance"]) / 10
        avg_gr = sum(EVAL_DATA["groundedness"]) / 10

        col1, col2, col3 = st.columns(3)
        for col, val, label, color in [
            (col1, avg_ar, "Answer Relevance", "#6366f1"),
            (col2, avg_cr, "Context Relevance", "#3b82f6"),
            (col3, avg_gr, "Groundedness", "#22c55e"),
        ]:
            with col:
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=val * 100,
                    title={"text": label, "font": {"color": "#94a3b8", "size": 13}},
                    number={"font": {"color": color}, "suffix": "%", "valueformat": ".1f"},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": "#475569"},
                        "bar": {"color": color},
                        "bgcolor": "#111118",
                        "steps": [
                            {"range": [0, 40], "color": "#1a0a0a"},
                            {"range": [40, 70], "color": "#1c1000"},
                            {"range": [70, 100], "color": "#052e16"},
                        ],
                        "threshold": {"line": {"color": "#22c55e", "width": 3}, "thickness": 0.75, "value": 75},
                    }
                ))
                fig.update_layout(paper_bgcolor="#0a0a0f", height=230, margin=dict(t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Per-Query Breakdown")
        df_eval = pd.DataFrame({
            "Query": [q[:55]+"..." if len(q)>55 else q for q in EVAL_DATA["queries"]],
            "Ans Relevance": EVAL_DATA["answer_relevance"],
            "Ctx Relevance": EVAL_DATA["context_relevance"],
            "Groundedness": EVAL_DATA["groundedness"],
        })
        st.dataframe(df_eval, use_container_width=True, hide_index=True)

        worst_idx = EVAL_DATA["groundedness"].index(min(EVAL_DATA["groundedness"]))
        st.markdown("#### ⚠️ Lowest Groundedness Query")
        st.warning(f"""**Query:** {EVAL_DATA['queries'][worst_idx]}
Groundedness: {EVAL_DATA['groundedness'][worst_idx]:.3f} | Context Relevance: {EVAL_DATA['context_relevance'][worst_idx]:.3f}
**Why:** Document corpus lacks a dedicated section on this topic. Retrieval brings adjacent chunks with low relevance.""")

    with tab2:
        st.markdown("### Benchmark: With vs Without Reranking")
        bench = pd.DataFrame({
            "Metric": ["Context Relevance", "Groundedness", "Answer Relevance", "Top-1 Chunk Precision"],
            "Without Reranking": [0.701, 0.763, 0.831, 0.61],
            "With Cohere Reranking": [0.791, 0.823, 0.847, 0.79],
            "Improvement": ["+12.8%", "+7.9%", "+1.9%", "+29.5%"],
        })
        st.dataframe(bench, use_container_width=True, hide_index=True)

        st.markdown("### Debate Quality: Single Model vs Three-Agent")
        debate_bench = pd.DataFrame({
            "Dimension": ["Identifies all key risks", "Considers opposing views", "Calculation accuracy", "Actionability", "Overall confidence"],
            "Single Model (Opus)": [3.4, 2.8, 3.9, 3.7, 3.5],
            "Three-Agent Debate": [4.6, 4.8, 4.7, 4.4, 4.5],
            "Improvement": ["+35.3%", "+71.4%", "+20.5%", "+18.9%", "+28.6%"],
        })
        st.dataframe(debate_bench, use_container_width=True, hide_index=True)
        st.info("📊 Scores rated 1–5 by 3 independent reviewers across 20 complex queries. Biggest gain: **+71.4%** in considering opposing perspectives.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OBSERVABILITY
# ══════════════════════════════════════════════════════════════════════════════

elif page == "🔭 Observability":
    st.markdown('<div class="hero-title">Observability Stack</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Langfuse LLM Traces · Prometheus Metrics · Grafana Panels</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔭 Langfuse Traces", "📈 Prometheus Metrics", "📊 Grafana Panels"])

    with tab1:
        st.markdown("### LLM Traces — Last 5 Queries")
        st.markdown("""
        <div class="card" style="font-size:0.75rem;color:#64748b;margin-bottom:1rem;">
        Every AI call is traced in <strong style="color:#818cf8;">Langfuse Cloud</strong> with full input/output, token counts, cost, and latency.
        In production, go to <code>cloud.langfuse.com</code> to see all traces.
        </div>
        """, unsafe_allow_html=True)

        for t in LANGFUSE_TRACES:
            status_color = {"success": "#22c55e", "cache_hit": "#5eead4", "governance_paused": "#ef4444"}.get(t["status"], "#94a3b8")
            status_icon = {"success": "✅", "cache_hit": "⚡", "governance_paused": "🔒"}.get(t["status"], "●")
            st.markdown(f"""
            <div class="card" style="margin-bottom:0.5rem;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    <span style="font-family:'DM Mono',monospace;font-size:0.70rem;color:#475569;">{t['id']}</span>
                    <span style="color:{status_color};font-size:0.75rem;">{status_icon} {t['status'].replace('_',' ').upper()}</span>
                    <span style="margin-left:auto;" class="model-tag">{t['model']}</span>
                </div>
                <div style="font-size:0.82rem;color:#e2e8f0;margin-bottom:6px;">"{t['query']}"</div>
                <div style="display:flex;gap:16px;font-size:0.72rem;color:#64748b;">
                    <span>🔢 <strong style="color:#818cf8;">{t['tokens']:,}</strong> tokens</span>
                    <span>💰 <strong class="cost-tag">{t['cost']}</strong></span>
                    <span>⏱ <strong style="color:#94a3b8;">{t['latency']}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Trace Breakdown — Complex Debate Query")
        st.markdown("""
        <div class="card" style="font-size:0.75rem;">
        """, unsafe_allow_html=True)
        trace_lines = [
            ("span", "pii_scan", "83ms", "0 entities"),
            ("span", "classification → groq/llama3-70b", "312ms", "complexity=complex, risk=high"),
            ("span", "cache_lookup → SemanticCache miss", "91ms", "certainty=0.00"),
            ("span", "guardrail_check → PASS", "12ms", "rules=[]"),
            ("span", "query_rewrite → groq/llama3-70b", "281ms", "462 tokens"),
            ("span", "hybrid_search → Weaviate", "143ms", "10 chunks retrieved"),
            ("span", "rerank → Cohere Rerank v3", "418ms", "top 5 returned"),
            ("generation", "rag_generation → claude-3-opus", "8,700ms", "2580 tokens · ₹2.30"),
            ("generation", "advocate → claude-3-5-sonnet", "12,400ms", "2840 tokens · ₹3.01"),
            ("generation", "critic → gpt-4o", "13,100ms", "2910 tokens · ₹3.48"),
            ("tool_call", "judge.calculator('200/40')", "2ms", "= 5.0"),
            ("tool_call", "judge.current_date()", "1ms", "2024-12-19"),
            ("tool_call", "judge.document_search('customer concentration')", "143ms", "3 chunks"),
            ("generation", "judge → gemini-1.5-pro", "15,800ms", "3200 tokens · ₹3.60"),
            ("span", "confidence_score", "8ms", "0.71"),
            ("span", "db_write → PostgreSQL", "68ms", "query_logs + debate_records"),
            ("span", "cache_store → SemanticCache", "82ms", "stored"),
        ]
        for kind, name, timing, detail in trace_lines:
            kind_color = {"generation": "#818cf8", "tool_call": "#f59e0b", "span": "#475569"}.get(kind, "#475569")
            indent = "margin-left:16px;" if kind in ("tool_call",) else ""
            st.markdown(f'<div class="trace-line" style="{indent}"><span style="color:{kind_color};min-width:80px;display:inline-block;">[{kind}]</span> <span style="color:#e2e8f0;">{name}</span> <span style="float:right;color:#374151;">{timing} · {detail}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### Live Prometheus Metrics")
        st.markdown('<div style="font-size:0.75rem;color:#64748b;margin-bottom:0.8rem;">Exposed at <code>/metrics</code> endpoint · scraped by Grafana Cloud every 15s</div>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Requests", "2,491")
        m2.metric("Cache Hit Rate", "49.9%")
        m3.metric("Total Cost (INR)", "₹192.67")
        m4.metric("Pending Governance", "3")

        st.code(PROMETHEUS_METRICS, language="text")

    with tab3:
        st.markdown("### Grafana Dashboard Panels")
        st.markdown('<div style="font-size:0.75rem;color:#64748b;margin-bottom:1rem;">8 panels in <code>docs/grafana_dashboard.json</code> — import at grafana.com</div>', unsafe_allow_html=True)

        panels_data = {
            "Total Queries": 2491,
            "Debates Triggered": 89,
            "Governance Pending": 3,
            "Errors (all stages)": 4,
        }
        cols = st.columns(4)
        colors = ["#6366f1", "#a855f7", "#ef4444", "#f59e0b"]
        for i, (k, v) in enumerate(panels_data.items()):
            with cols[i]:
                st.markdown(f"""
                <div class="card" style="text-align:center;border-top:2px solid {colors[i]};">
                    <div class="metric-number">{v}</div>
                    <div class="metric-label">{k}</div>
                </div>
                """, unsafe_allow_html=True)

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("**Request Rate by Complexity (rate[5m])**")
            df_rate = pd.DataFrame({
                "time": pd.date_range(end=datetime.now(), periods=20, freq="5min"),
                "simple": [random.uniform(0.8, 1.4) for _ in range(20)],
                "medium": [random.uniform(0.2, 0.6) for _ in range(20)],
                "complex": [random.uniform(0.05, 0.15) for _ in range(20)],
            })
            fig = px.line(df_rate, x="time", y=["simple","medium","complex"],
                         color_discrete_map={"simple":"#22c55e","medium":"#f59e0b","complex":"#ef4444"})
            fig.update_layout(paper_bgcolor="#0a0a0f", plot_bgcolor="#111118", font_color="#94a3b8",
                              height=260, legend_title_text="Complexity", title_font_color="#e2e8f0",
                              legend=dict(bgcolor="#0a0a0f"))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("**P95 Latency by Complexity (seconds)**")
            df_lat = pd.DataFrame({
                "time": pd.date_range(end=datetime.now(), periods=20, freq="5min"),
                "simple_p95": [random.uniform(2.8, 3.4) for _ in range(20)],
                "medium_p95": [random.uniform(5.8, 7.2) for _ in range(20)],
                "complex_p95": [random.uniform(68, 82) for _ in range(20)],
            })
            fig2 = px.line(df_lat, x="time", y=["simple_p95","medium_p95","complex_p95"],
                          color_discrete_map={"simple_p95":"#22c55e","medium_p95":"#f59e0b","complex_p95":"#ef4444"})
            fig2.update_layout(paper_bgcolor="#0a0a0f", plot_bgcolor="#111118", font_color="#94a3b8",
                               height=260, legend=dict(bgcolor="#0a0a0f"))
            st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SYSTEM HEALTH
# ══════════════════════════════════════════════════════════════════════════════

elif page == "📊 System Health":
    st.markdown('<div class="hero-title">System Health</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Service status · API endpoints · Configuration</div>', unsafe_allow_html=True)

    st.markdown("### Service Status")
    services = [
        ("FastAPI Backend", ":8000", "healthy", "v1.0.0", "#22c55e"),
        ("Weaviate Cloud", "cloud.weaviate.io", "connected", "2 collections · 312 objects", "#22c55e"),
        ("Neon PostgreSQL", "us-east-2", "connected", "8 tables · 2,491 rows", "#22c55e"),
        ("Langfuse Cloud", "cloud.langfuse.com", "connected", "2,491 traces stored", "#22c55e"),
        ("Groq API", "api.groq.com", "connected", "llama3-70b-8192", "#22c55e"),
        ("Anthropic API", "api.anthropic.com", "connected", "claude-3-haiku / sonnet / opus", "#22c55e"),
        ("OpenAI API", "api.openai.com", "connected", "gpt-4o + text-embedding-ada-002", "#22c55e"),
        ("Google AI", "generativelanguage.googleapis.com", "connected", "gemini-1.5-pro", "#22c55e"),
        ("Cohere API", "api.cohere.com", "connected", "rerank-english-v3.0", "#22c55e"),
    ]
    for name, endpoint, status, detail, color in services:
        col1, col2, col3, col4 = st.columns([2, 2, 1, 3])
        col1.markdown(f'<span style="font-size:0.83rem;color:#e2e8f0;font-weight:500;">{name}</span>', unsafe_allow_html=True)
        col2.markdown(f'<span style="font-family:DM Mono,monospace;font-size:0.70rem;color:#475569;">{endpoint}</span>', unsafe_allow_html=True)
        col3.markdown(f'<span style="font-size:0.72rem;color:{color};">● {status}</span>', unsafe_allow_html=True)
        col4.markdown(f'<span style="font-size:0.72rem;color:#64748b;">{detail}</span>', unsafe_allow_html=True)
        st.markdown('<div style="border-bottom:1px solid #1e1e2e;margin:3px 0;"></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### API Endpoints")
    endpoints = [
        ("POST", "/query", "Submit query — runs full 15-step pipeline"),
        ("GET",  "/query/history", "Query history for a user"),
        ("GET",  "/query/{id}", "Full detail of one query"),
        ("POST", "/documents/upload", "Upload and ingest a document"),
        ("POST", "/documents/upload-url", "Ingest from a URL"),
        ("GET",  "/documents/list", "List all documents for a user"),
        ("DELETE","/documents/{id}", "Delete document from Weaviate + PostgreSQL"),
        ("GET",  "/governance/pending", "All pending governance items"),
        ("POST", "/governance/action", "Approve or reject a governance item"),
        ("GET",  "/governance/audit", "Full audit log"),
        ("GET",  "/finops/summary", "Cost aggregation dashboard data"),
        ("GET",  "/memory/{user_id}", "Get stored user memories"),
        ("DELETE","/memory/{user_id}", "Clear user memories"),
        ("POST", "/eval/run", "Run TruLens RAG Triad evaluation"),
        ("GET",  "/eval/history", "Past evaluation runs"),
        ("POST", "/feedback", "Submit thumbs up/down feedback"),
        ("GET",  "/health", "Health check"),
        ("GET",  "/metrics", "Prometheus metrics"),
    ]
    for method, path, desc in endpoints:
        color = {"POST": "#22c55e", "GET": "#3b82f6", "DELETE": "#ef4444"}.get(method, "#94a3b8")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:5px 0;border-bottom:1px solid #111118;">
            <span style="font-family:DM Mono,monospace;font-size:0.70rem;color:{color};min-width:48px;font-weight:600;">{method}</span>
            <span style="font-family:DM Mono,monospace;font-size:0.75rem;color:#818cf8;min-width:240px;">{path}</span>
            <span style="font-size:0.75rem;color:#64748b;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Database Tables")
    tables = [
        ("query_logs", "2,491 rows", "Every query — cost, model, tokens, answer, sources, confidence"),
        ("governance_records", "156 rows", "PII/high-risk flags — status, reviewer, decision"),
        ("debate_records", "89 rows", "Full advocate/critic/judge outputs per debate"),
        ("document_records", "5 rows", "Uploaded document metadata"),
        ("user_memories", "38 rows", "Extracted role/department/focus per user"),
        ("feedback_records", "312 rows", "Thumbs up/down per query"),
        ("evaluation_runs", "4 rows", "TruLens evaluation history"),
        ("prompt_versions", "0 rows", "Prompt version management"),
    ]
    for name, count, desc in tables:
        col1, col2, col3 = st.columns([2, 1, 4])
        col1.markdown(f'<span style="font-family:DM Mono,monospace;font-size:0.78rem;color:#818cf8;">{name}</span>', unsafe_allow_html=True)
        col2.markdown(f'<span style="font-size:0.72rem;color:#f59e0b;">{count}</span>', unsafe_allow_html=True)
        col3.markdown(f'<span style="font-size:0.72rem;color:#64748b;">{desc}</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"📖 **API Docs:** [Swagger UI](http://localhost:8000/docs) | [ReDoc](http://localhost:8000/redoc)")
