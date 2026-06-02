import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

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
# GLOBAL CSS — INDUSTRIAL PRECISION THEME
# ----------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

    /* Root theme */
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

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Dark app background */
    .stApp {
        background-color: var(--bg-primary);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-secondary);
        border-bottom: 1px solid var(--border);
        gap: 0px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary) !important;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 12px 24px;
        border: none;
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

    /* Metric cards */
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px 22px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
    }
    .kpi-card.blue::before  { background: var(--accent-blue); }
    .kpi-card.green::before { background: var(--accent-green); }
    .kpi-card.red::before   { background: var(--accent-red); }
    .kpi-card.purple::before{ background: var(--accent-purple); }

    .kpi-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 32px;
        font-weight: 600;
        line-height: 1;
        margin-bottom: 6px;
    }
    .kpi-sub {
        font-size: 11px;
        color: var(--text-secondary);
        font-family: 'IBM Plex Mono', monospace;
    }
    .kpi-delta-good { color: var(--accent-green); }
    .kpi-delta-bad  { color: var(--accent-red); }

    /* Lever cards */
    .lever-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 22px 24px;
        margin-bottom: 14px;
    }
    .lever-badge {
        display: inline-block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 3px;
        margin-bottom: 10px;
    }
    .lever-title {
        font-size: 15px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 8px 0 6px 0;
    }
    .lever-stat {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }
    .lever-body {
        font-size: 13px;
        color: #a0aab4;
        line-height: 1.6;
    }

    /* Section headers */
    .section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--text-secondary);
        border-bottom: 1px solid var(--border);
        padding-bottom: 8px;
        margin: 24px 0 18px 0;
    }

    /* Page title band */
    .page-title-band {
        background: linear-gradient(135deg, #161b22 0%, #1c2230 100%);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 24px 28px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .page-title-band h1 {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 22px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    .page-title-band p {
        font-size: 13px;
        color: var(--text-secondary);
        margin: 4px 0 0 0;
    }

    /* Simulator result row */
    .sim-result-row {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 18px 22px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .sim-result-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        color: var(--text-secondary);
    }
    .sim-result-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 16px;
        font-weight: 600;
        color: var(--accent-green);
    }

    /* Plotly chart container */
    .stPlotlyChart {
        background-color: transparent !important;
    }

    /* File uploader + selectbox */
    .stFileUploader, .stSelectbox, .stMultiSelect {
        background-color: var(--bg-card) !important;
        border-color: var(--border) !important;
    }
    label { color: var(--text-secondary) !important; }

    /* Sliders */
    .stSlider > div { color: var(--text-primary) !important; }

    /* Success/warning/info boxes */
    .stSuccess { background-color: rgba(61,214,140,0.1) !important; border-color: var(--accent-green) !important; }
    .stWarning { background-color: rgba(247,168,58,0.1) !important; border-color: var(--accent-amber) !important; }

    /* Expander */
    .stExpander { background-color: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }

    /* Dataframe */
    .stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px !important; }
    
    /* Sidebar uploader label */
    [data-testid="stSidebar"] .stCheckbox label { color: var(--text-primary) !important; }

    /* Number input */
    .stNumberInput input { background-color: var(--bg-card) !important; color: var(--text-primary) !important; border-color: var(--border) !important; }
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
    legend=dict(
        bgcolor="rgba(22,27,34,0.8)",
        bordercolor="#30363d",
        borderwidth=1,
        font=dict(size=11)
    )
)

COLOR_OEE    = "#4F8EF7"
COLOR_AVAIL  = "#3DD68C"
COLOR_PERF   = "#F7A83A"
COLOR_QUAL   = "#A78BFA"
COLOR_RED    = "#F75555"
COLOR_GREY   = "#30363d"


# ----------------------------------------------------------------
# DATA PIPELINE
# ----------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_bytes=None, filename=None, is_sample=False):
    if is_sample:
        np.random.seed(42)
        rows = 15
        sched_time = [480] * rows
        planned_down = np.random.randint(15, 35, size=rows)
        unplanned_down = np.random.randint(20, 85, size=rows)
        cycle_time = [80] * rows
        total_qty, defective_qty = [], []
        for i in range(rows):
            net_op_m = sched_time[i] - planned_down[i] - unplanned_down[i]
            max_possible = int((net_op_m * 60) / cycle_time[i])
            actual = int(max_possible * np.random.uniform(0.90, 0.99))
            scrap = int(actual * np.random.uniform(0.01, 0.05))
            total_qty.append(actual)
            defective_qty.append(scrap)
        data = {
            'Cycle Time (Seconds) Look Up / Override': cycle_time,
            'Scheduled Production Time': sched_time,
            'Planned Downtime': planned_down,
            'Unplanned Downtime': unplanned_down,
            'Total Quantity Produced': total_qty,
            'Total Quantity Defective': defective_qty
        }
        df = pd.DataFrame(data)
    else:
        import io
        buf = io.BytesIO(file_bytes)
        if filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(buf)
        else:
            df = pd.read_csv(buf)

    df = df.dropna(how='all')
    df.columns = [str(c).replace('\n', ' ').replace('  ', ' ').strip().replace('"', '') for c in df.columns]

    target_cols = [
        'Cycle Time (Seconds) Look Up / Override',
        'Scheduled Production Time',
        'Planned Downtime',
        'Unplanned Downtime',
        'Total Quantity Produced',
        'Total Quantity Defective'
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

    # Derived columns
    df['Net Available Time']  = df['Scheduled Production Time'] - df['Planned Downtime']
    df['Net Operating Time']  = df['Net Available Time'] - df['Unplanned Downtime']
    df['Ideal Operating Time']= (df['Total Quantity Produced'] * df['Cycle Time (Seconds) Look Up / Override']) / 60
    df['Lost Quality Time']   = (df['Total Quantity Defective'] * df['Cycle Time (Seconds) Look Up / Override']) / 60

    df['Availability (A)'] = np.where(df['Net Available Time'] > 0, df['Net Operating Time'] / df['Net Available Time'], 0)
    df['Performance (P)']  = np.where(df['Net Operating Time'] > 0, df['Ideal Operating Time'] / df['Net Operating Time'], 0)
    df['Quality (Q)']      = np.where(df['Total Quantity Produced'] > 0,
                                       (df['Total Quantity Produced'] - df['Total Quantity Defective']) / df['Total Quantity Produced'], 0)
    df['OEE (A × P × Q)'] = df['Availability (A)'] * df['Performance (P)'] * df['Quality (Q)']

    for p_col in ['Availability (A)', 'Performance (P)', 'Quality (Q)', 'OEE (A × P × Q)']:
        df[p_col] = df[p_col].clip(0.0, 1.0)

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

    uploaded_file = st.file_uploader("Upload Production Log", type=["csv", "xlsx"], help="Accepts .csv or .xlsx factory data exports")
    use_sample    = st.checkbox("Use sample dataset", value=(uploaded_file is None))

    if uploaded_file is not None:
        raw_df = load_and_clean_data(
            file_bytes=uploaded_file.read(),
            filename=uploaded_file.name,
            is_sample=False
        )
        data_source_label = f"📂 {uploaded_file.name}"
    elif use_sample:
        raw_df = load_and_clean_data(is_sample=True)
        data_source_label = "🧪 Sample Dataset (15 Runs)"
    else:
        st.info("Upload a production log or enable the sample dataset to begin.")
        st.stop()

    st.markdown("<hr style='border-color: #30363d; margin: 16px 0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-family: IBM Plex Mono, monospace; font-size: 10px; font-weight: 700; letter-spacing: 0.15em; color: #8b949e; text-transform: uppercase; margin-bottom: 10px;'>Run Selection Filter</div>", unsafe_allow_html=True)

    all_runs = raw_df['Run ID'].tolist()
    selected_runs = st.multiselect("Runs to include:", options=all_runs, default=all_runs, label_visibility="collapsed")

    if not selected_runs:
        st.warning("Select at least one run to continue.")
        st.stop()

    df = raw_df[raw_df['Run ID'].isin(selected_runs)].reset_index(drop=True)

    st.markdown(f"""
    <hr style='border-color: #30363d; margin: 16px 0;'>
    <div style='font-family: IBM Plex Mono, monospace; font-size: 10px; color: #8b949e; letter-spacing: 0.08em;'>
        SOURCE<br>
        <span style='color: #e6edf3;'>{data_source_label}</span>
    </div>
    <div style='font-family: IBM Plex Mono, monospace; font-size: 10px; color: #8b949e; letter-spacing: 0.08em; margin-top: 8px;'>
        SELECTED RUNS<br>
        <span style='color: #e6edf3;'>{len(df)} / {len(raw_df)}</span>
    </div>
    """, unsafe_allow_html=True)


# ----------------------------------------------------------------
# PRE-COMPUTE FLEET AVERAGES  (used across all tabs)
# ----------------------------------------------------------------
avg_oee   = float(df['OEE (A × P × Q)'].mean())
avg_avail = float(df['Availability (A)'].mean())
avg_perf  = float(df['Performance (P)'].mean())
avg_qual  = float(df['Quality (Q)'].mean())


# ----------------------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------------------
st.markdown(f"""
<div class='page-title-band'>
    <div style='width:44px; height:44px; background: linear-gradient(135deg,#4F8EF7,#A78BFA); border-radius:8px;
                display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0;'>🏭</div>
    <div>
        <h1>OEE Intelligence Platform</h1>
        <p>Overall Equipment Effectiveness · Waterfall Diagnostics · Improvement Levers · What-If Simulator</p>
    </div>
    <div style='margin-left:auto; text-align:right;'>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 28px; font-weight: 700;
                    color: {"#3DD68C" if avg_oee >= 0.85 else "#F7A83A" if avg_oee >= 0.65 else "#F75555"};'>
            {avg_oee*100:.1f}%
        </div>
        <div style='font-family: IBM Plex Mono, monospace; font-size: 10px; color: #8b949e; letter-spacing:0.1em;'>FLEET OEE</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------
# TABS
# ----------------------------------------------------------------
tab_summary, tab_waterfall, tab_levers, tab_simulator = st.tabs([
    "PERFORMANCE TRENDS",
    "WATERFALL DIAGNOSTIC",
    "IMPROVEMENT LEVERS",
    "WHAT-IF SIMULATOR",
])


# ================================================================
# TAB 1 — PERFORMANCE TRENDS
# ================================================================
with tab_summary:

    # ── KPI Row ──────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)

    def delta_vs_target(val, target):
        diff = (val - target) * 100
        sign = "+" if diff >= 0 else ""
        cls = "kpi-delta-good" if diff >= 0 else "kpi-delta-bad"
        return f"<span class='{cls}'>{sign}{diff:.1f}% vs target</span>"

    with k1:
        st.markdown(f"""
        <div class='kpi-card blue'>
            <div class='kpi-label'>Overall OEE</div>
            <div class='kpi-value' style='color:#4F8EF7;'>{avg_oee*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_oee, 0.85)}</div>
        </div>""", unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class='kpi-card green'>
            <div class='kpi-label'>Availability</div>
            <div class='kpi-value' style='color:#3DD68C;'>{avg_avail*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_avail, 0.90)}</div>
        </div>""", unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class='kpi-card red'>
            <div class='kpi-label'>Performance</div>
            <div class='kpi-value' style='color:#F7A83A;'>{avg_perf*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_perf, 0.95)}</div>
        </div>""", unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class='kpi-card purple'>
            <div class='kpi-label'>Quality Yield</div>
            <div class='kpi-value' style='color:#A78BFA;'>{avg_qual*100:.1f}%</div>
            <div class='kpi-sub'>{delta_vs_target(avg_qual, 0.98)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-header' style='margin-top:32px;'>Run-Over-Run Trend Analysis</div>", unsafe_allow_html=True)

    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(
        x=df['Run ID'], y=df['OEE (A × P × Q)'] * 100,
        name='OEE', line=dict(color=COLOR_OEE, width=3),
        fill='tozeroy', fillcolor='rgba(79,142,247,0.06)'
    ))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['Availability (A)'] * 100, name='Availability', line=dict(color=COLOR_AVAIL, width=1.5, dash='dash')))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['Performance (P)'] * 100, name='Performance', line=dict(color=COLOR_PERF, width=1.5, dash='dot')))
    fig_trends.add_trace(go.Scatter(x=df['Run ID'], y=df['Quality (Q)'] * 100, name='Quality', line=dict(color=COLOR_QUAL, width=1.5, dash='longdash')))
    fig_trends.add_hline(y=85, line_dash="dash", line_color="#F75555", line_width=1,
                         annotation_text="World-Class Target (85%)", annotation_font_color="#F75555", annotation_font_size=11)
    
    # FIX APPLIED HERE: Split update_layout and axis bounds constraints into separate safe pipeline commands
    fig_trends.update_layout(**PLOTLY_LAYOUT, height=420, yaxis_title="Efficiency (%)", xaxis_title="Production Run")
    fig_trends.update_yaxes(range=[0, 105])
    
    st.plotly_chart(fig_trends, use_container_width=True)

    st.markdown("<div class='section-header'>Run-Level Breakdown</div>", unsafe_allow_html=True)

    fig_bar = go.Figure()
    for col, name, color in [
        ('Availability (A)', 'Availability', COLOR_AVAIL),
        ('Performance (P)', 'Performance', COLOR_PERF),
        ('Quality (Q)',      'Quality',      COLOR_QUAL),
    ]:
        fig_bar.add_trace(go.Bar(x=df['Run ID'], y=df[col] * 100, name=name,
                                  marker_color=color, opacity=0.85))
    fig_bar.add_trace(go.Scatter(x=df['Run ID'], y=df['OEE (A × P × Q)'] * 100,
                                  name='OEE', mode='markers+lines',
                                  marker=dict(color=COLOR_OEE, size=8, symbol='diamond'),
                                  line=dict(color=COLOR_OEE, width=2)))
    fig_bar.update_layout(**PLOTLY_LAYOUT, barmode='group', height=350,
                           yaxis_title="Efficiency (%)", xaxis_title="Production Run")
    st.plotly_chart(fig_bar, use_container_width=True)


# ================================================================
# TAB 2 — WATERFALL DIAGNOSTIC
# ================================================================
with tab_waterfall:
    st.markdown("<div class='section-header' style='margin-top:0;'>Capacity Loss Waterfall — Time-Drop Funnel</div>", unsafe_allow_html=True)

    target_shift = st.selectbox("Select Run to Diagnose:", options=df['Run ID'].tolist(), label_visibility="visible")
    row = df[df['Run ID'] == target_shift].iloc[0]

    sched     = float(row['Scheduled Production Time'])
    p_down    = float(row['Planned Downtime'])
    net_avail = float(row['Net Available Time'])
    u_down    = float(row['Unplanned Downtime'])
    net_op    = float(row['Net Operating Time'])
    ideal_op  = float(row['Ideal Operating Time'])
    lost_q    = float(row['Lost Quality Time'])
    perf_loss = max(0.0, net_op - ideal_op)
    fully_prod = max(0.0, ideal_op - lost_q)

    avail_r = float(row['Availability (A)'])
    perf_r  = float(row['Performance (P)'])
    qual_r  = float(row['Quality (Q)'])
    oee_r   = float(row['OEE (A × P × Q)'])

    # Mini KPI row for selected run
    r1, r2, r3, r4 = st.columns(4)
    for col_obj, label, val, color in [
        (r1, "Run OEE",       oee_r,   COLOR_OEE),
        (r2, "Availability",  avail_r, COLOR_AVAIL),
        (r3, "Performance",   perf_r,  COLOR_PERF),
        (r4, "Quality",       qual_r,  COLOR_QUAL),
    ]:
        with col_obj:
            st.markdown(f"""
            <div style='background:#1c2230; border:1px solid #30363d; border-radius:8px; padding:14px 18px; text-align:center;'>
                <div style='font-family: IBM Plex Mono, monospace; font-size:10px; color:#8b949e; letter-spacing:0.12em; text-transform:uppercase;'>{label}</div>
                <div style='font-family: IBM Plex Mono, monospace; font-size:26px; font-weight:700; color:{color}; margin-top:4px;'>{val*100:.1f}%</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "total", "relative", "total", "relative", "total", "relative", "total"],
        x=["Scheduled Time", "Planned Downtime", "Net Available", "Unplanned Breakdowns",
           "Net Operating", "Speed / Perf Loss", "Ideal Operating", "Quality / Scrap Loss", "Fully Productive"],
        y=[sched, -p_down, 0, -u_down, 0, -perf_loss, 0, -lost_q, 0],
        text=[f"{sched:.0f}m", f"−{p_down:.0f}m", f"{net_avail:.0f}m",
              f"−{u_down:.0f}m", f"{net_op:.0f}m", f"−{perf_loss:.0f}m",
              f"{ideal_op:.0f}m", f"−{lost_q:.0f}m", f"{fully_prod:.0f}m"],
        textposition="outside",
        textfont=dict(family="IBM Plex Mono, monospace", size=11, color="#e6edf3"),
        decreasing=dict(marker=dict(color=COLOR_RED, line=dict(color=COLOR_RED, width=0))),
        increasing=dict(marker=dict(color=COLOR_AVAIL, line=dict(color=COLOR_AVAIL, width=0))),
        totals=dict(marker=dict(color=COLOR_OEE, line=dict(color=COLOR_OEE, width=0))),
        connector=dict(line=dict(color=COLOR_GREY, width=1, dash="dot"))
    ))
    fig_wf.update_layout(**PLOTLY_LAYOUT, height=520,
                          yaxis_title="Minutes",
                          xaxis=dict(**PLOTLY_LAYOUT['xaxis'], tickangle=-20))
    st.plotly_chart(fig_wf, use_container_width=True)

    # Loss summary table
    st.markdown("<div class='section-header'>Loss Decomposition Summary</div>", unsafe_allow_html=True)
    loss_data = {
        "Loss Category": ["Planned Downtime", "Unplanned Breakdowns", "Speed / Performance Loss", "Quality / Scrap Loss"],
        "Minutes Lost": [p_down, u_down, perf_loss, lost_q],
        "% of Scheduled Time": [
            f"{p_down/sched*100:.1f}%" if sched > 0 else "—",
            f"{u_down/sched*100:.1f}%" if sched > 0 else "—",
            f"{perf_loss/sched*100:.1f}%" if sched > 0 else "—",
            f"{lost_q/sched*100:.1f}%" if sched > 0 else "—",
        ],
        "OEE Pillar Impact": ["Availability", "Availability", "Performance", "Quality"]
    }
    st.dataframe(pd.DataFrame(loss_data), use_container_width=True, hide_index=True)


# ================================================================
# TAB 3 — IMPROVEMENT LEVERS  
# ================================================================
with tab_levers:
    st.markdown("<div class='section-header' style='margin-top:0;'>Prescriptive Improvement Playbook</div>", unsafe_allow_html=True)

    # Thresholds
    AVAIL_TARGET = 0.90
    PERF_TARGET  = 0.95
    QUAL_TARGET  = 0.98

    levers = []

    if avg_avail < AVAIL_TARGET:
        levers.append(dict(
            prio=1 if avg_avail == min(avg_avail, avg_perf, avg_qual) else 2,
            metric="Availability", val=avg_avail, target=AVAIL_TARGET,
            color=COLOR_RED,
            title="SMED & Predictive Maintenance Programme",
            body=(
                "Unplanned downtime is the primary capacity thief. "
                "Decompose changeover steps into Internal vs External activities — stage tooling, fixtures, "
                "and parameters while the machine is still running the prior batch. "
                "Layer CMMS-driven predictive maintenance triggers to eliminate reactive breakdown events."
            )
        ))

    if avg_perf < PERF_TARGET:
        levers.append(dict(
            prio=1 if avg_perf == min(avg_avail, avg_perf, avg_qual) else 2,
            metric="Performance", val=avg_perf, target=PERF_TARGET,
            color=COLOR_PERF,
            title="Cycle Lock, SOP Standardisation & Micro-Stop Elimination",
            body=(
                "Equipment throughput rates are running below nameplate capacity. "
                "Lock cycle time parameters directly into PLC/HMI control logic to prevent operator-driven slowing. "
                "Deploy TPM short-interval controls and andon systems to surface and close micro-stop causes within the shift."
            )
        ))

    if avg_qual < QUAL_TARGET:
        levers.append(dict(
            prio=1 if avg_qual == min(avg_avail, avg_perf, avg_qual) else 2,
            metric="Quality", val=avg_qual, target=QUAL_TARGET,
            color=COLOR_QUAL,
            title="Poka-Yoke Mistake-Proofing & Inline SPC Controls",
            body=(
                "Scrap and rework events are consuming productive machine time. "
                "Deploy structural Poka-Yoke positioning pins, vision inspection arrays, or weight-check gates "
                "at source. Introduce inline SPC control charts with auto-alert thresholds to detect process drift "
                "before defects are produced."
            )
        ))

    levers.sort(key=lambda k: k['prio'])

    if not levers:
        st.markdown("""
        <div style='background:rgba(61,214,140,0.08); border:1px solid #3DD68C; border-radius:8px; padding:24px; text-align:center;'>
            <div style='font-size:28px; margin-bottom:8px;'>✅</div>
            <div style='font-family: IBM Plex Mono, monospace; font-size:14px; color:#3DD68C; font-weight:600;'>All metrics exceed world-class thresholds.</div>
            <div style='font-size:13px; color:#8b949e; margin-top:6px;'>Continue monitoring for sustainability and further optimisation opportunities.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for lv in levers:
            gap = (lv['target'] - lv['val']) * 100
            badge_bg = lv['color'] if lv['prio'] == 1 else "#30363d"
            st.markdown(f"""
            <div class='lever-card' style='border-top: 3px solid {lv["color"]};'>
                <span class='lever-badge' style='background:{badge_bg}; color:white;'>
                    P{lv['prio']} · {lv['metric'].upper()}
                </span>
                <div class='lever-title'>{lv['title']}</div>
                <div class='lever-stat'>
                    Current: <strong>{lv['val']*100:.1f}%</strong> &nbsp;·&nbsp;
                    Target: <strong>{lv['target']*100:.0f}%</strong> &nbsp;·&nbsp;
                    Gap: <strong style='color:{lv["color"]};'>{gap:.1f}pp</strong>
                </div>
                <div class='lever-body'>{lv['body']}</div>
            </div>""", unsafe_allow_html=True)

    # Fleet radar
    st.markdown("<div class='section-header'>OEE Pillar Health Radar</div>", unsafe_allow_html=True)
    categories = ['Availability', 'Performance', 'Quality', 'Availability']
    values_cur  = [avg_avail * 100, avg_perf * 100, avg_qual * 100, avg_avail * 100]
    values_wc   = [90, 95, 98, 90]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=values_wc, theta=categories, fill='toself',
                                        name='World-Class Target', line=dict(color=COLOR_RED, dash='dash'),
                                        fillcolor='rgba(247,85,85,0.06)'))
    fig_radar.add_trace(go.Scatterpolar(r=values_cur, theta=categories, fill='toself',
                                        name='Current Performance', line=dict(color=COLOR_OEE, width=2),
                                        fillcolor='rgba(79,142,247,0.15)'))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=COLOR_GREY, tickfont=dict(color="#8b949e", size=10)),
            angularaxis=dict(gridcolor=COLOR_GREY, tickfont=dict(color="#e6edf3", size=12))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(bgcolor="rgba(22,27,34,0.8)", bordercolor=COLOR_GREY, borderwidth=1, font=dict(size=11)),
        height=360
    )
    st.plotly_chart(fig_radar, use_container_width=True)


# ================================================================
# TAB 4 — WHAT-IF SIMULATOR
# ================================================================
with tab_simulator:
    st.markdown("<div class='section-header' style='margin-top:0;'>What-If Capacity & Revenue Simulator</div>", unsafe_allow_html=True)

    current_unplanned = float(df['Unplanned Downtime'].sum())
    current_produced  = float(df['Total Quantity Produced'].sum())
    current_scrap     = float(df['Total Quantity Defective'].sum())
    total_net_avail   = float(df['Net Available Time'].sum())

    inp_col, out_col = st.columns([1, 1], gap="large")

    with inp_col:
        st.markdown("<div style='font-family: IBM Plex Mono, monospace; font-size: 11px; font-weight: 700; letter-spacing: 0.12em; color: #8b949e; text-transform: uppercase; margin-bottom: 16px;'>Simulate Improvements</div>", unsafe_allow_html=True)

        downtime_red = st.slider("Unplanned Downtime Reduction:", min_value=0, max_value=100, value=20,
                                  format="%d%%", help="% reduction in unplanned breakdown hours across all runs")
        scrap_red    = st.slider("Scrap Rate Reduction:", min_value=0, max_value=100, value=30,
                                  format="%d%%", help="% reduction in total defective units")
        value_per_unit = st.number_input("Part Value ($ / unit):", min_value=0.0, value=12.50, step=0.50,
                                          help="Assumed revenue value per good finished part")

    with out_col:
        st.markdown("<div style='font-family: IBM Plex Mono, monospace; font-size: 11px; font-weight: 700; letter-spacing: 0.12em; color: #8b949e; text-transform: uppercase; margin-bottom: 16px;'>Projected Returns</div>", unsafe_allow_html=True)

        sim_unplanned   = current_unplanned * (1 - downtime_red / 100)
        sim_scrap       = current_scrap * (1 - scrap_red / 100)
        sim_net_op      = total_net_avail - sim_unplanned
        sim_good_units  = current_produced - sim_scrap

        sim_avail = sim_net_op / total_net_avail if total_net_avail > 0 else 0
        sim_qual  = sim_good_units / current_produced if current_produced > 0 else 0
        sim_oee   = sim_avail * avg_perf * sim_qual

        hours_recovered    = (current_unplanned - sim_unplanned) / 60
        extra_good_units   = current_scrap - sim_scrap
        revenue_recovery   = extra_good_units * value_per_unit
        oee_gain           = (sim_oee - avg_oee) * 100

        results = [
            ("Projected OEE",        f"{sim_oee*100:.1f}%",        f"↑ +{oee_gain:.1f}pp from baseline",  COLOR_OEE),
            ("Availability (Sim)",   f"{sim_avail*100:.1f}%",      f"Was {avg_avail*100:.1f}%",            COLOR_AVAIL),
            ("Time Reclaimed",       f"{hours_recovered:.1f} hrs", f"{hours_recovered*60:.0f} min total",  COLOR_PERF),
            ("Scrap Units Saved",    f"{int(extra_good_units):,}",  f"of {int(current_scrap):,} total scrap", COLOR_QUAL),
            ("Revenue Recovery",     f"${revenue_recovery:,.0f}",   f"@ ${value_per_unit:.2f}/unit",         COLOR_AVAIL),
        ]

        for label, val, sub, color in results:
            st.markdown(f"""
            <div class='sim-result-row'>
                <div>
                    <div style='font-family: IBM Plex Mono, monospace; font-size: 11px; color: #8b949e; letter-spacing: 0.1em; text-transform: uppercase;'>{label}</div>
                    <div style='font-size: 11px; color: #555d69; margin-top: 2px;'>{sub}</div>
                </div>
                <div class='sim-result-value' style='color:{color};'>{val}</div>
            </div>""", unsafe_allow_html=True)

    # Comparison bar chart
    st.markdown("<div class='section-header'>Baseline vs Simulated OEE Pillars</div>", unsafe_allow_html=True)

    categories_bar = ['OEE', 'Availability', 'Performance', 'Quality']
    baseline_vals  = [avg_oee * 100, avg_avail * 100, avg_perf * 100, avg_qual * 100]
    simulated_vals = [sim_oee * 100, sim_avail * 100, avg_perf * 100, sim_qual * 100]

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(name='Baseline', x=categories_bar, y=baseline_vals,
                               marker_color=COLOR_GREY, text=[f"{v:.1f}%" for v in baseline_vals],
                               textposition='outside', textfont=dict(color="#8b949e", size=11)))
    fig_comp.add_trace(go.Bar(name='Simulated', x=categories_bar, y=simulated_vals,
                               marker_color=COLOR_OEE, text=[f"{v:.1f}%" for v in simulated_vals],
                               textposition='outside', textfont=dict(color="#e6edf3", size=11)))
    fig_comp.update_layout(**PLOTLY_LAYOUT, barmode='group', height=340,
                            yaxis=dict(**PLOTLY_LAYOUT['yaxis'], range=[0, 110]),
                            yaxis_title="Efficiency (%)")
    st.plotly_chart(fig_comp, use_container_width=True)


# ----------------------------------------------------------------
# FOOTER — RAW DATA EXPANDER
# ----------------------------------------------------------------
st.markdown("<hr style='border-color:#21262d; margin: 32px 0 16px 0;'>", unsafe_allow_html=True)
with st.expander("🔍 Raw Data Matrix"):
    display_cols = [
        'Run ID', 'Scheduled Production Time', 'Planned Downtime', 'Unplanned Downtime',
        'Net Available Time', 'Net Operating Time', 'Total Quantity Produced', 'Total Quantity Defective',
        'Availability (A)', 'Performance (P)', 'Quality (Q)', 'OEE (A × P × Q)'
    ]
    display_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(
        df[display_cols].style.format({
            'Availability (A)': '{:.1%}',
            'Performance (P)': '{:.1%}',
            'Quality (Q)': '{:.1%}',
            'OEE (A × P × Q)': '{:.1%}',
        }),
        use_container_width=True,
        hide_index=True
    )
