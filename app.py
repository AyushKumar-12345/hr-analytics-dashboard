import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- PAGE SETUP ---
st.set_page_config(
    page_title="HR Workforce Intelligence",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN EXECUTIVE DARK THEME CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .stApp {
        background-color: #0B0F19;
        background-image: 
            radial-gradient(circle at 10% 8%, rgba(14, 116, 144, 0.18) 0%, transparent 35%),
            radial-gradient(circle at 90% 90%, rgba(194, 65, 12, 0.12) 0%, transparent 40%);
        color: #F8FAFC;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px;
    }

    /* Branding Header */
    .brand-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #00E5FF;
        margin: 0;
        text-shadow: 0 0 24px rgba(0, 229, 255, 0.25);
    }
    .brand-title span {
        color: #FFFFFF;
    }
    .brand-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-top: 4px;
        margin-bottom: 22px;
        font-weight: 400;
    }

    /* Filter Ribbon */
    .filter-ribbon {
        background: rgba(18, 24, 38, 0.85);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px 8px 20px;
        margin-bottom: 24px;
    }

    /* Dropdown UI */
    div[data-baseweb="select"] > div {
        background-color: #121826 !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: #151D2E !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        z-index: 999999 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: rgba(18, 24, 38, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-left: 3px solid #00E5FF;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card.alert {
        border-left: 3px solid #FF6D00;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #94A3B8;
    }
    .kpi-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 6px;
        line-height: 1.1;
    }
    .kpi-pill {
        display: inline-block;
        font-size: 0.72rem;
        padding: 2px 8px;
        border-radius: 9999px;
        background-color: rgba(0, 229, 255, 0.14);
        color: #00E5FF;
        font-weight: 600;
        margin-top: 8px;
    }
    .kpi-pill.alert {
        background-color: rgba(255, 109, 0, 0.14);
        color: #FF6D00;
    }

    /* Chart Containers */
    .panel-container {
        background: rgba(18, 24, 38, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 18px 20px 10px 20px;
        margin-bottom: 20px;
    }
    .panel-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    .panel-caption {
        font-size: 0.8rem;
        color: #64748B;
        margin-top: 2px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD CLEANED DATASET ---
@st.cache_data
def load_hr_data():
    base = Path(__file__).resolve().parent
    file_path = base / "HR_Data_cleaned.csv"
    return pd.read_csv(file_path)

try:
    df = load_hr_data()
except Exception as e:
    st.error(f"Error loading HR_Data_cleaned.csv: {e}")
    st.stop()

# --- TOP HEADER ---
st.markdown("""
    <div>
        <h1 class="brand-title">WORKFORCE <span>INTELLIGENCE</span></h1>
        <p class="brand-subtitle">Strategic Human Capital Analytics & Employee Attrition Diagnostics</p>
    </div>
""", unsafe_allow_html=True)

# --- TOP FILTER RIBBON ---
with st.container():
    st.markdown('<div class="filter-ribbon">', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns([1.3, 1.3, 1.3, 1.5])

    with f1:
        dept_options = ["All Departments"] + sorted(df["Department"].dropna().unique().tolist())
        selected_dept = st.selectbox("Department", dept_options)

    with f2:
        salary_bands = ["All Bands"] + ["Low", "Medium", "High"]
        selected_salary = st.selectbox("Salary Band", salary_bands)

    with f3:
        overtime_opts = ["All"] + sorted(df["OverTime"].dropna().unique().tolist())
        selected_ot = st.selectbox("OverTime Status", overtime_opts)

    with f4:
        min_age = int(df["Age"].min())
        max_age = int(df["Age"].max())
        selected_age = st.slider("Age Span", min_value=min_age, max_value=max_age, value=(min_age, max_age))

    st.markdown('</div>', unsafe_allow_html=True)

# --- FILTERING ENGINE ---
filtered = df[
    (df["Age"] >= selected_age[0]) &
    (df["Age"] <= selected_age[1])
]

if selected_dept != "All Departments":
    filtered = filtered[filtered["Department"] == selected_dept]

if selected_salary != "All Bands" and "Salary Band" in filtered.columns:
    filtered = filtered[filtered["Salary Band"] == selected_salary]

if selected_ot != "All":
    filtered = filtered[filtered["OverTime"] == selected_ot]

# --- KEY PERFORMANCE METRICS ---
total_emp = len(filtered)
attrition_count = len(filtered[filtered["Attrition"] == "Yes"])
active_count = total_emp - attrition_count
attrition_rate = round((attrition_count / total_emp * 100), 2) if total_emp > 0 else 0
avg_monthly_income = round(filtered["MonthlyIncome"].mean(), 0) if total_emp > 0 else 0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Employees Filtered</div>
        <div class="kpi-value">{total_emp:,}</div>
        <div class="kpi-pill">Headcount Scope</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Active Workforce</div>
        <div class="kpi-value">{active_count:,}</div>
        <div class="kpi-pill">Retained Talent</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card alert">
        <div class="kpi-label">Attrition Rate</div>
        <div class="kpi-value">{attrition_rate}%</div>
        <div class="kpi-pill alert">{attrition_count} Departures</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Monthly Salary</div>
        <div class="kpi-value">${int(avg_monthly_income):,}</div>
        <div class="kpi-pill">Compensation Avg</div>
    </div>
    """, unsafe_allow_html=True)

# --- VISUALIZATION SECTION 1 ---
c1, c2 = st.columns([1, 1.45])

with c1:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-title">Attrition Proportion</div>
        <div class="panel-caption">Active headcount vs departed personnel</div>
    """, unsafe_allow_html=True)

    att_counts = filtered["Attrition"].value_counts().reset_index()
    att_counts.columns = ["Attrition", "Count"]

    fig_donut = px.pie(
        att_counts,
        names="Attrition",
        values="Count",
        hole=0.68,
        color="Attrition",
        color_discrete_map={"No": "#00E5FF", "Yes": "#FF6D00"}
    )
    fig_donut.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont=dict(color="#D1D5DB", size=11),
        marker=dict(line=dict(color="#0B0F19", width=2.5)),
        pull=[0.02, 0.02]
    )
    fig_donut.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(t=30, b=25, l=30, r=30)
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-title">Attrition Rate by Department</div>
        <div class="panel-caption">Turnover concentration across organizational business units</div>
    """, unsafe_allow_html=True)

    dept_group = (
        filtered.groupby("Department")["Attrition"]
        .apply(lambda s: (s == "Yes").mean() * 100)
        .reset_index(name="AttritionRate")
    )

    fig_dept = px.bar(
        dept_group,
        x="Department",
        y="AttritionRate",
        color_discrete_sequence=["#FF6D00"],
        text_auto=".1f"
    )
    fig_dept.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8"),
        height=320,
        margin=dict(t=15, b=20, l=55, r=15),
        xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.08)", ticksuffix="%")
    )
    st.plotly_chart(fig_dept, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# --- VISUALIZATION SECTION 2 ---
c3, c4 = st.columns(2)

with c3:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-title">Attrition by Age Bracket</div>
        <div class="panel-caption">Turnover frequency mapped across employee demographic cohorts</div>
    """, unsafe_allow_html=True)

    if "Age Bracket" in filtered.columns:
        age_group = (
            filtered[filtered["Attrition"] == "Yes"]["Age Bracket"]
            .value_counts()
            .reset_index()
        )
        age_group.columns = ["Age Bracket", "Departures"]
        age_group = age_group.sort_values("Age Bracket")

        fig_age = px.bar(
            age_group,
            x="Age Bracket",
            y="Departures",
            color_discrete_sequence=["#00E5FF"]
        )
        fig_age.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8"),
            height=340,
            margin=dict(t=10, b=10, l=45, r=15),
            xaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.08)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.08)")
        )
        st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="panel-container">
        <div class="panel-title">Job Role Risk Analysis</div>
        <div class="panel-caption">Top job titles ordered by absolute departure count</div>
    """, unsafe_allow_html=True)

    role_group = (
        filtered[filtered["Attrition"] == "Yes"]["JobRole"]
        .value_counts()
        .head(7)
        .reset_index()
    )
    role_group.columns = ["JobRole", "Count"]

    fig_role = px.bar(
        role_group.sort_values("Count", ascending=True),
        x="Count",
        y="JobRole",
        orientation="h",
        color_discrete_sequence=["#FF6D00"]
    )
    fig_role.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8"),
        height=340,
        margin=dict(t=10, b=10, l=15, r=15),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(showgrid=False, linecolor="rgba(255,255,255,0.08)")
    )
    st.plotly_chart(fig_role, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# --- SEARCH & EXPLORATION TABLE ---
st.markdown("""
<div class="panel-container">
    <div class="panel-title">Talent Roster Explorer & Deep Search</div>
    <div class="panel-caption">Inspect individual employee records, compensation, and job details</div>
""", unsafe_allow_html=True)

search_keyword = st.text_input("Search records", placeholder="Filter by Job Role, Department, Education Field...", label_visibility="collapsed")

display_cols = [c for c in ["Department", "JobRole", "Age", "MonthlyIncome", "Attrition", "OverTime", "TotalWorkingYears", "YearsAtCompany"] if c in filtered.columns]
table_df = filtered[display_cols].copy()

if search_keyword:
    mask = (
        table_df["JobRole"].astype(str).str.contains(search_keyword, case=False, na=False) |
        table_df["Department"].astype(str).str.contains(search_keyword, case=False, na=False)
    )
    table_df = table_df[mask]

st.dataframe(
    table_df,
    use_container_width=True,
    height=260
)
st.markdown("</div>", unsafe_allow_html=True)
