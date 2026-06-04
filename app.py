import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import io

# ----------------------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------------------
st.set_page_config(
    page_title="OEE Intelligence Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------
# GLOBAL CSS — INDUSTRIAL PRECISION THEME (unchanged + new classes)
# ----------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-card: #1c2230;
        --border: #30363d;
        --accent-blue: #4F8EF7;
        --accent-green: #3DD68C;
        --accent-red: #F75555;
        --accent-amber: #F7A83A;
        --accent-purple: #A78BFA;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-mono: #79c0ff;
    }

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--text-primary);
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp { background-color: var(--bg-primary); }

    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * { color: var(--text-primary) !important; }

    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-secondary);
        border-bottom: 1px solid var(--border);
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary) !important;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px; font-weight: 600;
        letter-spacing: 0.08em; text-transform: uppercase;
        padding: 12px 24px; border: none;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: var(--accent-blue) !important;
        border-bottom: 2px solid var(--accent-blue) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: var(--bg-primary);
        padding-top: 24px;
    }

    .kpi-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 8px; padding: 20px 22px;
        position: relative; overflow: hidden;
    }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 100%; height: 3px;
    }
    .kpi-card.blue::before   { background: var(--accent-blue); }
    .kpi-card.green::before  { background: var(--accent-green); }
    .kpi-card.red::before    { background: var(--accent-red); }
    .kpi-card.purple::before { background: var(--accent-purple); }
    .kpi-card.amber::before  { background: var(--accent-amber); }

    .kpi-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px; font-weight: 600;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--text-secondary); margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 32px; font-weight: 600;
        line-height: 1; margin-bottom: 6px;
    }
    .kpi-sub { font-size: 11px; color: var(--text-secondary); font-family: 'IBM Plex Mono', monospace; }
    .kpi-delta-good { color: var(--accent-green); }
    .kpi-delta-bad  { color: var(--accent-red); }

    .lever-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 8px; padding: 22px 24px; margin-bottom: 14px;
    }
    .lever-badge {
        display: inline-block; font-family: 'IBM Plex Mono', monospace;
        font-size: 10px; font-weight: 700; letter-spacing: 0.12em;
        text-transform: uppercase; padding: 3px 10px; border-radius: 3px; margin-bottom: 10px;
    }
    .lever-title { font-size: 15px; font-weight: 600; color: var(--text-primary); margin: 8px 0 6px 0; }
    .lever-stat  { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--text-secondary); margin-bottom: 8px; }
    .lever-body  { font-size: 13px; color: #a0aab4; line-height: 1.6; }

    .section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px; font-weight: 600; letter-spacing: 0.15em; text-transform: uppercase;
        color: var(--text-secondary); border-bottom: 1px solid var(--border);
        padding-bottom: 8px; margin: 24px 0 18px 0;
    }

    .page-title-band {
        background: linear-gradient(135deg, #161b22 0%, #1c2230 100%);
        border: 1px solid var(--border); border-radius: 10px;
        padding: 24px 28px; margin-bottom: 28px;
        display: flex; align-items: center; gap: 16px;
    }
    .page-title-band h1 { font-family: 'IBM Plex Mono', monospace; font-size: 22px; font-weight: 600; color: var(--text-primary); margin: 0; }
    .page-title-band p  { font-size: 13px; color: var(--text-secondary); margin: 4px 0 0 0; }

    .sim-result-row {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 8px; padding: 18px 22px; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .sim-result-value { font-family: 'IBM Plex Mono', monospace; font-size: 16px; font-weight: 600; color: var(--accent-green); }

    .six-loss-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px 18px; height: 100%; }
    .six-loss-pillar { font-family: 'IBM Plex Mono', monospace; font-size: 9px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 10px; padding: 3px 8px; border-radius: 3px; display: inline-block; }
    .six-loss-name  { font-size: 12px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
    .six-loss-value { font-family: 'IBM Plex Mono', monospace; font-size: 20px; font-weight: 700; line-height: 1; }
    .six-loss-sub   { font-size: 11px; color: var(--text-secondary); font-family: 'IBM Plex Mono', monospace; margin-top: 3px; }

    .cost-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 8px; padding: 18px 20px; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
        border-left: 3px solid var(--border);
    }
    .cost-label { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--text-secondary); letter-spacing: 0.08em; text-transform: uppercase; }
    .cost-value { font-family: 'IBM Plex Mono', monospace; font-size: 18px; font-weight: 700; }

    .alert-critical { background: rgba(247,85,85,0.08); border: 1px solid #F75555; border-left: 4px solid #F75555; border-radius: 8px; padding: 16px 20px; margin-bottom: 14px; }
    .alert-warning  { background: rgba(247,168,58,0.08); border: 1px solid #F7A83A; border-left: 4px solid #F7A83A; border-radius: 8px; padding: 16px 20px; margin-bottom: 14px; }
    .alert-info     { background: rgba(79,142,247,0.08); border: 1px solid #4F8EF7; border-left: 4px solid #4F8EF7; border-radius: 8px; padding: 16px 20px; margin-bottom: 14px; }
    .alert-title    { font-size: 14px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
    .alert-body     { font-size: 13px; color: #a0aab4; line-height: 1.6; }

    /* NEW — Executive Snapshot Banner */
    .exec-banner {
        background: linear-gradient(135deg, #1c2230 0%, #161b22 100%);
        border: 1px solid var(--border); border-radius: 10px;
        padding: 20px 24px; margin-bottom: 20px;
    }
    .exec-banner-title { font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 14px; }
    .exec-action-item { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 10px; }
    .exec-action-num  { font-family: 'IBM Plex Mono', monospace; font-size: 11px; font-weight: 700; color: #0d1117; background: var(--accent-blue); border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
    .exec-action-text { font-size: 13px; color: var(--text-primary); line-height: 1.5; }
    .exec-action-meta { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--text-secondary); margin-top: 2px; }

    /* NEW — Benchmark card */
    .bench-card {
        background: var(--bg-card); border: 1px solid var(--border);
        border-radius: 8px; padding: 18px 20px; margin-bottom: 10px;
    }
    .bench-label { font-family: 'IBM Plex Mono', monospace; font-size: 10px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 8px; }
    .bench-run   { font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 700; color: var(--accent-green); margin-bottom: 4px; }
    .bench-val   { font-family: 'IBM Plex Mono', monospace; font-size: 26px; font-weight: 700; line-height: 1; }
    .bench-gap   { font-size: 11px; color: var(--text-secondary); margin-top: 4px; }

    /* NEW — Consistency badge */
    .consistency-badge {
        display: inline-block; font-family: 'IBM Plex Mono', monospace;
        font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 4px; margin-left: 8px;
    }

    /* NEW — TEEP card */
    .teep-card {
        background: linear-gradient(135deg, rgba(79,142,247,0.08) 0%, rgba(167,139,250,0.08) 100%);
        border: 1px solid rgba(79,142,247,0.3); border-radius: 8px; padding: 20px 22px;
    }

    .stPlotlyChart { background-color: transparent !important; }
    .stFileUploader, .stSelectbox, .stMultiSelect { background-color: var(--bg-card) !important; border-color: var(--border) !important; }
    label { color: var(--text-secondary) !important; }
    .stSlider > div { color: var(--text-primary) !important; }
    .stSuccess { background-color: rgba(61,214,140,0.1) !important; border-color: var(--accent-green) !important; }
    .stWarning { background-color: rgba(247,168,58,0.1) !important; border-color: var(--accent-amber) !important; }
    .stExpander { background-color: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
    .stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px !important; }
    [data-testid="stSidebar"] .stCheckbox label { color: var(--text-primary) !important; }
    .stNumberInput input { background-color: var(--bg-card) !important; color: var(--text-primary) !important; border-color: var(--border) !important; }
    .stDownloadButton > button {
        background-color: var(--bg-card) !important; color: var(--text-primary) !important;
        border: 1px solid var(--border) !important; font-family: 'IBM Plex Mono', monospace !important;
        font-size: 12px !important; letter-spacing: 0.06em !important;
    }
    .stDownloadButton > button:hover { border-color: var(--accent-blue) !important; color: var(--accent-blue) !important; }
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------
# PLOTLY SHARED THEME
# ----------------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono, monospace", color="#8b949e", size=11),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont=dict(color="#8b949e")),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickfont=dict(color="#8b949e")),
    margin=dict(t=40, b=40, l=60, r=30),
    legend=dict(bgcolor="rgba(22,27,34,0.8)", bordercolor="#30363d", borderwidth=1, font=dict(size=11))
)

COLOR_OEE   = "#4F8EF7"
COLOR_AVAIL = "#3DD68C"
COLOR_PERF  = "#F7A83A"
COLOR_QUAL  = "#A78BFA"
COLOR_RED   = "#F75555"
COLOR_GREY  = "#30363d"


# ----------------------------------------------------------------
# DATA PIPELINE
# ----------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_bytes=None, filename=None, is_sample=False,
                         part_value=12.50, machine_rate=75.0, labor_rate=35.0):
    if is_sample:
        np.random.seed(42)
        rows = 15
        sched_time     = [480] * rows
        planned_down   = np.random.randint(15, 35, size=rows)
        unplanned_down = np.random.randint(20, 85, size=rows)
        cycle_time     = [80] * rows
        total_qty, defective_qty = [], []
        for i in range(rows):
            net_op_m     = sched_time[i] - planned_down[i] - unplanned_down[i]
            max_possible = int((net_op_m * 60) / cycle_time[i])
            actual       = int(max_possible * np.random.uniform(0.90, 0.99))
            scrap        = int(actual * np.random.uniform(0.01, 0.05))
            total_qty.append(actual)
            defective_qty.append(scrap)
        data = {
            'Cycle Time (Seconds) Look Up / Override': cycle_time,
            'Scheduled Production Time': sched_time,
            'Planned Downtime':          planned_down,
            'Unplanned Downtime':        unplanned_down,
            'Total Quantity Produced':   total_qty,
            'Total Quantity Defective':  defective_qty
        }
        df = pd.DataFrame(data)
    else:
        buf = io.BytesIO(file_bytes)
        if filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(buf)
        else:
            df = pd.read_csv(buf)

    df = df.dropna(how='all')
    df.columns = [str(c).replace('\n', ' ').replace('  ', ' ').strip().replace('"', '') for c in df.columns]

    target_cols = [
        'Cycle Time (Seconds) Look Up / Override',
        'Scheduled Production Time', 'Planned Downtime',
        'Unplanned Downtime', 'Total Quantity Produced', 'Total Quantity Defective'
    ]
    col_mapping = {}
    for target in target_cols:
        if target not in df.columns:
            keyword = target.split(' ')[0]
            matched = [c for c in df.columns if keyword.lower() in c.lower()]
            if matched:
                col_mapping[matched[0]] = target
    if col_mapping:
        df = df.rename(columns=col_mapping)

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.fillna(0)

    # Core time derivations
    df['Net Available Time']    = df['Scheduled Production Time'] - df['Planned Downtime']
    df['Net Operating Time']    = df['Net Available Time'] - df['Unplanned Downtime']
    df['Ideal Operating Time']  = (df['Total Quantity Produced'] * df['Cycle Time (Seconds) Look Up / Override']) / 60
    df['Lost Quality Time']     = (df['Total Quantity Defective'] * df['Cycle Time (Seconds) Look Up / Override']) / 60
    df['Performance Loss Time'] = (df['Net Operating Time'] - df['Ideal Operating Time']).clip(lower=0)

    # OEE pillars
    df['Availability (A)'] = np.where(df['Net Available Time'] > 0,
                                       df['Net Operating Time'] / df['Net Available Time'], 0)
    df['Performance (P)']  = np.where(df['Net Operating Time'] > 0,
                                       df['Ideal Operating Time'] / df['Net Operating Time'], 0)
    df['Quality (Q)']      = np.where(df['Total Quantity Produced'] > 0,
                                       (df['Total Quantity Produced'] - df['Total Quantity Defective']) / df['Total Quantity Produced'], 0)
    df['OEE (A × P × Q)'] = df['Availability (A)'] * df['Performance (P)'] * df['Quality (Q)']

    for p_col in ['Availability (A)', 'Performance (P)', 'Quality (Q)', 'OEE (A × P × Q)']:
        df[p_col] = df[p_col].clip(0.0, 1.0)

    # NEW — TEEP: uses total calendar time (assume 1440 min/day per run = full 24h)
    df['Calendar Time']  = 1440
    df['TEEP']           = df['OEE (A × P × Q)'] * (df['Scheduled Production Time'] / df['Calendar Time'])
    df['TEEP']           = df['TEEP'].clip(0.0, 1.0)

    # Financial leakage
    combined_rate = machine_rate + labor_rate
    df['Cost: Planned Downtime']   = df['Planned Downtime']      * (machine_rate / 60)
    df['Cost: Unplanned Downtime'] = df['Unplanned Downtime']    * (combined_rate / 60)
    df['Cost: Speed / Perf Loss']  = df['Performance Loss Time'] * (machine_rate / 60)
    df['Cost: Scrap / Rework']     = df['Total Quantity Defective'] * part_value
    df['Total Financial Leakage']  = (
        df['Cost: Planned Downtime'] + df['Cost: Unplanned Downtime'] +
        df['Cost: Speed / Perf Loss'] + df['Cost: Scrap / Rework']
    )

    df.insert(0, 'Run ID', [f"Run_{i+1:02d}" for i in range(len(df))])
    return df


# ----------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='padding: 8px 0 16px 0;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 18px; font-weight: 700; color: #4F8EF7; letter-spacing: 0.05em;'>
            ◈ OEE PLATFORM
        </div>
        <div style='font-size: 11px; color: #8b949e; margin-top: 4px; font-family: IBM Plex Mono, monospace;'>
            INDUSTRIAL INTELLIGENCE
        </div>
    </div>
    <hr style='border-color: #30363d; margin: 0 0 16px 0;'>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Production Log", type=["csv", "xlsx"],
                                      help="Accepts .csv or .xlsx factory data exports")
    use_sample = st.checkbox("Use sample dataset", value=(uploaded_file is None))

    st.markdown("<hr style='border-color: #30363d; margin: 16px 0 12px 0;'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family: IBM Plex Mono, monospace; font-size: 10px; font-weight: 700;
        letter-spacing: 0.15em; color: #8b949e; text-transform: uppercase; margin-bottom: 10px;'>
        Cost Parameters</div>""", unsafe_allow_html=True)

    part_value   = st.number_input("Part / Material Value ($):",  min_value=0.0, value=12.50, step=0.50)
    machine_rate = st.number_input("Machine Hourly Rate ($/hr):", min_value=0.0, value=75.00, step=5.00)
    labor_rate   = st.number_input("Labor Hourly Rate ($/hr):",   min_value=0.0, value=35.00, step=5.00)

    st.markdown("<hr style='border-color: #30363d; margin: 16px 0;'>", unsafe_allow_html=True)

    if uploaded_file is not None:
        raw_df = load_and_clean_data(
            file_bytes=uploaded_file.read(), filename=uploaded_file.name, is_sample=False,
            part_value=part_value, machine_rate=machine_rate, labor_rate=labor_rate
        )
        data_source_label = f"📂 {uploaded_file.name}"
    elif use_sample:
        raw_df = load_and_clean_data(is_sample=True,
                                      part_value=part_value, machine_rate=machine_rate, labor_rate=labor_rate)
        data_source_label = "🧪 Sample Dataset (15 Runs)"
    else:
        st.info("Upload a production log or enable the sample dataset to begin.")
        st.stop()

    st.markdown("""<div style='font-family: IBM Plex Mono, monospace; font-size: 10px; font-weight: 700;
        letter-spacing: 0.15em; color: #8b949e; text-transform: uppercase; margin-bottom: 10px;'>
        Run Selection Filter</div>""", unsafe_allow_html=True)

    all_runs      = raw_df['Run ID'].tolist()
    selected_runs = st.multiselect("Runs to include:", options=all_runs, default=all_runs,
                                    label_visibility="collapsed")

    if not selected_runs:
        st.warning("Select at least one run to continue.")
        st.stop()

    df = raw_df[raw_df['Run ID'].isin(selected_runs)].reset_index(drop=True)

    st.markdown(f"""
    <hr style='border-color: #30363d; margin: 16px 0;'>
    <div style='font-family: IBM Plex Mono, monospace; font-size: 10px; color: #8b949e; letter-spacing: 0.08em;'>
        SOURCE<br><span style='color: #e6edf3;'>{data_source_label}</span>
    </div>
    <div style='font-family: IBM Plex Mono, monospace; font-size: 10px; color: #8b949e; letter-spacing: 0.08em; margin-top: 8px;'>
        SELECTED RUNS<br><span style='color: #e6edf3;'>{len(df)} / {len(raw_df)}</span>
    </div>
    <div style='font-family: IBM Plex Mono, monospace; font-size: 10px; color: #8b949e; letter-spacing: 0.08em; margin-top: 8px;'>
        TOTAL LEAKAGE<br><span style='color: #F75555; font-weight: 700;'>${df["Total Financial Leakage"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── NEW: Export buttons in sidebar ──────────────────────────
    st.markdown("<hr style='border-color: #30363d; margin: 16px 0 12px 0;'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-family: IBM Plex Mono, monospace; font-size: 10px; font-weight: 700;
        letter-spacing: 0.15em; color: #8b949e; text-transform: uppercase; margin-bottom: 10px;'>
        Export Data</div>""", unsafe_allow_html=True)

    export_cols = [c for c in [
        'Run ID', 'Scheduled Production Time', 'Planned Downtime', 'Unplanned Downtime',
        'Net Available Time', 'Net Operating Time', 'Total Quantity Produced', 'Total Quantity Defective',
        'Availability (A)', 'Performance (P)', 'Quality (Q)', 'OEE (A × P × Q)', 'TEEP',
        'Cost: Planned Downtime', 'Cost: Unplanned Downtime', 'Cost: Speed / Perf Loss',
        'Cost: Scrap / Rework', 'Total Financial Leakage'
    ] if c in df.columns]

    csv_bytes = df[export_cols].to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", data=csv_bytes,
                        file_name="oee_report.csv", mime="text/csv", use_container_width=True)

    excel_buf = io.BytesIO()
    with pd.ExcelWriter(excel_buf, engine='openpyxl') as writer:
        df[export_cols].to_excel(writer, index=False, sheet_name='OEE Data')
    st.download_button("⬇ Download Excel", data=excel_buf.getvalue(),
                        file_name="oee_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True)


# ----------------------------------------------------------------
# FLEET AVERAGES, TOTALS & NEW ANALYTICS
# ----------------------------------------------------------------
avg_oee   = float(df['OEE (A × P × Q)'].mean())
avg_avail = float(df['Availability (A)'].mean())
avg_perf  = float(df['Performance (P)'].mean())
avg_qual  = float(df['Quality (Q)'].mean())
avg_teep  = float(df['TEEP'].mean())

total_leakage        = float(df['Total Financial Leakage'].sum())
total_planned_cost   = float(df['Cost: Planned Downtime'].sum())
total_unplanned_cost = float(df['Cost: Unplanned Downtime'].sum())
total_speed_cost     = float(df['Cost: Speed / Perf Loss'].sum())
total_scrap_cost     = float(df['Cost: Scrap / Rework'].sum())

# NEW — Best Run Benchmarking
best_idx      = df['OEE (A × P × Q)'].idxmax()
worst_idx     = df['OEE (A × P × Q)'].idxmin()
best_run_id   = df.loc[best_idx, 'Run ID']
worst_run_id  = df.loc[worst_idx, 'Run ID']
best_oee      = float(df.loc[best_idx, 'OEE (A × P × Q)'])
worst_oee     = float(df.loc[worst_idx, 'OEE (A × P × Q)'])
best_avail    = float(df.loc[best_idx, 'Availability (A)'])
best_perf     = float(df.loc[best_idx, 'Performance (P)'])
best_qual     = float(df.loc[best_idx, 'Quality (Q)'])

# NEW — Consistency / Volatility (Coefficient of Variation)
oee_std   = float(df['OEE (A × P × Q)'].std())
oee_cv    = (oee_std / avg_oee * 100) if avg_oee > 0 else 0
cv_label  = "HIGH STABILITY" if oee_cv < 5 else "MODERATE" if oee_cv < 12 else "HIGH VOLATILITY"
cv_color  = COLOR_AVAIL if oee_cv < 5 else COLOR_PERF if oee_cv < 12 else COLOR_RED

# NEW — SPC Control Limits (±3σ)
ucl = min(avg_oee + 3 * oee_std, 1.0)
lcl = max(avg_oee - 3 * oee_std, 0.0)
out_of_control = df[(df['OEE (A × P × Q)'] > ucl) | (df['OEE (A × P × Q)'] < lcl)]['Run ID'].tolist()

# NEW — Executive Priority Actions (auto-generated)
exec_actions = []
if avg_avail < 0.90:
    gap_a = (0.90 - avg_avail) * 100
    cost_a = total_unplanned_cost
    exec_actions.append({
        "title": f"Reduce unplanned downtime to hit 90% Availability target",
        "meta":  f"Current {avg_avail*100:.1f}% · Gap {gap_a:.1f}pp · Leakage ${cost_a:,.0f}",
        "color": COLOR_RED if avg_avail < 0.80 else COLOR_PERF
    })
if avg_perf < 0.95:
    gap_p = (0.95 - avg_perf) * 100
    exec_actions.append({
        "title": f"Lock cycle times & eliminate micro-stops to hit 95% Performance",
        "meta":  f"Current {avg_perf*100:.1f}% · Gap {gap_p:.1f}pp · Leakage ${total_speed_cost:,.0f}",
        "color": COLOR_RED if avg_perf < 0.75 else COLOR_PERF
    })
if avg_qual < 0.98:
    gap_q = (0.98 - avg_qual) * 100
    exec_actions.append({
        "title": f"Deploy inline SPC & Poka-Yoke to hit 98% Quality Yield",
        "meta":  f"Current {avg_qual*100:.1f}% · Gap {gap_q:.1f}pp · Leakage ${total_scrap_cost:,.0f}",
        "color": COLOR_RED if avg_qual < 0.90 else COLOR_PERF
    })
if oee_cv > 8:
    exec_actions.append({
        "title": f"Stabilise process: OEE variation of {oee_cv:.1f}% CV signals inconsistent operations",
        "meta":  f"Std Dev {oee_std*100:.1f}pp · Best Run {best_oee*100:.1f}% · Worst Run {worst_oee*100:.1f}%",
        "color": COLOR_PERF
    })
if not exec_actions:
    exec_actions.append({
        "title": "All KPIs at or above world-class thresholds — focus on sustaining performance",
        "meta":  f"OEE {avg_oee*100:.1f}% · Availability {avg_avail*100:.1f}% · Performance {avg_perf*100:.1f}% · Quality {avg_qual*100:.1f}%",
        "color": COLOR_AVAIL
    })


# ----------------------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------------------
oee_color = "#3DD68C" if avg_oee >= 0.85 else "#F7A83A" if avg_oee >= 0.65 else "#F75555"
st.markdown(f"""
<div class='page-title-band'>
    <div style='width:44px; height:44px; background: linear-gradient(135deg,#4F8EF7,#A78BFA); border-radius:8px;
                display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0;'>🏭</div>
    <div>
        <h1>OEE Intelligence Platform</h1>
        <p>Equipment Effectiveness · Waterfall Diagnostics · Improvement Levers · Financial Simulator</p>
    </div>
    <div style='margin-left:auto; text-align:right; padding-right:24px;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size:26px; font-weight:700; color:{oee_color};'>{avg_oee*100:.1f}%</div>
        <div style='font-family: IBM Plex Mono, monospace; font-size:9px; color:#8b949e; letter-spacing:0.1em;'>FLEET OEE</div>
    </div>
    <div style='text-align:right; padding-right:24px;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size:26px; font-weight:700; color:#A78BFA;'>{avg_teep*100:.1f}%</div>
        <div style='font-family: IBM Plex Mono, monospace; font-size:9px; color:#8b949e; letter-spacing:0.1em;'>FLEET TEEP</div>
    </div>
    <div style='text-align:right;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size:26px; font-weight:700; color:#F75555;'>${total_leakage:,.0f}</div>
        <div style='font-family: IBM Plex Mono, monospace; font-size:9px; color:#8b949e; letter-spacing:0.1em;'>TOTAL LEAKAGE</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── NEW: Executive Snapshot Banner ───────────────────────────────
items_html_parts = []
for i, act in enumerate(exec_actions[:4], 1):
    bg   = act["color"]
    ttl  = act["title"]
    meta = act["meta"]
    items_html_parts.append(
        "<div class='exec-action-item'>"
        "<div class='exec-action-num' style='background:" + bg + ";'>" + str(i) + "</div>"
        "<div>"
        "<div class='exec-action-text'>" + ttl + "</div>"
        "<div class='exec-action-meta'>" + meta + "</div>"
        "</div>"
        "</div>"
    )
items_html = "\n".join(items_html_parts)

oc_html = ""
if out_of_control:
    runs_str = ", ".join(out_of_control)
    oc_html = (
        "<div style='font-family:IBM Plex Mono,monospace;font-size:11px;color:"
        + COLOR_RED
        + ";margin-top:10px;'>\u26a0 SPC Alert: Runs outside 3\u03c3 limits \u2192 "
        + runs_str + "</div>"
    )

st.markdown(
    "<div class='exec-banner'>"
    "<div class='exec-banner-title'>⚡ Executive Priority Actions</div>"
    + items_html
    + oc_html
    + "</div>",
    unsafe_allow_html=True
)


# ----------------------------------------------------------------
# TABS
# ----------------------------------------------------------------
tab_summary, tab_waterfall, tab_levers, tab_simulator = st.tabs([
    "PERFORMANCE TRENDS",
    "WATERFALL DIAGNOSTIC",
    "IMPROVEMENT LEVERS",
    "FINANCIAL SIMULATOR",
])


# ================================================================
# TAB 1 — PERFORMANCE TRENDS
# ================================================================
with tab_summary:

    def delta_vs_target(val, target):
        diff = (val - target) * 100
        sign = "+" if diff >= 0 else ""
        cls  = "kpi-delta-good" if diff >= 0 else "kpi-delta-bad"
        return f"<span class='{cls}'>{sign}{diff:.1f}pp vs target</span>"

    # Original KPI row
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class='kpi-card blue'>
            <div class='kpi-label'>Overall OEE</div>
            <div class='kpi-value' style='color:#4F8EF7;'>{avg_oee*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_oee, 0.85)}</div>
        </div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class='kpi-card green'>
            <div class='kpi-label'>Availability</div>
            <div class='kpi-value' style='color:#3DD68C;'>{avg_avail*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_avail, 0.90)}</div>
        </div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class='kpi-card red'>
            <div class='kpi-label'>Performance</div>
            <div class='kpi-value' style='color:#F7A83A;'>{avg_perf*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_perf, 0.95)}</div>
        </div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class='kpi-card purple'>
            <div class='kpi-label'>Quality Yield</div>
            <div class='kpi-value' style='color:#A78BFA;'>{avg_qual*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_qual, 0.98)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── NEW Row 2: TEEP + Consistency + Best Run + Worst Run ─────
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(f"""
        <div class='teep-card'>
            <div class='kpi-label'>TEEP <span style='font-size:9px;color:#8b949e;'>(Total Effective Equip. Perf.)</span></div>
            <div class='kpi-value' style='color:#A78BFA;'>{avg_teep*100:.1f}%</div>
            <div class='kpi-sub' style='color:#8b949e;'>OEE × Utilisation Rate</div>
        </div>""", unsafe_allow_html=True)
    with t2:
        st.markdown(f"""
        <div class='bench-card'>
            <div class='bench-label'>OEE Consistency <span class='consistency-badge' style='background:{cv_color}22;color:{cv_color};'>{cv_label}</span></div>
            <div class='bench-val' style='color:{cv_color};'>{oee_cv:.1f}% CV</div>
            <div class='bench-gap'>Std Dev: {oee_std*100:.1f}pp across {len(df)} runs</div>
        </div>""", unsafe_allow_html=True)
    with t3:
        st.markdown(f"""
        <div class='bench-card'>
            <div class='bench-label'>Best Run Benchmark</div>
            <div class='bench-run'>{best_run_id}</div>
            <div class='bench-val' style='color:{COLOR_AVAIL};'>{best_oee*100:.1f}%</div>
            <div class='bench-gap'>+{(best_oee - avg_oee)*100:.1f}pp above fleet avg</div>
        </div>""", unsafe_allow_html=True)
    with t4:
        st.markdown(f"""
        <div class='bench-card'>
            <div class='bench-label'>Worst Run (Drag)</div>
            <div class='bench-run' style='color:{COLOR_RED};'>{worst_run_id}</div>
            <div class='bench-val' style='color:{COLOR_RED};'>{worst_oee*100:.1f}%</div>
            <div class='bench-gap'>{(avg_oee - worst_oee)*100:.1f}pp below fleet avg</div>
        </div>""", unsafe_allow_html=True)

    # Original OEE trend chart
    st.markdown("<div class='section-header' style='margin-top:32px;'>Run-Over-Run Trend Analysis</div>",
                unsafe_allow_html=True)

    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=df['Run ID'], y=df['OEE (A × P × Q)'] * 100, name='OEE',
        line=dict(color=COLOR_OEE, width=3),
        fill='tozeroy', fillcolor='rgba(79,142,247,0.06)'
    ))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['Availability (A)'] * 100,
                                     name='Availability', line=dict(color=COLOR_AVAIL, width=1.5, dash='dash')))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['Performance (P)'] * 100,
                                     name='Performance', line=dict(color=COLOR_PERF, width=1.5, dash='dot')))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['Quality (Q)'] * 100,
                                     name='Quality', line=dict(color=COLOR_QUAL, width=1.5, dash='longdash')))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['TEEP'] * 100,
                                     name='TEEP', line=dict(color='#A78BFA', width=1.5, dash='dashdot'),
                                     opacity=0.7))
    fig_trends.add_hline(y=85, line_dash="dash", line_color="#F75555", line_width=1,
                          annotation_text="World-Class Target (85%)",
                          annotation_font_color="#F75555", annotation_font_size=11)
    # NEW — fleet average reference line
    fig_trends.add_hline(y=avg_oee * 100, line_dash="dot", line_color=COLOR_OEE, line_width=1,
                          annotation_text=f"Fleet Avg ({avg_oee*100:.1f}%)",
                          annotation_font_color=COLOR_OEE, annotation_font_size=10)
    fig_trends.update_layout(**PLOTLY_LAYOUT, height=420,
                              yaxis_title="Efficiency (%)", xaxis_title="Production Run")
    fig_trends.update_yaxes(range=[0, 105])
    st.plotly_chart(fig_trends, use_container_width=True)

    # ── NEW: SPC Control Chart ───────────────────────────────────
    st.markdown("<div class='section-header'>SPC Control Chart — OEE Statistical Process Control</div>",
                unsafe_allow_html=True)

    oee_pct = df['OEE (A × P × Q)'] * 100
    fig_spc = go.Figure()
    # Fill between UCL/LCL
    fig_spc.add_trace(go.Scatter(
        x=df['Run ID'].tolist() + df['Run ID'].tolist()[::-1],
        y=[ucl*100]*len(df) + [lcl*100]*len(df),
        fill='toself', fillcolor='rgba(79,142,247,0.04)',
        line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
    ))
    fig_spc.add_trace(go.Scatter(x=df['Run ID'], y=[ucl*100]*len(df),
                                  name='UCL (+3σ)', line=dict(color=COLOR_RED, width=1, dash='dash'),
                                  mode='lines'))
    fig_spc.add_trace(go.Scatter(x=df['Run ID'], y=[lcl*100]*len(df),
                                  name='LCL (−3σ)', line=dict(color=COLOR_RED, width=1, dash='dash'),
                                  mode='lines', showlegend=False))
    fig_spc.add_trace(go.Scatter(x=df['Run ID'], y=[avg_oee*100]*len(df),
                                  name='Mean', line=dict(color=COLOR_OEE, width=1.5, dash='dot'),
                                  mode='lines'))
    # Points — colour out-of-control red
    point_colors = [COLOR_RED if rid in out_of_control else COLOR_OEE for rid in df['Run ID']]
    point_sizes  = [12 if rid in out_of_control else 8 for rid in df['Run ID']]
    fig_spc.add_trace(go.Scatter(
        x=df['Run ID'], y=oee_pct,
        name='OEE per Run', mode='lines+markers',
        line=dict(color=COLOR_OEE, width=2),
        marker=dict(color=point_colors, size=point_sizes, symbol='circle',
                    line=dict(color='#0d1117', width=1))
    ))
    fig_spc.update_layout(**PLOTLY_LAYOUT, height=320,
                           yaxis_title="OEE (%)", xaxis_title="Production Run")
    fig_spc.update_yaxes(range=[max(0, lcl*100 - 10), min(105, ucl*100 + 10)])
    st.plotly_chart(fig_spc, use_container_width=True)

    if out_of_control:
        st.markdown(f"""
        <div style='background:rgba(247,85,85,0.08); border:1px solid #F75555; border-radius:8px;
                    padding:12px 16px; font-family:IBM Plex Mono,monospace; font-size:12px; color:#F75555;'>
            ⚠ Out-of-control runs detected: <strong>{", ".join(out_of_control)}</strong> — investigate for assignable causes.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background:rgba(61,214,140,0.06); border:1px solid #3DD68C; border-radius:8px;
                    padding:12px 16px; font-family:IBM Plex Mono,monospace; font-size:12px; color:#3DD68C;'>
            ✓ All runs within 3σ statistical control limits — process is stable.
        </div>""", unsafe_allow_html=True)

    # Original grouped bar chart
    st.markdown("<div class='section-header'>Run-Level Breakdown</div>", unsafe_allow_html=True)
    fig_bar = go.Figure()
    for col, name, color in [
        ('Availability (A)', 'Availability', COLOR_AVAIL),
        ('Performance (P)',  'Performance',  COLOR_PERF),
        ('Quality (Q)',      'Quality',      COLOR_QUAL),
    ]:
        fig_bar.add_trace(go.Bar(x=df['Run ID'], y=df[col] * 100, name=name,
                                  marker_color=color, opacity=0.85))
    fig_bar.add_trace(go.Scatter(
        x=df['Run ID'], y=df['OEE (A × P × Q)'] * 100, name='OEE',
        mode='markers+lines',
        marker=dict(color=COLOR_OEE, size=8, symbol='diamond'),
        line=dict(color=COLOR_OEE, width=2)
    ))
    fig_bar.update_layout(**PLOTLY_LAYOUT, barmode='group', height=350,
                           yaxis_title="Efficiency (%)", xaxis_title="Production Run")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── NEW: OEE vs Financial Leakage Scatter ────────────────────
    st.markdown("<div class='section-header'>OEE vs Financial Leakage — Correlation Scatter</div>",
                unsafe_allow_html=True)

    fig_scatter = go.Figure()
    scatter_colors = df['Total Financial Leakage'].tolist()
    fig_scatter.add_trace(go.Scatter(
        x=df['OEE (A × P × Q)'] * 100,
        y=df['Total Financial Leakage'],
        mode='markers+text',
        text=df['Run ID'],
        textposition='top center',
        textfont=dict(family='IBM Plex Mono, monospace', size=9, color='#8b949e'),
        marker=dict(
            size=14,
            color=df['Total Financial Leakage'].tolist(),
            colorscale=[[0, COLOR_AVAIL], [0.5, COLOR_PERF], [1, COLOR_RED]],
            showscale=True,
            colorbar=dict(
                title=dict(text="$ Leakage", font=dict(color='#8b949e', size=10)),
                tickfont=dict(color='#8b949e', size=10)
            ),
            line=dict(color='#0d1117', width=1)
        ),
        hovertemplate='<b>%{text}</b><br>OEE: %{x:.1f}%<br>Leakage: $%{y:,.0f}<extra></extra>'
    ))
    # Trend line
    if len(df) > 2:
        z  = np.polyfit(df['OEE (A × P × Q)'] * 100, df['Total Financial Leakage'], 1)
        xr = np.linspace((df['OEE (A × P × Q)'] * 100).min(), (df['OEE (A × P × Q)'] * 100).max(), 50)
        fig_scatter.add_trace(go.Scatter(
            x=xr, y=np.polyval(z, xr), name='Trend',
            mode='lines', line=dict(color=COLOR_OEE, width=1.5, dash='dot'),
            opacity=0.6
        ))
    fig_scatter.update_layout(**PLOTLY_LAYOUT, height=380,
                               xaxis_title="OEE (%)", yaxis_title="Financial Leakage ($)")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Original financial leakage stacked bar
    st.markdown("<div class='section-header'>Financial Leakage Per Run</div>", unsafe_allow_html=True)
    fig_cost = go.Figure()
    fig_cost.add_trace(go.Bar(x=df['Run ID'], y=df['Cost: Unplanned Downtime'],
                               name='Unplanned Downtime', marker_color=COLOR_RED, opacity=0.9))
    fig_cost.add_trace(go.Bar(x=df['Run ID'], y=df['Cost: Planned Downtime'],
                               name='Planned Downtime', marker_color=COLOR_GREY, opacity=0.9))
    fig_cost.add_trace(go.Bar(x=df['Run ID'], y=df['Cost: Speed / Perf Loss'],
                               name='Speed Loss', marker_color=COLOR_PERF, opacity=0.9))
    fig_cost.add_trace(go.Bar(x=df['Run ID'], y=df['Cost: Scrap / Rework'],
                               name='Scrap / Rework', marker_color=COLOR_QUAL, opacity=0.9))
    fig_cost.update_layout(**PLOTLY_LAYOUT, barmode='stack', height=320,
                            yaxis_title="Cost ($)", xaxis_title="Production Run")
    st.plotly_chart(fig_cost, use_container_width=True)

    # ── NEW: Best Run Benchmark Detail ───────────────────────────
    st.markdown("<div class='section-header'>Best Run Benchmark — Performance Fingerprint</div>",
                unsafe_allow_html=True)
    bc1, bc2, bc3 = st.columns(3)
    bench_items = [
        (bc1, "Availability", best_avail, avg_avail, 0.90, COLOR_AVAIL),
        (bc2, "Performance",  best_perf,  avg_perf,  0.95, COLOR_PERF),
        (bc3, "Quality",      best_qual,  avg_qual,  0.98, COLOR_QUAL),
    ]
    for col_obj, label, best_val, fleet_val, target, color in bench_items:
        gap_to_target = (best_val - target) * 100
        gap_to_fleet  = (best_val - fleet_val) * 100
        with col_obj:
            st.markdown(f"""
            <div class='bench-card'>
                <div class='bench-label'>{label} — {best_run_id}</div>
                <div class='bench-val' style='color:{color};'>{best_val*100:.1f}%</div>
                <div class='bench-gap'>
                    Fleet avg: {fleet_val*100:.1f}% &nbsp;·&nbsp;
                    <span style='color:{COLOR_AVAIL if gap_to_fleet>=0 else COLOR_RED};'>
                        {"+"+f"{gap_to_fleet:.1f}pp" if gap_to_fleet>=0 else f"{gap_to_fleet:.1f}pp"}
                    </span><br>
                    vs Target: <span style='color:{COLOR_AVAIL if gap_to_target>=0 else COLOR_RED};'>
                        {"+"+f"{gap_to_target:.1f}pp" if gap_to_target>=0 else f"{gap_to_target:.1f}pp"}
                    </span>
                </div>
            </div>""", unsafe_allow_html=True)


# ================================================================
# TAB 2 — WATERFALL DIAGNOSTIC (unchanged + existing Six Big Losses)
# ================================================================
with tab_waterfall:
    st.markdown("<div class='section-header' style='margin-top:0;'>Capacity Loss Waterfall — Time-Drop Funnel</div>",
                unsafe_allow_html=True)

    target_shift = st.selectbox("Select Run to Diagnose:", options=df['Run ID'].tolist())
    row = df[df['Run ID'] == target_shift].iloc[0]

    sched       = float(row['Scheduled Production Time'])
    p_down      = float(row['Planned Downtime'])
    net_avail   = float(row['Net Available Time'])
    u_down      = float(row['Unplanned Downtime'])
    net_op      = float(row['Net Operating Time'])
    ideal_op    = float(row['Ideal Operating Time'])
    lost_q      = float(row['Lost Quality Time'])
    perf_loss   = float(row['Performance Loss Time'])
    fully_prod  = max(0.0, ideal_op - lost_q)
    avail_r     = float(row['Availability (A)'])
    perf_r      = float(row['Performance (P)'])
    qual_r      = float(row['Quality (Q)'])
    oee_r       = float(row['OEE (A × P × Q)'])
    run_leakage = float(row['Total Financial Leakage'])
    run_teep    = float(row['TEEP'])

    r1, r2, r3, r4, r5 = st.columns(5)
    for col_obj, label, val, color, is_pct in [
        (r1, "Run OEE",      oee_r,        COLOR_OEE,   True),
        (r2, "Availability", avail_r,      COLOR_AVAIL, True),
        (r3, "Performance",  perf_r,       COLOR_PERF,  True),
        (r4, "Quality",      qual_r,       COLOR_QUAL,  True),
        (r5, "$ Leakage",    run_leakage,  COLOR_RED,   False),
    ]:
        with col_obj:
            display = f"{val*100:.1f}%" if is_pct else f"${val:,.0f}"
            st.markdown(f"""
            <div style='background:#1c2230; border:1px solid #30363d; border-radius:8px;
                        padding:14px 18px; text-align:center;'>
                <div style='font-family: IBM Plex Mono, monospace; font-size:10px; color:#8b949e;
                            letter-spacing:0.12em; text-transform:uppercase;'>{label}</div>
                <div style='font-family: IBM Plex Mono, monospace; font-size:22px; font-weight:700;
                            color:{color}; margin-top:4px;'>{display}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","total","relative","total","relative","total","relative","total"],
        x=["Scheduled Time","Planned Downtime","Net Available","Unplanned Breakdowns",
           "Net Operating","Speed / Perf Loss","Ideal Operating","Quality / Scrap Loss","Fully Productive"],
        y=[sched, -p_down, 0, -u_down, 0, -perf_loss, 0, -lost_q, 0],
        text=[f"{sched:.0f}m", f"−{p_down:.0f}m", f"{net_avail:.0f}m",
              f"−{u_down:.0f}m", f"{net_op:.0f}m", f"−{perf_loss:.0f}m",
              f"{ideal_op:.0f}m", f"−{lost_q:.0f}m", f"{fully_prod:.0f}m"],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono, monospace", size=11, color="#e6edf3"),
        decreasing=dict(marker=dict(color=COLOR_RED,   line=dict(color=COLOR_RED,   width=0))),
        increasing=dict(marker=dict(color=COLOR_AVAIL, line=dict(color=COLOR_AVAIL, width=0))),
        totals=dict(marker=dict(color=COLOR_OEE,       line=dict(color=COLOR_OEE,   width=0))),
        connector=dict(line=dict(color=COLOR_GREY, width=1, dash="dot"))
    ))
    fig_wf.update_layout(**PLOTLY_LAYOUT, height=520, yaxis_title="Minutes")
    fig_wf.update_xaxes(tickangle=-20)
    st.plotly_chart(fig_wf, use_container_width=True)

    # Six Big Losses (unchanged)
    st.markdown("<div class='section-header'>Six Big Losses Classification</div>", unsafe_allow_html=True)

    total_defects      = float(row['Total Quantity Defective'])
    startup_scrap      = total_defects * 0.05
    process_defects    = total_defects - startup_scrap
    micro_stop_time    = perf_loss * 0.15
    reduced_speed_time = perf_loss * 0.85

    six_losses = [
        (1, "AVAILABILITY", "#F75555", "rgba(247,85,85,0.12)", "Equipment Failure",
         u_down, "min", f"{u_down/sched*100:.1f}% of scheduled time" if sched > 0 else "—"),
        (2, "AVAILABILITY", "#F75555", "rgba(247,85,85,0.08)", "Setup & Adjustments",
         p_down, "min", f"{p_down/sched*100:.1f}% of scheduled time" if sched > 0 else "—"),
        (3, "PERFORMANCE", "#F7A83A", "rgba(247,168,58,0.12)", "Idling & Micro-Stops",
         micro_stop_time, "min", f"≈15% of speed loss ({perf_loss:.0f}min total)"),
        (4, "PERFORMANCE", "#F7A83A", "rgba(247,168,58,0.08)", "Reduced Speed",
         reduced_speed_time, "min", f"≈85% of speed loss ({perf_loss:.0f}min total)"),
        (5, "QUALITY", "#A78BFA", "rgba(167,139,250,0.12)", "Process Defects",
         process_defects, "units", f"{process_defects/total_defects*100:.0f}% of total defects" if total_defects > 0 else "—"),
        (6, "QUALITY", "#A78BFA", "rgba(167,139,250,0.08)", "Startup / Reduced Yield",
         startup_scrap, "units", f"≈5% of total defects ({total_defects:.0f} total)"),
    ]

    col_a, col_b, col_c = st.columns(3)
    col_map = {0: col_a, 1: col_a, 2: col_b, 3: col_b, 4: col_c, 5: col_c}
    for idx, (num, pillar, p_color, bg, name, value, unit, sub) in enumerate(six_losses):
        with col_map[idx]:
            st.markdown(f"""
            <div class='six-loss-card' style='background:{bg}; border-color:{p_color}33; margin-bottom:10px;'>
                <span class='six-loss-pillar' style='background:{p_color}22; color:{p_color};'>
                    Loss #{num} · {pillar}
                </span>
                <div class='six-loss-name'>{name}</div>
                <div class='six-loss-value' style='color:{p_color};'>{value:.1f}
                    <span style='font-size:13px; font-weight:400; color:#8b949e;'>{unit}</span>
                </div>
                <div class='six-loss-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    # Loss decomposition table (unchanged)
    st.markdown("<div class='section-header'>Loss Decomposition Summary</div>", unsafe_allow_html=True)
    loss_data = {
        "Six Big Loss":    ["#1 Equipment Failure","#2 Setup & Adjustments",
                            "#3 Idling & Micro-Stops","#4 Reduced Speed",
                            "#5 Process Defects","#6 Startup Scrap"],
        "OEE Pillar":      ["Availability","Availability","Performance","Performance","Quality","Quality"],
        "Quantity":        [f"{u_down:.1f} min", f"{p_down:.1f} min",
                            f"{micro_stop_time:.1f} min", f"{reduced_speed_time:.1f} min",
                            f"{process_defects:.0f} units", f"{startup_scrap:.0f} units"],
        "% Sched. Time":   [
            f"{u_down/sched*100:.1f}%"           if sched > 0 else "—",
            f"{p_down/sched*100:.1f}%"           if sched > 0 else "—",
            f"{micro_stop_time/sched*100:.1f}%"  if sched > 0 else "—",
            f"{reduced_speed_time/sched*100:.1f}%" if sched > 0 else "—",
            "—", "—"
        ],
        "Financial Impact": [
            f"${u_down * (machine_rate+labor_rate)/60:,.0f}",
            f"${p_down * machine_rate/60:,.0f}",
            f"${micro_stop_time * machine_rate/60:,.0f}",
            f"${reduced_speed_time * machine_rate/60:,.0f}",
            f"${process_defects * part_value:,.0f}",
            f"${startup_scrap * part_value:,.0f}",
        ]
    }
    st.dataframe(pd.DataFrame(loss_data), use_container_width=True, hide_index=True)

    # ── NEW: Run vs Fleet Comparison mini-chart ───────────────────
    st.markdown("<div class='section-header'>This Run vs Fleet Average — Pillar Comparison</div>",
                unsafe_allow_html=True)
    fig_vs = go.Figure()
    cats = ['Availability', 'Performance', 'Quality', 'OEE']
    run_vals  = [avail_r*100, perf_r*100, qual_r*100, oee_r*100]
    fleet_vals= [avg_avail*100, avg_perf*100, avg_qual*100, avg_oee*100]
    wc_vals   = [90, 95, 98, 85]
    fig_vs.add_trace(go.Bar(name=f'{target_shift}', x=cats, y=run_vals,
                             marker_color=COLOR_OEE, opacity=0.9,
                             text=[f"{v:.1f}%" for v in run_vals], textposition='outside',
                             textfont=dict(color="#e6edf3", size=11)))
    fig_vs.add_trace(go.Bar(name='Fleet Average', x=cats, y=fleet_vals,
                             marker_color=COLOR_GREY, opacity=0.9,
                             text=[f"{v:.1f}%" for v in fleet_vals], textposition='outside',
                             textfont=dict(color="#8b949e", size=11)))
    fig_vs.add_trace(go.Scatter(name='World-Class Target', x=cats, y=wc_vals,
                                 mode='markers', marker=dict(color=COLOR_RED, size=10, symbol='line-ew',
                                 line=dict(color=COLOR_RED, width=3))))
    fig_vs.update_layout(**PLOTLY_LAYOUT, barmode='group', height=320,
                          yaxis_title="Efficiency (%)")
    fig_vs.update_yaxes(range=[0, 110])
    st.plotly_chart(fig_vs, use_container_width=True)


# ================================================================
# TAB 3 — IMPROVEMENT LEVERS (unchanged)
# ================================================================
with tab_levers:
    st.markdown("<div class='section-header' style='margin-top:0;'>Prescriptive Improvement Playbook</div>",
                unsafe_allow_html=True)

    def avail_lever(val):
        if val < 0.80:
            return dict(severity="critical", prio=1,
                        header="🔴 Critical: Turnkey SMED Intervention Required",
                        css_class="alert-critical", badge_color=COLOR_RED,
                        body=("Availability has collapsed below 80% — this asset is a primary production constraint. "
                              "Immediate capital escalation is required: procure a dedicated SMED consulting team, "
                              "conduct a full breakdown mode analysis (FMEA), and fast-track spare-parts inventory stocking. "
                              "Consider redundant asset procurement or temporary capacity leasing to protect downstream SLAs."))
        elif val < 0.90:
            return dict(severity="warning", prio=2,
                        header="🟡 Targeted: CMMS Synchronisation Programme",
                        css_class="alert-warning", badge_color=COLOR_PERF,
                        body=("Availability is degraded in the 80–90% band. "
                              "Decompose changeover steps into Internal vs External activities and stage tooling, fixtures, "
                              "and parameters while the asset is still running. Deploy CMMS-driven predictive maintenance "
                              "triggers with vibration/thermal sensors to catch failure precursors before breakdown events occur."))
        return None

    def perf_lever(val):
        if val < 0.75:
            return dict(severity="critical", prio=1,
                        header="🔴 Critical: Emergency Throughput Recovery — PLC Parameter Audit",
                        css_class="alert-critical", badge_color=COLOR_RED,
                        body=("Performance is critically below 75%. Asset is running at deeply sub-optimal speed. "
                              "Conduct an emergency PLC/HMI parameter audit — cycle times may have been manually overridden. "
                              "Deploy a dedicated andon system and short-interval control boards to surface and escalate "
                              "every micro-stop event within minutes. Engage maintenance and engineering concurrently."))
        elif val < 0.95:
            return dict(severity="warning", prio=2,
                        header="🟡 Targeted: Cycle Lock, SOP Standardisation & Micro-Stop Elimination",
                        css_class="alert-warning", badge_color=COLOR_PERF,
                        body=("Equipment throughput is below nameplate capacity. "
                              "Lock ideal cycle time parameters directly into PLC/HMI control logic to prevent operator-driven "
                              "slowing. Deploy TPM short-interval controls and live andon boards to surface micro-stop root "
                              "causes within the shift, and track OPF (One-Point Feedback) for recurring patterns."))
        return None

    def qual_lever(val):
        if val < 0.90:
            return dict(severity="critical", prio=1,
                        header="🔴 Critical: Containment & Root Cause Isolation — Quality Hold Protocol",
                        css_class="alert-critical", badge_color=COLOR_RED,
                        body=("Quality has fallen below 90% — a product quality hold may be warranted. "
                              "Immediately activate containment: 100% inspection at the output gate, segregate suspect batches, "
                              "and escalate to your quality engineering team for urgent 8D root cause analysis. "
                              "Deploy automated vision inspection or CMM verification if available."))
        elif val < 0.98:
            return dict(severity="warning", prio=2,
                        header="🟡 Targeted: Poka-Yoke Mistake-Proofing & Inline SPC Controls",
                        css_class="alert-warning", badge_color=COLOR_QUAL,
                        body=("Scrap and rework events are consuming productive machine time. "
                              "Deploy structural Poka-Yoke positioning pins, vision check arrays, or weight-check gates at source. "
                              "Introduce inline SPC control charts with auto-alert thresholds to detect process drift "
                              "before defects are produced. Link defect codes to specific shift patterns or operators."))
        return None

    levers = [l for l in [avail_lever(avg_avail), perf_lever(avg_perf), qual_lever(avg_qual)] if l]
    levers.sort(key=lambda k: k['prio'])

    if not levers:
        st.markdown("""
        <div style='background:rgba(61,214,140,0.08); border:1px solid #3DD68C; border-radius:8px;
                    padding:24px; text-align:center;'>
            <div style='font-size:28px; margin-bottom:8px;'>✅</div>
            <div style='font-family: IBM Plex Mono, monospace; font-size:14px; color:#3DD68C; font-weight:600;'>
                All metrics exceed world-class thresholds.</div>
            <div style='font-size:13px; color:#8b949e; margin-top:6px;'>
                Continue monitoring for sustainability and further optimisation opportunities.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for lv in levers:
            cur_val = avg_avail
            tgt_val = 0.90
            for mk, cur, tgt in [("Availability", avg_avail, 0.90),
                                   ("Performance",  avg_perf,  0.95),
                                   ("Quality",      avg_qual,  0.98)]:
                if mk.lower() in lv['header'].lower() or mk.lower() in lv['body'].lower()[:60]:
                    cur_val = cur; tgt_val = tgt; break
            gap = (tgt_val - cur_val) * 100
            st.markdown(f"""
            <div class='{lv["css_class"]}'>
                <div class='alert-title'>{lv['header']}</div>
                <div style='font-family: IBM Plex Mono, monospace; font-size: 11px; color:#8b949e; margin-bottom:8px;'>
                    Current: <strong>{cur_val*100:.1f}%</strong> &nbsp;·&nbsp;
                    Target: <strong>{tgt_val*100:.0f}%</strong> &nbsp;·&nbsp;
                    Gap: <strong style='color:{lv["badge_color"]};'>{gap:.1f}pp</strong>
                </div>
                <div class='alert-body'>{lv['body']}</div>
            </div>""", unsafe_allow_html=True)

    # Radar (unchanged)
    st.markdown("<div class='section-header'>OEE Pillar Health Radar</div>", unsafe_allow_html=True)
    radar_cats = ['Availability', 'Performance', 'Quality', 'Availability']
    values_cur = [avg_avail*100, avg_perf*100, avg_qual*100, avg_avail*100]
    values_wc  = [90, 95, 98, 90]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=values_wc, theta=radar_cats, fill='toself',
                                        name='World-Class Target',
                                        line=dict(color=COLOR_RED, dash='dash'),
                                        fillcolor='rgba(247,85,85,0.06)'))
    fig_radar.add_trace(go.Scatterpolar(r=values_cur, theta=radar_cats, fill='toself',
                                        name='Current Performance',
                                        line=dict(color=COLOR_OEE, width=2),
                                        fillcolor='rgba(79,142,247,0.15)'))
    fig_radar.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True, range=[0,100], gridcolor=COLOR_GREY,
                                   tickfont=dict(color="#8b949e", size=10)),
                   angularaxis=dict(gridcolor=COLOR_GREY, tickfont=dict(color="#e6edf3", size=12))),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(bgcolor="rgba(22,27,34,0.8)", bordercolor=COLOR_GREY, borderwidth=1, font=dict(size=11)),
        height=380
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Donut + cost cards (unchanged)
    st.markdown("<div class='section-header'>Fleet Financial Leakage Breakdown</div>", unsafe_allow_html=True)
    cost_cols = st.columns(2)
    with cost_cols[0]:
        fig_donut = go.Figure(go.Pie(
            labels=['Unplanned Downtime','Planned Downtime','Speed / Perf Loss','Scrap / Rework'],
            values=[total_unplanned_cost, total_planned_cost, total_speed_cost, total_scrap_cost],
            hole=0.55,
            marker=dict(colors=[COLOR_RED, COLOR_GREY, COLOR_PERF, COLOR_QUAL],
                        line=dict(color='#0d1117', width=2)),
            textfont=dict(family="IBM Plex Mono, monospace", size=11),
            textinfo='percent+label'
        ))
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8b949e", family="IBM Plex Mono, monospace"),
            showlegend=False, height=300, margin=dict(t=20, b=20, l=20, r=20),
            annotations=[dict(text=f"${total_leakage:,.0f}", x=0.5, y=0.5,
                              font=dict(size=16, color="#e6edf3", family="IBM Plex Mono, monospace"),
                              showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    with cost_cols[1]:
        for label, val, color in [
            ("Unplanned Downtime", total_unplanned_cost, COLOR_RED),
            ("Planned Downtime",   total_planned_cost,   COLOR_GREY),
            ("Speed / Perf Loss",  total_speed_cost,     COLOR_PERF),
            ("Scrap / Rework",     total_scrap_cost,     COLOR_QUAL),
            ("TOTAL LEAKAGE",      total_leakage,        "#e6edf3"),
        ]:
            border = "2px solid #e6edf3" if label == "TOTAL LEAKAGE" else f"1px solid {color}44"
            st.markdown(f"""
            <div class='cost-card' style='border-left-color:{color}; border:{border}; margin-top:6px;'>
                <div class='cost-label'>{label}</div>
                <div class='cost-value' style='color:{color};'>${val:,.0f}</div>
            </div>""", unsafe_allow_html=True)


# ================================================================
# TAB 4 — FINANCIAL SIMULATOR (unchanged)
# ================================================================
with tab_simulator:
    st.markdown("<div class='section-header' style='margin-top:0;'>What-If Financial & Capacity Simulator</div>",
                unsafe_allow_html=True)

    current_unplanned = float(df['Unplanned Downtime'].sum())
    current_produced  = float(df['Total Quantity Produced'].sum())
    current_scrap     = float(df['Total Quantity Defective'].sum())
    total_net_avail   = float(df['Net Available Time'].sum())

    inp_col, out_col = st.columns([1, 1], gap="large")

    with inp_col:
        st.markdown("""<div style='font-family: IBM Plex Mono, monospace; font-size: 11px; font-weight: 700;
            letter-spacing: 0.12em; color: #8b949e; text-transform: uppercase; margin-bottom: 16px;'>
            Simulate Improvements</div>""", unsafe_allow_html=True)

        downtime_red   = st.slider("Unplanned Downtime Reduction:", 0, 100, 20, format="%d%%",
                                    help="% reduction in unplanned breakdown hours across all runs")
        scrap_red      = st.slider("Scrap Rate Reduction:", 0, 100, 30, format="%d%%",
                                    help="% reduction in total defective units")
        speed_loss_red = st.slider("Speed / Performance Loss Reduction:", 0, 100, 25, format="%d%%",
                                    help="% reduction in performance loss minutes")

        st.markdown(f"""
        <div style='background:#1c2230; border:1px solid #30363d; border-radius:8px;
                    padding:14px 18px; margin-top:12px;'>
            <div style='font-family: IBM Plex Mono, monospace; font-size:10px; color:#8b949e;
                        letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px;'>Cost Parameters (from sidebar)</div>
            <div style='font-family: IBM Plex Mono, monospace; font-size:12px; color:#e6edf3; line-height:1.8;'>
                Part Value: <strong>${part_value:.2f}</strong><br>
                Machine Rate: <strong>${machine_rate:.2f}/hr</strong><br>
                Labor Rate: <strong>${labor_rate:.2f}/hr</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    with out_col:
        st.markdown("""<div style='font-family: IBM Plex Mono, monospace; font-size: 11px; font-weight: 700;
            letter-spacing: 0.12em; color: #8b949e; text-transform: uppercase; margin-bottom: 16px;'>
            Projected Returns</div>""", unsafe_allow_html=True)

        sim_unplanned  = current_unplanned * (1 - downtime_red / 100)
        sim_scrap      = current_scrap * (1 - scrap_red / 100)
        sim_perf_loss  = float(df['Performance Loss Time'].sum()) * (1 - speed_loss_red / 100)
        sim_net_op     = total_net_avail - sim_unplanned
        sim_good_units = current_produced - sim_scrap
        sim_avail      = sim_net_op / total_net_avail if total_net_avail > 0 else 0
        sim_qual       = sim_good_units / current_produced if current_produced > 0 else 0
        sim_oee        = sim_avail * avg_perf * sim_qual
        oee_gain       = (sim_oee - avg_oee) * 100
        hours_recovered  = (current_unplanned - sim_unplanned) / 60
        extra_good_units = current_scrap - sim_scrap
        revenue_recovery = extra_good_units * part_value

        combined_rate      = machine_rate + labor_rate
        sim_cost_unplanned = sim_unplanned  * (combined_rate / 60)
        sim_cost_planned   = total_planned_cost
        sim_cost_speed     = sim_perf_loss  * (machine_rate / 60)
        sim_cost_scrap     = sim_scrap      * part_value
        sim_total_leakage  = sim_cost_unplanned + sim_cost_planned + sim_cost_speed + sim_cost_scrap
        leakage_saved      = total_leakage - sim_total_leakage

        results = [
            ("Projected OEE",      f"{sim_oee*100:.1f}%",        f"↑ +{oee_gain:.1f}pp from {avg_oee*100:.1f}%",                    COLOR_OEE),
            ("Availability (Sim)", f"{sim_avail*100:.1f}%",      f"Was {avg_avail*100:.1f}%",                                         COLOR_AVAIL),
            ("Time Reclaimed",     f"{hours_recovered:.1f} hrs", f"{hours_recovered*60:.0f} total minutes",                           COLOR_PERF),
            ("Scrap Units Saved",  f"{int(extra_good_units):,}", f"of {int(current_scrap):,} total scrap",                            COLOR_QUAL),
            ("Revenue Recovery",   f"${revenue_recovery:,.0f}",  f"@ ${part_value:.2f}/unit × {int(extra_good_units):,} units",       COLOR_AVAIL),
            ("Leakage Eliminated", f"${leakage_saved:,.0f}",     f"Residual leakage: ${sim_total_leakage:,.0f}",                      COLOR_RED),
        ]
        for label, val, sub, color in results:
            st.markdown(f"""
            <div class='sim-result-row'>
                <div>
                    <div style='font-family: IBM Plex Mono, monospace; font-size:11px; color:#8b949e;
                                letter-spacing:0.1em; text-transform:uppercase;'>{label}</div>
                    <div style='font-size:11px; color:#555d69; margin-top:2px;'>{sub}</div>
                </div>
                <div class='sim-result-value' style='color:{color};'>{val}</div>
            </div>""", unsafe_allow_html=True)

    # Financial leakage comparison chart (unchanged)
    st.markdown("<div class='section-header'>Baseline vs Simulated Financial Leakage</div>",
                unsafe_allow_html=True)
    loss_categories = ['Unplanned Downtime','Planned Downtime','Speed / Perf Loss','Scrap / Rework','TOTAL']
    baseline_costs  = [total_unplanned_cost, total_planned_cost, total_speed_cost, total_scrap_cost, total_leakage]
    simulated_costs = [sim_cost_unplanned, sim_cost_planned, sim_cost_speed, sim_cost_scrap, sim_total_leakage]

    fig_fin = go.Figure()
    fig_fin.add_trace(go.Bar(name='Baseline Leakage', x=loss_categories, y=baseline_costs,
                              marker_color=[COLOR_RED, COLOR_GREY, COLOR_PERF, COLOR_QUAL, "#F75555"],
                              opacity=0.5, text=[f"${v:,.0f}" for v in baseline_costs],
                              textposition='outside', textfont=dict(color="#8b949e", size=10)))
    fig_fin.add_trace(go.Bar(name='Simulated (Post-Improvement)', x=loss_categories, y=simulated_costs,
                              marker_color=[COLOR_RED, COLOR_GREY, COLOR_PERF, COLOR_QUAL, "#F75555"],
                              opacity=1.0, text=[f"${v:,.0f}" for v in simulated_costs],
                              textposition='outside', textfont=dict(color="#e6edf3", size=10)))
    fig_fin.update_layout(**PLOTLY_LAYOUT, barmode='group', height=380,
                           yaxis_title="Cost ($)", xaxis_title="Loss Category")
    fig_fin.update_yaxes(range=[0, max(baseline_costs) * 1.25])
    st.plotly_chart(fig_fin, use_container_width=True)

    # Cost savings waterfall (unchanged)
    st.markdown("<div class='section-header'>Cost Savings Breakdown</div>", unsafe_allow_html=True)
    fig_sav = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute","relative","relative","relative","relative","total"],
        x=["Baseline Leakage","↓ Unplanned DT","↓ Speed Loss","↓ Scrap","Planned DT (unchanged)","Residual Leakage"],
        y=[total_leakage,
           -(total_unplanned_cost - sim_cost_unplanned),
           -(total_speed_cost     - sim_cost_speed),
           -(total_scrap_cost     - sim_cost_scrap),
           0, 0],
        text=[f"${total_leakage:,.0f}",
              f"-${total_unplanned_cost - sim_cost_unplanned:,.0f}",
              f"-${total_speed_cost     - sim_cost_speed:,.0f}",
              f"-${total_scrap_cost     - sim_cost_scrap:,.0f}",
              "No change", f"${sim_total_leakage:,.0f}"],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono, monospace", size=11, color="#e6edf3"),
        decreasing=dict(marker=dict(color=COLOR_AVAIL, line=dict(color=COLOR_AVAIL, width=0))),
        increasing=dict(marker=dict(color=COLOR_RED,   line=dict(color=COLOR_RED,   width=0))),
        totals=dict(marker=dict(color=COLOR_OEE,       line=dict(color=COLOR_OEE,   width=0))),
        connector=dict(line=dict(color=COLOR_GREY, width=1, dash="dot"))
    ))
    fig_sav.update_layout(**PLOTLY_LAYOUT, height=420, yaxis_title="Cost ($)")
    fig_sav.update_xaxes(tickangle=-15)
    st.plotly_chart(fig_sav, use_container_width=True)

    # OEE comparison chart (unchanged)
    st.markdown("<div class='section-header'>Baseline vs Simulated OEE Pillars</div>", unsafe_allow_html=True)
    categories_bar = ['OEE', 'Availability', 'Performance', 'Quality']
    baseline_vals  = [avg_oee*100, avg_avail*100, avg_perf*100, avg_qual*100]
    simulated_vals = [sim_oee*100, sim_avail*100, avg_perf*100, sim_qual*100]
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name='Baseline', x=categories_bar, y=baseline_vals,
                               marker_color=COLOR_GREY, text=[f"{v:.1f}%" for v in baseline_vals],
                               textposition='outside', textfont=dict(color="#8b949e", size=11)))
    fig_comp.add_trace(go.Bar(name='Simulated', x=categories_bar, y=simulated_vals,
                               marker_color=COLOR_OEE, text=[f"{v:.1f}%" for v in simulated_vals],
                               textposition='outside', textfont=dict(color="#e6edf3", size=11)))
    fig_comp.update_layout(**PLOTLY_LAYOUT, barmode='group', height=340, yaxis_title="Efficiency (%)")
    fig_comp.update_yaxes(range=[0, 110])
    st.plotly_chart(fig_comp, use_container_width=True)


# ----------------------------------------------------------------
# RAW DATA EXPANDER
# ----------------------------------------------------------------
st.markdown("<hr style='border-color:#21262d; margin: 32px 0 16px 0;'>", unsafe_allow_html=True)
with st.expander("🔍 Raw Data Matrix"):
    display_cols = [c for c in [
        'Run ID', 'Scheduled Production Time', 'Planned Downtime', 'Unplanned Downtime',
        'Net Available Time', 'Net Operating Time', 'Total Quantity Produced', 'Total Quantity Defective',
        'Availability (A)', 'Performance (P)', 'Quality (Q)', 'OEE (A × P × Q)', 'TEEP',
        'Cost: Planned Downtime', 'Cost: Unplanned Downtime', 'Cost: Speed / Perf Loss',
        'Cost: Scrap / Rework', 'Total Financial Leakage'
    ] if c in df.columns]
    fmt = {
        'Availability (A)': '{:.1%}', 'Performance (P)': '{:.1%}',
        'Quality (Q)': '{:.1%}', 'OEE (A × P × Q)': '{:.1%}', 'TEEP': '{:.1%}',
        'Cost: Planned Downtime': '${:.0f}', 'Cost: Unplanned Downtime': '${:.0f}',
        'Cost: Speed / Perf Loss': '${:.0f}', 'Cost: Scrap / Rework': '${:.0f}',
        'Total Financial Leakage': '${:.0f}'
    }
    st.dataframe(df[display_cols].style.format(fmt), use_container_width=True, hide_index=True)
