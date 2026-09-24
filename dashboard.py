import streamlit as st
import pandas as pd
import altair as alt

# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="Payer Revenue Integrity Command Center",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("outputs/revenue_integrity_exceptions.csv")

df = load_data()

# =========================================================
# KPI METRICS
# =========================================================

providers_requiring_review = df["provider_id"].nunique()
denied_claims = int(df["denied_claim_count"].sum())
billed_charges_at_risk = df["potential_revenue_at_risk"].sum()
exception_flags = int(df["issue_count"].sum())

# =========================================================
# CLEAN EXECUTIVE-FACING LABELS
# =========================================================

exception_names = {
    "SPECIALTY_MISMATCH": "Specialty Mismatch",
    "PENDING_ENROLLMENT": "Pending Enrollment",
    "TERMINATED_ENROLLMENT": "Terminated Enrollment",
    "CLOSED_PANEL": "Closed Panel",
    "INACTIVE_LOCATION": "Inactive Location",
    "INACTIVE_PROVIDER_ACTIVE_ENROLLMENT":
        "Inactive Provider / Active Enrollment"
}

def clean_exception_label(value):
    issues = str(value).split("|")

    cleaned = []

    for issue in issues:
        issue = issue.strip()

        cleaned.append(
            exception_names.get(
                issue,
                issue.replace("_", " ").title()
            )
        )

    return " | ".join(cleaned)

df["executive_exception"] = (
    df["exception_type"]
    .apply(clean_exception_label)
)

# =========================================================
# GLOBAL STYLE
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* HERO */

.command-header {
    padding: 34px 40px;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #0B1F33 0%,
        #123B5D 52%,
        #146C7E 100%
    );
    margin-bottom: 25px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.18);
}

.eyebrow {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #7FDBDA;
    margin-bottom: 8px;
}

.command-title {
    font-size: 39px;
    font-weight: 800;
    color: white;
    line-height: 1.15;
}

.command-subtitle {
    font-size: 16px;
    color: #D7E7EF;
    margin-top: 11px;
    margin-bottom: 25px;
}

.risk-label {
    font-size: 12px;
    font-weight: 700;
    color: #AFC8D6;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.risk-value {
    font-size: 44px;
    font-weight: 800;
    color: white;
    margin-top: 3px;
    line-height: 1;
}

.risk-note {
    font-size: 12px;
    color: #AFC8D6;
    margin-top: 9px;
}

/* KPI CARDS */

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 8px;
    margin-bottom: 35px;
}

.kpi-card {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 15px;
    padding: 21px 22px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.kpi-label {
    color: #64748B;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .7px;
}

.kpi-number {
    color: #0B1F33;
    font-size: 34px;
    font-weight: 800;
    margin-top: 8px;
    line-height: 1;
}

.kpi-detail {
    color: #64748B;
    font-size: 12px;
    margin-top: 10px;
}

.kpi-primary {
    border-top: 4px solid #123B5D;
}

.kpi-alert {
    border-top: 4px solid #C65D3A;
}

.kpi-watch {
    border-top: 4px solid #D99A32;
}

.kpi-info {
    border-top: 4px solid #146C7E;
}

/* SECTION LABELS */

.section-label {
    color: #146C7E;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 14px;
    margin-bottom: 3px;
}

/* ACTION BADGE */

.priority-badge {
    display: inline-block;
    background: #FDECEC;
    color: #A63D2F;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# COMMAND CENTER HERO
# =========================================================

hero_html = (
    f'<div class="command-header">'
    f'<div class="eyebrow">'
    f'HEALTHCARE ANALYTICS • REVENUE INTEGRITY'
    f'</div>'
    f'<div class="command-title">'
    f'Payer Revenue Integrity Command Center'
    f'</div>'
    f'<div class="command-subtitle">'
    f'Provider configuration intelligence for identifying '
    f'reimbursement exposure before discrepancies become recurring '
    f'revenue-cycle problems.'
    f'</div>'
    f'<div class="risk-label">'
    f'Synthetic Billed Charges Potentially at Risk'
    f'</div>'
    f'<div class="risk-value">'
    f'${billed_charges_at_risk:,.0f}'
    f'</div>'
    f'<div class="risk-note">'
    f'Associated with denied claims linked to provider configuration exceptions'
    f'</div>'
    f'</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)

# =========================================================
# EXECUTIVE KPI CARDS
# =========================================================

kpi_html = (
    f'<div class="kpi-grid">'

    f'<div class="kpi-card kpi-primary">'
    f'<div class="kpi-label">Providers Requiring Review</div>'
    f'<div class="kpi-number">{providers_requiring_review}</div>'
    f'<div class="kpi-detail">Provider configurations flagged</div>'
    f'</div>'

    f'<div class="kpi-card kpi-alert">'
    f'<div class="kpi-label">Denied Claims</div>'
    f'<div class="kpi-number">{denied_claims}</div>'
    f'<div class="kpi-detail">Associated with identified exceptions</div>'
    f'</div>'

    f'<div class="kpi-card kpi-watch">'
    f'<div class="kpi-label">Billed Charges at Risk</div>'
    f'<div class="kpi-number">${billed_charges_at_risk:,.0f}</div>'
    f'<div class="kpi-detail">Synthetic denied billed charges</div>'
    f'</div>'

    f'<div class="kpi-card kpi-info">'
    f'<div class="kpi-label">Exception Flags</div>'
    f'<div class="kpi-number">{exception_flags}</div>'
    f'<div class="kpi-detail">Across configuration categories</div>'
    f'</div>'

    f'</div>'
)

st.markdown(
    kpi_html,
    unsafe_allow_html=True
)

# =========================================================
# FINANCIAL EXPOSURE
# =========================================================

st.markdown(
    '<div class="section-label">FINANCIAL EXPOSURE</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Revenue Exposure by Provider"
)

st.caption(
    "Providers ranked by synthetic billed charges associated with "
    "denied claims and identified configuration exceptions."
)

risk_by_provider = (
    df[
        [
            "provider_id",
            "provider_name",
            "potential_revenue_at_risk"
        ]
    ]
    .sort_values(
        "potential_revenue_at_risk",
        ascending=False
    )
)

risk_chart = (
    alt.Chart(risk_by_provider)
    .mark_bar(
        cornerRadiusEnd=4
    )
    .encode(
        y=alt.Y(
            "provider_id:N",
            sort="-x",
            title="Provider"
        ),
        x=alt.X(
            "potential_revenue_at_risk:Q",
            title="Billed Charges Potentially at Risk"
        ),
        tooltip=[
            alt.Tooltip(
                "provider_id:N",
                title="Provider ID"
            ),
            alt.Tooltip(
                "provider_name:N",
                title="Provider"
            ),
            alt.Tooltip(
                "potential_revenue_at_risk:Q",
                title="Billed Charges at Risk",
                format="$,.0f"
            )
        ]
    )
    .properties(
        height=320
    )
)

st.altair_chart(
    risk_chart,
    use_container_width=True
)

# =========================================================
# PRIORITY REVIEW QUEUE
# =========================================================

st.markdown(
    '<div class="section-label">ACTION CENTER</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Priority Review Queue"
)

st.caption(
    "Provider configurations prioritized by synthetic billed charges "
    "associated with denied claims."
)

st.markdown(
    '<div class="priority-badge">'
    '● CONFIGURATION REVIEW REQUIRED'
    '</div>',
    unsafe_allow_html=True
)

priority_queue = df[
    [
        "provider_id",
        "provider_name",
        "payer_name",
        "line_of_business",
        "executive_exception",
        "denied_claim_count",
        "potential_revenue_at_risk"
    ]
].copy()

priority_queue = priority_queue.sort_values(
    "potential_revenue_at_risk",
    ascending=False
)

priority_queue = priority_queue.rename(
    columns={
        "provider_id":
            "Provider ID",

        "provider_name":
            "Provider",

        "payer_name":
            "Payer",

        "line_of_business":
            "Line of Business",

        "executive_exception":
            "Configuration Exception",

        "denied_claim_count":
            "Denied Claims",

        "potential_revenue_at_risk":
            "Billed Charges at Risk"
    }
)

priority_queue["Billed Charges at Risk"] = (
    priority_queue["Billed Charges at Risk"]
    .map(
        lambda x: f"${x:,.0f}"
    )
)

st.dataframe(
    priority_queue,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# ANALYTICS ARCHITECTURE
# =========================================================

st.markdown(
    '<div class="section-label">DATA PIPELINE</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Analytics Architecture"
)

st.markdown(
    "**Synthetic Healthcare Data** → "
    "**Python Validation** → "
    "**Snowflake Warehouse** → "
    "**SQL Reconciliation** → "
    "**dbt Transformations & Testing** → "
    "**Revenue Integrity Analytics** → "
    "**Streamlit Command Center**"
)

# =========================================================
# PORTFOLIO DISCLOSURE
# =========================================================

st.divider()

st.caption(
    "Portfolio demonstration using entirely synthetic healthcare data. "
    "Dollar amounts represent synthetic billed charges associated with "
    "denied claims and are not recovered revenue, confirmed lost revenue, "
    "or guaranteed recoverable revenue."
)