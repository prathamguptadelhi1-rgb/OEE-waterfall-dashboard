import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ----------------------------------------------------------------
# PAGE CONFIGURATION & THEME PROFILE
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Enterprise OEE Performance Center",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom css for metric positioning and card structures
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #636EFA;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .lever-card {
        background-color: #ffffff;
        border-radius: 6px;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# DATA INGESTION & PIPELINE ENGINE
# ----------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_or_path, is_sample=False):
    if is_sample:
        # Generates a comprehensive multi-row template reflecting user's structural columns
        np.random.seed(42)
        rows = 15
        sched_time = [480] * rows
        planned_down = np.random.randint(15, 35, size=rows)
        unplanned_down = np.random.randint(20, 85, size=rows)
        cycle_time = [80] * rows
        
        total_qty = []
        defective_qty = []
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
        df = pd.read_csv(file_or_path)
        
    # Standardize column headers by wiping out newline flags
    df.columns = [col.replace('\n', ' ').replace('  ', ' ').strip() for col in df.columns]
    
    # Calculate downstream parameters dynamically if missing from input file mapping
    if 'Net Available Time' not in df.columns:
        df['Net Available Time'] = df['Scheduled Production Time'] - df['Planned Downtime']
    if 'Net Operating Time' not in df.columns:
        df['Net Operating Time'] = df['Net Available Time'] - df['Unplanned Downtime']
    if 'Ideal Operating Time' not in df.columns:
        df['Ideal Operating Time'] = (df['Total Quantity Produced'] * df['Cycle Time (Seconds) Look Up / Override']) / 60
    if 'Lost "Quality" Time' not in df.columns:
        df['Lost "Quality" Time'] = (df['Total Quantity Defective'] * df['Cycle Time (Seconds) Look Up / Override']) / 60
        
    # Pillar Ratios
    df['Availability (A)'] = df['Net Operating Time'] / df['Net Available Time']
    df['Performance (P)'] = df['Ideal Operating Time'] / df['Net Operating Time']
    df['Quality (Q)'] = (df['Total Quantity Produced'] - df['Total Quantity Defective']) / df['Total Quantity Produced']
    df['OEE (A * P * Q)'] = df['Availability (A)'] * df['Performance (P)'] * df['Quality (Q)']
    
    # Add sequential run designation index for tracking visualizations
    df.insert(0, 'Run ID', [f"Shift_Run_{i+1:02d}" for i in range(len(df))])
    return df

# ----------------------------------------------------------------
# SIDEBAR CONTROL NAVIGATION
# ----------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/external-flatart-icons-flat-flatarticons/128/external-factory-industry-flatart-icons-flat-flatarticons.png", width=70)
st.sidebar.title("OEE Control Center")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("Upload Factory Production Log (.CSV)", type=["csv"])
use_sample = st.sidebar.checkbox("Load Production Sample Environment", value=True if not uploaded_file else False)

if uploaded_file is not None:
    raw_df = load_and_clean_data(uploaded_file, is_sample=False)
elif use_sample:
    raw_df = load_and_clean_data(None, is_sample=True)
else:
    st.info("Please stage a valid operational template log to populate the processing canvas.")
    st.stop()

# Global Run filtering limits inside sidebar panel
st.sidebar.markdown("---")
st.sidebar.subheader("Global Canvas Filters")
selected_runs = st.sidebar.multiselect("Isolate Specific Assets / Runs", options=raw_df['Run ID'].tolist(), default=raw_df['Run ID'].tolist())
df_filtered = raw_df[raw_df['Run ID'].isin(selected_runs)].reset_index(drop=True)

if df_filtered.empty:
    st.warning("All parameters filtered out. Re-enable run components inside sidebar configuration.")
    st.stop()

# ----------------------------------------------------------------
# APPLICATION HEAD NAVIGATION TABS
# ----------------------------------------------------------------
tab_summary, tab_waterfall, tab_levers, tab_simulator = st.tabs([
    "📈 Performance Trends", 
    "📊 Waterfall Diagnostic", 
    "🛠️ Asset Improvement Levers", 
    "🎛️ Optimization Simulator"
])

# ----------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW & PERFORMANCE TRENDS
# ----------------------------------------------------------------
with tab_summary:
    st.subheader("Aggregate Factory Operational Performance")
    
    # Calculate global tracking averages
    avg_oee = df_filtered['OEE (A * P * Q)'].mean()
    avg_avail = df_filtered['Availability (A)'].mean()
    avg_perf = df_filtered['Performance (P)'].mean()
    avg_qual = df_filtered['Quality (Q)'].mean()
    
    # Dynamic Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-card'><strong>Global OEE Target (vs 85% Benchmark)</strong><br><span style='font-size:28px; font-weight:bold; color:#636EFA;'>{avg_oee*100:.2f}%</span></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><strong>Availability Index</strong><br><span style='font-size:28px; font-weight:bold; color:#00CC96;'>{avg_avail*100:.2f}%</span></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><strong>Performance Index</strong><br><span style='font-size:28px; font-weight:bold; color:#EF553B;'>{avg_perf*100:.2f}%</span></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='metric-card'><strong>Quality Yield Index</strong><br><span style='font-size:28px; font-weight:bold; color:#AB63FA;'>{avg_qual*100:.2f}%</span></div>", unsafe_allow_html=True)
        
    st.markdown("### Run-over-Run Optimization Roadmap Traces")
    
    # Generate timeline visualization plots via Express engine
    fig_trends = go.Figure()
    fig_trends.add_trace(go.Scatter(x=df_filtered['Run ID'], y=df_filtered['OEE (A * P * Q)']*100, name='Overall OEE', line=dict(color='#636EFA', width=4)))
    fig_trends.add_trace(go.Scatter(x=df_filtered['Run ID'], y=df_filtered['Availability (A)']*100, name='Availability', line=dict(color='#00CC96', dash='dash')))
    fig_trends.add_trace(go.Scatter(x=df_filtered['Run ID'], y=df_filtered['Performance (P)']*100, name='Performance', line=dict(color='#EF553B', dash='dot')))
    fig_trends.add_trace(go.Scatter(x=df_filtered['Run ID'], y=df_filtered['Quality (Q)']*100, name='Quality', line=dict(color='#AB63FA', dash='longdash')))
    
    fig_trends.add_hline(y=85.0, line_dash="dash", line_color="red", annotation_text="World Class Target Boundary (85%)")
    fig_trends.update_layout(yaxis_title="Efficiency Percentage (%)", xaxis_title="Production Batches / Asset Runs", height=450, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_trends, use_container_width=True)

# ----------------------------------------------------------------
# TAB 2: SHIFT OEE WATERFALL DEEP-DIVE
# ----------------------------------------------------------------
with tab_waterfall:
    st.subheader("Capacity Losses Deep-Dive (Time-Drop Funnel Map)")
    
    target_shift = st.selectbox("Select Target Run Asset to Isolate Vector Map:", options=df_filtered['Run ID'].tolist())
    row = df_filtered[df_filtered['Run ID'] == target_shift].iloc[0]
    
    # Time variables extract
    scheduled_production = row['Scheduled Production Time']
    planned_downtime = row['Planned Downtime']
    net_available = row['Net Available Time']
    unplanned_downtime = row['Unplanned Downtime']
    net_operating = row['Net Operating Time']
    ideal_operating = row['Ideal Operating Time']
    lost_quality_time = row['Lost "Quality" Time']
    
    # Calculate performance time losses explicitly
    performance_loss = net_operating - ideal_operating
    fully_productive = ideal_operating - lost_quality_time
    
    # Construct plotting metrics for core waterfall architecture
    x_steps = [
        "Scheduled Production", "Planned Downtime", "Net Available Time",
        "Unplanned Breakdowns", "Net Operating Time", "Performance Speed Losses",
        "Ideal Operating Time", "Scrap & Quality Defect Losses", "Fully Productive Time"
    ]
    
    y_values = [
        scheduled_production, -planned_downtime, 0,
        -unplanned_downtime, 0, -performance_loss,
        0, -lost_quality_time, 0
    ]
    
    measure_types = ["absolute", "relative", "total", "relative", "total", "relative", "total", "relative", "total"]
    
    text_labels = [
        f"{scheduled_production:.1f}m", f"-{planned_downtime:.1f}m", f"{net_available:.1f}m",
        f"-{unplanned_downtime:.1f}m", f"{net_operating:.1f}m", f"-{performance_loss:.1f}m",
        f"{ideal_operating:.1f}m", f"-{lost_quality_time:.1f}m", f"{fully_productive:.1f}m"
    ]
    
    fig_wf = go.Figure(go.Waterfall(
        orientation = "v",
        measure = measure_types,
        x = x_steps,
        y = y_values,
        text = text_labels,
        textposition = "outside",
        decreasing = {"marker":{"color": "#DC3545"}},
        increasing = {"marker":{"color": "#28A745"}},
        totals = {"marker":{"color": "#007BFF"}},
        connector = {"line":{"color":"#6c757d", "width":1}}
    ))
    
    fig_wf.update_layout(
        yaxis_title="Minutes Assigned",
        height=550,
        margin=dict(t=30, b=30, l=10, r=10),
        xaxis=dict(tickangle=-15)
    )
    st.plotly_chart(fig_wf, use_container_width=True)

# ----------------------------------------------------------------
# TAB 3: CONTINUOUS IMPROVEMENT (CI) LEVERS & PLAYBOOK ENGINE
# ----------------------------------------------------------------
with tab_levers:
    st.subheader("Prescriptive Engineering Interventions & Priorities")
    st.markdown("The system analyzes current runtime losses to prioritize and display action plans for the plant floor:")
    
    # Calculate global baseline means for routing thresholds
    m_avail = df_filtered['Availability (A)'].mean()
    m_perf = df_filtered['Performance (P)'].mean()
    m_qual = df_filtered['Quality (Q)'].mean()
    
    # Establish dynamic data sorting to isolate root constraint bottlenecks
    levers = []
    if m_avail < 0.90:
        levers.append({
            "prio": 1 if m_avail < min(m_perf, m_qual) else 2,
            "metric": "Availability",
            "val": m_avail,
            "title": "Lever: Single-Minute Exchange of Die (SMED) & Asset Maintenance Automation",
            "type": "Danger",
            "color": "#DC3545",
            "body": "Unplanned breakdown hours and setup steps are impacting production capacity. Group tasks into Internal vs External steps. Stage raw inputs, tooling packages, and parameters while the asset is executing the prior line run. Audit your Autonomous Maintenance tracker to confirm frontline operators are completing daily cleanup and pre-failure inspection checks."
        })
    if m_perf < 0.95:
        levers.append({
            "prio": 1 if m_perf < min(m_avail, m_qual) else 2,
            "metric": "Performance",
            "val": m_perf,
            "title": "Lever: SOP Standardization, Cycle Locking, and Line Buffering",
            "type": "Warning",
            "color": "#FFC107",
            "body": "Equipment processing rates are dipping below target design capacities due to frequent micro-stops or intentional operator deceleration. Lock ideal cycle parameters within machine PLCs to prevent manual slowing. Install dynamic line accumulation tables or material conveyor loops to prevent upstream starvation or downstream blockages."
        })
    if m_qual < 0.98:
        levers.append({
            "prio": 1 if m_qual < min(m_avail, m_perf) else 2,
            "metric": "Quality",
            "val": m_qual,
            "title": "Lever: Poka-Yoke Mistake Proofing & Inline SPC Sensor Controls",
            "type": "Info",
            "color": "#17A2B8",
            "body": "Defects and rework runs are wasting valuable production time and material costs. Deploy structural Poka-Yoke (Mistake-Proofing) positioning pins or electronic orientation arrays to prevent misaligned processing. Set up Statistical Process Control (SPC) charting on critical machine telemetry parameters (clamping pressures, cylinder temperatures) to alert operators before drifts generate scrap."
        })
        
    # Sort levers by bottleneck severity
    levers = sorted(levers, key=lambda k: k['prio'])
    
    if not levers:
        st.success("🎉 **All Operational Metrics Balanced!** Running at world-class performance bounds across this shift.")
    else:
        for l in levers:
            st.markdown(f"""
            <div class='lever-card' style='border-top: 4px solid {l['color']};'>
                <span style='background-color:{l['color']}; color:white; padding:3px 8px; border-radius:3px; font-size:12px; font-weight:bold;'>PRIORITY {l['prio']}</span>
                <h4 style='margin-top:8px; color:#212529;'>{l['title']}</h4>
                <p style='color:#495057; font-size:14px;'><strong>Bottleneck Metric Profile:</strong> Global Mean average drops to <strong>{l['val']*100:.2f}%</strong>.</p>
                <p style='color:#333333; font-size:14px; line-height:1.6;'>{l['body']}</p>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------------------
# TAB 4: WHAT-IF OPTIMIZATION SIMULATOR
# ----------------------------------------------------------------
with tab_simulator:
    st.subheader("What-If Capacity Value Simulator")
    st.markdown("Adjust the sliders below to simulate the financial and capacity upside of optimizing your factory floor metrics.")
    
    # Sizing metrics aggregate constraints
    current_planned = df_filtered['Scheduled Production Time'].sum()
    current_unplanned = df_filtered['Unplanned Downtime'].sum()
    current_total_produced = df_filtered['Total Quantity Produced'].sum()
    current_scrap = df_filtered['Total Quantity Defective'].sum()
    
    c_col, r_col = st.columns([1, 1])
    
    with c_col:
        st.markdown("#### Step 1: Simulate Optimization Efficiencies")
        downtime_reduction = st.slider("Reduce Unplanned Breakdowns via SMED & PM (%):", min_value=0, max_value=100, value=20, step=5)
        scrap_reduction = st.slider("Minimize Scrap Counts via Poka-Yoke Controls (%):", min_value=0, max_value=100, value=30, step=5)
        financial_value_per_unit = st.number_input("Assumed Finished Part Value ($ / Piece):", min_value=0.0, max_value=500.0, value=12.50, step=0.50)
        
    with r_col:
        st.markdown("#### Step 2: Projected Returns Analysis")
        
        # Calculate simulation outputs
        simulated_unplanned = current_unplanned * (1 - (downtime_reduction / 100))
        simulated_scrap = current_scrap * (1 - (scrap_reduction / 100))
        
        # Recalculate global metrics under optimized state bounds
        sim_net_operating = (df_filtered['Net Available Time'].sum()) - simulated_unplanned
        sim_ideal_operating = df_filtered['Ideal Operating Time'].sum() # assume production potential limits
        sim_good_units = current_total_produced - simulated_scrap
        
        sim_avail = sim_net_operating / (df_filtered['Net Available Time'].sum())
        sim_perf = avg_perf # Hold performance static to maintain ceteris paribus modeling constraints
        sim_qual = sim_good_units / current_total_produced
        sim_oee = sim_avail * sim_perf * sim_qual
        
        # Financial impacts calculations
        extra_good_pieces = current_scrap - simulated_scrap
        revenue_recovery = extra_good_pieces * financial_value_per_unit
        hours_recovered = (current_unplanned - simulated_unplanned) / 60
        
        # Yield comparison table layout
        st.markdown(f"""
        * **Projected Optimized OEE:** <span style='color:#28A745; font-weight:bold; font-size:18px;'>{sim_oee*100:.2f}%</span> (Baseline: {avg_oee*100:.2f}%)
        * **Total Capacity Production Time Reclaimed:** <span style='color:#007BFF; font-weight:bold; font-size:16px;'>{hours_recovered:.1f} Hours</span>
        * **Scrap Units Retained as Finished Goods:** <span style='color:#007BFF; font-weight:bold; font-size:16px;'>{int(extra_good_pieces):,} Units</span>
        """, unsafe_allow_html=True)
        
        st.metric(
            label="Projected Gross Cost Recovery Opportunity", 
            value=f"${revenue_recovery:,.2f}", 
            delta=f"+ ${(extra_good_pieces * financial_value_per_unit):,.2f} Retained Value"
        )

# ----------------------------------------------------------------
# DATA EXPLORER & SYSTEM AUDIT GRID
# ----------------------------------------------------------------
st.markdown("---")
with st.expander("🔍 View Raw Underlying Multi-Column Ingestion Matrix"):
    st.dataframe(df_filtered, use_container_width=True)
