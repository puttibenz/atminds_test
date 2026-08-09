import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as bg

# Streamlit Page Configuration
st.set_page_config(
    page_title="Hotel Amber 85 — Buffet Analytics Dashboard",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling with High Contrast Colors (Compatible with Light & Dark Themes)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #2B5C8F;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        color: #0F172A !important;
    }
    .verdict-box-true {
        background-color: #ECFDF5 !important;
        border-left: 5px solid #10B981 !important;
        padding: 18px !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
        color: #064E3B !important;
    }
    .verdict-box-true h4 {
        color: #047857 !important;
        margin-top: 0 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .verdict-box-true p, .verdict-box-true b {
        color: #065F46 !important;
        font-size: 1rem !important;
    }
    .verdict-box-false {
        background-color: #FEF2F2 !important;
        border-left: 5px solid #EF4444 !important;
        padding: 18px !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
        color: #7F1D1D !important;
    }
    .verdict-box-false h4 {
        color: #B91C1C !important;
        margin-top: 0 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .verdict-box-false p, .verdict-box-false b {
        color: #991B1B !important;
        font-size: 1rem !important;
    }
    .verdict-box-partial {
        background-color: #FFFBEB !important;
        border-left: 5px solid #F59E0B !important;
        padding: 18px !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
        color: #78350F !important;
    }
    .verdict-box-partial h4 {
        color: #B45309 !important;
        margin-top: 0 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .verdict-box-partial p, .verdict-box-partial b {
        color: #92400E !important;
        font-size: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Datasets with Caching
@st.cache_data
def load_data():
    cleaned_path = 'pipeline/output/cleaned_stage1.csv'
    dq_path = 'pipeline/output/UNRESOLVED_MASTER_LIST.csv'
    overlap_path = 'pipeline/output/table_overlap_log.csv'
    
    if not os.path.exists(cleaned_path):
        cleaned_path = '../pipeline/output/cleaned_stage1.csv'
        dq_path = '../pipeline/output/UNRESOLVED_MASTER_LIST.csv'
        overlap_path = '../pipeline/output/table_overlap_log.csv'
        
    df = pd.read_csv(cleaned_path)
    df_dq = pd.read_csv(dq_path) if os.path.exists(dq_path) else pd.DataFrame()
    df_overlap = pd.read_csv(overlap_path) if os.path.exists(overlap_path) else pd.DataFrame()
    
    return df, df_dq, df_overlap

df, df_dq, df_overlap = load_data()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/fine-dining.png", width=70)
st.sidebar.title("Navigation Menu")
page = st.sidebar.radio(
    "Select Analysis Page:",
    [
        "📊 Executive Summary & Decision Matrix",
        "💬 Task 1: Staff Comments Audit",
        "🛑 Task 2: Management Actions Disproof",
        "💡 Task 3: Recommended Strategy",
        "📋 Data Quality & Explorer"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Project:** Hotel Amber 85 Breakfast Buffet Review  
**Data Scope:** 5 Service Days (363 Cleaned Groups)  
**Author:** Data Analytics Team 2026
""")

# ==========================================
# PAGE 1: EXECUTIVE SUMMARY & DECISION MATRIX
# ==========================================
if page == "📊 Executive Summary & Decision Matrix":
    st.markdown('<div class="main-header">Hotel Amber 85 — Breakfast Buffet Executive Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Data-Driven Strategic Analysis of TikTok Promotion Impact, Peak Congestion, & Capacity Optimization</div>', unsafe_allow_html=True)
    
    # Top KPI Metrics Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Total Serviced Groups", value=f"{len(df)} Groups", delta="5 Days Scope")
    with c2:
        valid_pax = df[df['pax'] > 0]['pax'].sum()
        st.metric(label="Cleaned Pax Volume", value=f"{int(valid_pax)} Guests", delta="102 - 166 Pax / Day")
    with c3:
        walkin_dwell = df[df['Guest_type'] == 'Walk in']['dwell_time_min'].mean()
        st.metric(label="Avg Walk-In Dwell Time", value=f"{walkin_dwell:.1f} Mins", delta="+27.0 min vs In-house", delta_color="inverse")
    with c4:
        st.metric(label="Peak Capacity Saved (90-Min Cap)", value="22.1 Table-Hours", delta="+29 Additional Slots")
        
    st.markdown("---")
    
    # Master Decision Matrix Table
    st.subheader("📌 Executive Master Decision Matrix")
    st.markdown("Summary of empirical data evidence, verdicts, and strategic recommendations across all tasks:")
    
    matrix_data = {
        "Task / Section": [
            "Task 1: Comment 1", "Task 1: Comment 2", "Task 1: Comment 3",
            "Task 2: Action 1", "Task 2: Action 2", "Task 2: Action 3",
            "Task 3: Strategy"
        ],
        "Subject / Proposal": [
            "In-house wait long / Walk-in abandon queue",
            "Equally busy every day of the week",
            "Walk-in sit all day & block tables",
            "Reduce 5-hour seating limit (Flat)",
            "Increase price to 259 THB daily",
            "Queue-skipping priority for In-house",
            "Tiered Peak-Window Soft Cap (90–100 min)"
        ],
        "Key Empirical Finding": [
            "Walk-in wait median is 44.5 m (vs In-house 28.0 m). In-house walk-away rate is 28.0% (vs Walk-in 14.6%).",
            "Daily group volume varies by 50.9% (57 to 86 groups). Peak concurrency varies from 16 to 23 tables.",
            "Walk-in avg dwell is 72.8 m (vs In-house 45.8 m). Walk-in holds 69.2% capacity & causes 19 blocker overlaps.",
            "Only 0.29% (1 group) stays > 4 hrs. 82.8% finish <= 90 mins. Targets non-existent tail problem.",
            "Peak concurrency reaches 16 tables even on lightest day (Day A). Congestion is peak turnover, not daily volume.",
            "Walk-in holds 69.2% of physical tables. Skipping queue does not add physical seats.",
            "Enforce 90-100 min soft cap ONLY during 08:00-10:00 AM peak; maintain 5-hr unlimited benefit off-peak."
        ],
        "Verdict & Operational Impact": [
            "⚠️ PARTIALLY TRUE (Prioritize In-house retention)",
            "❌ FALSE (Dynamic staffing & allocation required)",
            "✅ TRUE (Walk-in dwell is primary bottleneck)",
            "🛑 WILL NOT WORK (Flat limit lacks focus)",
            "🛑 WILL NOT WORK (Punishes off-peak guests)",
            "🛑 WILL NOT WORK (Pushes Walk-in to crisis)",
            "💡 RECOMMENDED STRATEGY (Saves 22.1 Table-Hours)"
        ]
    }
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Overview Visualizations
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Daily Customer Volume by Guest Type")
        daily_gt = df.groupby(['day_id', 'Guest_type']).size().reset_index(name='group_count')
        fig_vol = px.bar(
            daily_gt, x='day_id', y='group_count', color='Guest_type',
            barmode='group', text_auto=True,
            labels={'day_id': 'Service Day', 'group_count': 'Number of Customer Groups', 'Guest_type': 'Guest Type'},
            color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
        )
        fig_vol.update_layout(height=380, legend=dict(orientation="h", y=1.1, x=0.2))
        st.plotly_chart(fig_vol, use_container_width=True)
        
    with col_right:
        st.subheader("Table Capacity Consumption Share (Table-Hours)")
        table_share = df.groupby('Guest_type')['table_minutes'].sum().reset_index()
        table_share['table_hours'] = table_share['table_minutes'] / 60.0
        fig_pie = px.pie(
            table_share, values='table_hours', names='Guest_type',
            hole=0.4, color='Guest_type',
            color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
        )
        fig_pie.update_traces(textinfo='percent+label', textfont_size=13)
        fig_pie.update_layout(height=380, legend=dict(orientation="h", y=1.1, x=0.2))
        st.plotly_chart(fig_pie, use_container_width=True)


# ==========================================
# PAGE 2: TASK 1 - STAFF COMMENTS AUDIT
# ==========================================
elif page == "💬 Task 1: Staff Comments Audit":
    st.markdown('<div class="main-header">Task 1: Front-Line Staff Comments Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Empirical Validation of Wait Times, Queue Abandonment, Operational Workload, and Dwell Bottlenecks</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "💬 Comment 1: Wait Time & Queue Abandonment",
        "💬 Comment 2: Daily Operational Workload",
        "💬 Comment 3: Walk-In Dwell & Table Bottlenecks"
    ])
    
    # ------------------ TAB 1 ------------------
    with tab1:
        st.markdown("""
        > **Staff Statement:** *"In-house (hotel) customers are unhappy that they have to wait for a table. Walk-in customers are also unhappy, when they queue up for a long time and leave the queue because they don't want to wait any longer."*
        """)
        
        df_q = df[df['queue_start_min'].notnull() & df['queue_end_min'].notnull()].copy()
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Walk-In Wait (Median)", "44.5 Mins", "Mean 38.4 Mins")
        with col_m2:
            st.metric("In-House Wait (Median)", "28.0 Mins", "Mean 28.0 Mins")
        with col_m3:
            st.metric("In-House Walk-Away Rate", "28.0%", "7 / 25 Queuing Groups", delta_color="inverse")
        with col_m4:
            st.metric("Walk-In Walk-Away Rate", "14.6%", "7 / 48 Queuing Groups")
            
        c_left, c_right = st.columns(2)
        with c_left:
            fig_wait = px.box(
                df_q[df_q['wait_time_min'].notnull()],
                x='Guest_type', y='wait_time_min', color='Guest_type',
                labels={'wait_time_min': 'Wait Time in Queue (Minutes)', 'Guest_type': 'Guest Type'},
                color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
            )
            fig_wait.update_layout(title="Queue Wait Time Distribution (Minutes)", height=380, showlegend=False)
            st.plotly_chart(fig_wait, use_container_width=True)
            
        with c_right:
            wa_df = df_q.groupby('Guest_type').agg(
                total=('service_no.', 'count'),
                walk_away=('is_walk_away', 'sum')
            ).reset_index()
            wa_df['pct'] = (wa_df['walk_away'] / wa_df['total']) * 100
            
            fig_wa = px.bar(
                wa_df, x='Guest_type', y='pct', color='Guest_type',
                text_auto='.1f',
                labels={'pct': 'Queue Abandonment Rate (%)', 'Guest_type': 'Guest Type'},
                color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
            )
            fig_wa.update_layout(title="Queue Abandonment Rate (% Walk-Away)", height=380, showlegend=False)
            st.plotly_chart(fig_wa, use_container_width=True)
            
        st.info("💡 **Operational Caveat (Queue Data Limitation):** Queue timestamps (queue_start / queue_end) were logged exclusively during Day B and Day C (73 total queuing groups), while Days A, D, and E lacked queue tracking. While this 73-group sample is statistically sufficient for Task 1 audit, mandatory daily queue logging across all service days is strongly recommended for future operational tracking.")
        
        st.markdown("""
        <div class="verdict-box-partial">
            <h4>⚠️ Audit Verdict: PARTIALLY TRUE</h4>
            <p>Walk-in guests experience longer queue wait times (Median <b>44.5 mins</b> vs In-house <b>28.0 mins</b>). However, front-line staff mistakenly assumed Walk-in guests abandon queues most often. In reality, <b>In-house hotel guests abandon queues at nearly double the rate (28.0% vs 14.6%)</b> due to significantly lower wait tolerance.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # ------------------ TAB 2 ------------------
    with tab2:
        st.markdown("""
        > **Staff Statement:** *"We are very busy every day of the week. If it's going to be this busy every week I think it's impossible to sustain this business."*
        """)
        
        daily_vol = df.groupby('day_id').agg(
            total_groups=('service_no.', 'count'),
            total_pax=('pax', lambda x: x[x > 0].sum())
        ).reset_index()
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Min Daily Volume (Day A)", "57 Groups", "102 Pax")
        with m2:
            st.metric("Max Daily Volume (Day C)", "86 Groups", "166 Pax")
        with m3:
            st.metric("Volume Difference", "+50.9%", "Day A vs Day C")
        with m4:
            st.metric("Peak Concurrency Range", "16 - 23 Tables", "Day A vs Day B/C")
            
        c_left2, c_right2 = st.columns(2)
        with c_left2:
            fig_dvol = px.bar(
                daily_vol, x='day_id', y='total_groups', text_auto=True,
                labels={'day_id': 'Service Day', 'total_groups': 'Total Serviced Groups'},
                color_discrete_sequence=['#2B5C8F']
            )
            fig_dvol.update_layout(title="Total Serviced Groups per Service Day", height=380)
            st.plotly_chart(fig_dvol, use_container_width=True)
            
        with c_right2:
            time_slots = list(range(360, 766, 15))
            conc_list = []
            for day in sorted(df['day_id'].unique()):
                df_day = df[(df['day_id'] == day) & df['meal_start_min'].notnull() & df['meal_end_min'].notnull()]
                for t in time_slots:
                    active = df_day[(df_day['meal_start_min'] <= t) & (df_day['meal_end_min'] > t)]
                    conc_list.append({
                        'day_id': day,
                        'time_str': f"{t//60:02d}:{t%60:02d}",
                        'active_tables': len(active)
                    })
            df_conc = pd.DataFrame(conc_list)
            
            fig_conc = px.line(
                df_conc, x='time_str', y='active_tables', color='day_id', markers=True,
                labels={'time_str': 'Time of Day', 'active_tables': 'Active Seated Tables', 'day_id': 'Day'}
            )
            fig_conc.update_layout(title="15-Minute Seated Table Concurrency (06:00 - 12:45)", height=380)
            st.plotly_chart(fig_conc, use_container_width=True)
            
        st.markdown("""
        <div class="verdict-box-false">
            <h4>❌ Audit Verdict: FALSE</h4>
            <p>Operational workload is <b>not equal every day of the week</b>. Daily volume varies by <b>50.9%</b> (57 to 86 groups). Day B & C reach peak stress levels of <b>22–23 active tables</b>, Day D reaches moderate peak concurrency of <b>18 tables</b>, and Day A peaks at <b>16 tables</b>. Management can implement dynamic staffing and table allocation based on day-of-week demand patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # ------------------ TAB 3 ------------------
    with tab3:
        st.markdown("""
        > **Staff Statement:** *"Walk-in customers sit the whole day. It's very difficult to find seats for in-house customers. We don't have enough tables so when one customer sits for a long time it makes the queue very long."*
        """)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Walk-In Avg Dwell", "72.8 Mins", "Median 66.0 Mins")
        with m2:
            st.metric("In-House Avg Dwell", "45.8 Mins", "Median 39.0 Mins")
        with m3:
            st.metric("Walk-In Table Share", "69.2%", "322.7 Table-Hours", delta_color="inverse")
        with m4:
            st.metric("Walk-In Overlap Blockers", "19 Events", "102.3 min avg blocker dwell")
            
        c_left3, c_right3 = st.columns(2)
        with c_left3:
            fig_dwell = px.box(
                df[df['dwell_time_min'].notnull()],
                x='Guest_type', y='dwell_time_min', color='Guest_type',
                labels={'dwell_time_min': 'Dwell Duration (Minutes)', 'Guest_type': 'Guest Type'},
                color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
            )
            fig_dwell.update_layout(title="Customer Dwell Duration Distribution (Minutes)", height=380, showlegend=False)
            st.plotly_chart(fig_dwell, use_container_width=True)
            
        with c_right3:
            if not df_overlap.empty:
                blocker_df = df_overlap.groupby('curr_group_guest_type').size().reset_index(name='blocking_events')
                fig_block = px.bar(
                    blocker_df, x='curr_group_guest_type', y='blocking_events', color='curr_group_guest_type',
                    text_auto=True,
                    labels={'curr_group_guest_type': 'Blocking Guest Type', 'blocking_events': 'Number of Blocker Events'},
                    color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
                )
                fig_block.update_layout(title="Double-Booking Table Blocker Overlap Events", height=380, showlegend=False)
                st.plotly_chart(fig_block, use_container_width=True)
                
        st.markdown("""
        <div class="verdict-box-true">
            <h4>✅ Audit Verdict: TRUE (Strongly Supported)</h4>
            <p>Walk-in guests sit substantially longer than hotel guests (Mean <b>72.8 mins</b> vs <b>45.8 mins</b>), monopolize <b>69.2% of total table capacity</b>, and represent the blocking group in 19 out of 31 table-overlap events (avg dwell 102.3 mins). Walk-in dwell duration is the primary operational bottleneck.</p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE 3: TASK 2 - MANAGEMENT ACTIONS DISPROOF
# ==========================================
elif page == "🛑 Task 2: Management Actions Disproof":
    st.markdown('<div class="main-header">Task 2: Empirical Disproof of Management Actions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Rigorous Evaluation of Proposed Candidate Actions Prior to Operational Implementation</div>', unsafe_allow_html=True)
    
    t1, t2, t3 = st.tabs([
        "🛑 Action 1: Reduce Seating Time Limit (Flat)",
        "🛑 Action 2: Increase Price Everyday to 259 THB",
        "🛑 Action 3: Queue-Skipping Priority for In-House"
    ])
    
    # ------------------ ACTION 1 ------------------
    with t1:
        st.markdown("""
        > **Proposed Candidate Action:** *"Reduce seating time limit from 5 hours to a shorter duration across the board."*
        """)
        
        df_dwell = df[df['dwell_time_min'].notnull()].copy()
        total_g = len(df_dwell)
        gt_240 = (df_dwell['dwell_time_min'] > 240).sum()
        le_90 = (df_dwell['dwell_time_min'] <= 90).sum()
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Evaluated Groups", f"{total_g} Groups")
        with m2:
            st.metric("Groups Sitting > 4 Hours", f"{gt_240} Group (0.29%)", delta="Non-existent tail", delta_color="normal")
        with m3:
            st.metric("Groups Finishing <= 90 Mins", f"{le_90} Groups (82.8%)", delta="Natural dining pace")
            
        fig_act1 = px.histogram(
            df_dwell, x='dwell_time_min', color='Guest_type', barmode='overlay',
            nbins=30, opacity=0.7,
            labels={'dwell_time_min': 'Dwell Time (Minutes)', 'Guest_type': 'Guest Type'},
            color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
        )
        fig_act1.add_vline(x=90, line_dash="dash", line_color="orange", annotation_text="Proposed 90-Min Soft Cap (82.8% <= 90m)")
        fig_act1.add_vline(x=300, line_dash="dash", line_color="red", annotation_text="Original 5-Hour Limit (0.29% > 4h)")
        fig_act1.update_layout(title="Dwell Duration Histogram with 90-Min and 300-Min Cutoff Thresholds", height=400)
        st.plotly_chart(fig_act1, use_container_width=True)
        
        st.markdown("""
        <div class="verdict-box-false">
            <h4>🛑 Verdict: WILL NOT WORK</h4>
            <p>Imposing a flat daily limit reduction (e.g. capping seating at 3 hours) targets a non-existent tail problem (only 0.29% stay past 4 hours). It fails to accelerate table turnover during the critical 08:00–10:00 AM peak window where Walk-in dwell averages 73 minutes.</p>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ ACTION 2 ------------------
    with t2:
        st.markdown("""
        > **Proposed Candidate Action:** *"Increase buffet price to 259 THB every day of the week."*
        """)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Lightest Day Volume (Day A)", "57 Groups", "102 Pax")
        with m2:
            st.metric("Day A Peak Concurrency", "16 Active Tables", "08:30 - 09:30 AM Peak")
        with m3:
            st.metric("Day C Peak Concurrency", "23 Active Tables", "86 Groups Volume")
            
        daily_vol = df.groupby('day_id').agg(total_groups=('service_no.', 'count')).reset_index()
        time_slots = list(range(360, 766, 15))
        conc_list = []
        for day in sorted(df['day_id'].unique()):
            df_day = df[(df['day_id'] == day) & df['meal_start_min'].notnull() & df['meal_end_min'].notnull()]
            for t in time_slots:
                active = df_day[(df_day['meal_start_min'] <= t) & (df_day['meal_end_min'] > t)]
                conc_list.append({'day_id': day, 'active_tables': len(active)})
        df_conc2 = pd.DataFrame(conc_list)
        peak_c = df_conc2.groupby('day_id')['active_tables'].max().reset_index(name='peak_concurrency')
        combo_df = pd.merge(daily_vol, peak_c, on='day_id')
        
        fig_combo = bg.Figure()
        fig_combo.add_trace(bg.Bar(x=combo_df['day_id'], y=combo_df['total_groups'], name='Total Daily Groups', marker_color='#2B5C8F', opacity=0.7))
        fig_combo.add_trace(bg.Scatter(x=combo_df['day_id'], y=combo_df['peak_concurrency'], name='Peak Concurrency (Tables)', yaxis='y2', mode='lines+markers', line=dict(color='#D95F02', width=3)))
        fig_combo.update_layout(
            title="Daily Total Serviced Groups vs Peak Hour Seated Concurrency",
            yaxis=dict(title="Total Serviced Groups"),
            yaxis2=dict(title="Peak Seated Concurrency (Active Tables)", overlaying='y', side='right'),
            height=400,
            legend=dict(orientation="h", y=1.1, x=0.2)
        )
        st.plotly_chart(fig_combo, use_container_width=True)
        
        st.markdown("""
        <div class="verdict-box-false">
            <h4>🛑 Verdict: WILL NOT WORK</h4>
            <p>Congestion is driven by <b>table turnover rate during peak morning hours</b>, not by total daily customer volume. Even on Day A (the lightest day with 57 groups), peak concurrency reached <b>16 active tables</b> during 08:30–09:30 AM. A flat price hike penalizes off-peak customers and damages viral TikTok marketing momentum.</p>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ ACTION 3 ------------------
    with t3:
        st.markdown("""
        > **Proposed Candidate Action:** *"Give In-house hotel guests queue-skipping priority over Walk-in guests."*
        """)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Walk-In Table Share", "69.2%", "Holds 322.7 Table-Hours")
        with m2:
            st.metric("In-House Queue Abandonment", "28.0%", "7 / 25 Queuing Groups")
        with m3:
            st.metric("Walk-In Overlap Blockers", "19 Events", "Avg dwell 102.3 mins")
            
        act3_data = pd.DataFrame({
            'Metric Category': ['Table Capacity Monopolization (%)', 'Queue Abandonment Rate (%)', 'Table Blocker Overlaps (Count)'],
            'In House': [30.8, 28.0, 12],
            'Walk in': [69.2, 14.6, 19]
        })
        fig_act3 = px.bar(
            act3_data, x='Metric Category', y=['In House', 'Walk in'], barmode='group',
            labels={'value': 'Metric Value', 'variable': 'Guest Type'},
            color_discrete_map={'In House': '#2B5C8F', 'Walk in': '#D95F02'}
        )
        fig_act3.update_layout(title="Action 3 Disproof: In-House Priority vs Walk-In Physical Monopolization", height=400)
        st.plotly_chart(fig_act3, use_container_width=True)
        
        st.markdown("""
        <div class="verdict-box-false">
            <h4>🛑 Verdict: WILL NOT WORK</h4>
            <p>Walk-in guests occupy <b>69.2% of physical tables</b>. Skipping the queue reorders waiting customers but creates zero physical seating capacity. Pushing Walk-in wait times past 45 minutes will trigger severe queue abandonment and negative online reviews.</p>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# PAGE 4: TASK 3 - RECOMMENDED STRATEGY
# ==========================================
elif page == "💡 Task 3: Recommended Strategy":
    st.markdown('<div class="main-header">Task 3: Supported Recommended Strategy — Tiered Soft Cap</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Balancing TikTok Promotional Marketing with Peak Morning Operational Efficiency</div>', unsafe_allow_html=True)
    
    st.subheader("💡 Strategic Policy Framework")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div style="background-color:#F0FDF4; padding:20px; border-radius:8px; border-left:5px solid #10B981; color:#064E3B !important;">
            <h4 style="color:#047857 !important; margin-top:0; font-size:1.15rem; font-weight:700;">🟢 Off-Peak Window (06:00–08:00 AM & 10:00 AM–01:00 PM)</h4>
            <p style="color:#065F46 !important; font-size:1rem; margin-bottom:0.5rem;"><b style="color:#047857 !important;">Policy:</b> Full 5-Hour Unlimited Seating Benefit</p>
            <p style="color:#065F46 !important; font-size:0.95rem;"><b style="color:#047857 !important;">Rationale:</b> Preserves the core promotional promise of the TikTok marketing campaign ("All You Can Eat / 5 Hours") when table vacancy is high.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_p2:
        st.markdown("""
        <div style="background-color:#EFF6FF; padding:20px; border-radius:8px; border-left:5px solid #3B82F6; color:#1E3A8A !important;">
            <h4 style="color:#1D4ED8 !important; margin-top:0; font-size:1.15rem; font-weight:700;">🔵 Peak Window (08:00–10:00 AM)</h4>
            <p style="color:#1E40AF !important; font-size:1rem; margin-bottom:0.5rem;"><b style="color:#1D4ED8 !important;">Policy:</b> Soft Cap of 90–100 Minutes on Seating</p>
            <p style="color:#1E40AF !important; font-size:0.95rem;"><b style="color:#1D4ED8 !important;">Rationale:</b> Directly targets peak congestion where Walk-in dwell averages 73–102 minutes, accelerating table turnover.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("📊 Quantitative Capacity Simulation (08:00 - 10:00 AM Peak)")
    
    df_peak = df[(df['meal_start_min'] >= 480) & (df['meal_start_min'] <= 600) & df['dwell_time_min'].notnull()].copy()
    df_peak['capped_dwell_90'] = df_peak['dwell_time_min'].apply(lambda x: min(x, 90.0))
    df_peak['table_mins_orig'] = df_peak['dwell_time_min'] * df_peak['n_units']
    df_peak['table_mins_capped'] = df_peak['capped_dwell_90'] * df_peak['n_units']
    
    orig_m = df_peak['table_mins_orig'].sum()
    capped_m = df_peak['table_mins_capped'].sum()
    saved_m = orig_m - capped_m
    saved_h = saved_m / 60.0
    slots = saved_m / 45.0
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Peak Seated Groups", f"{len(df_peak)} Groups")
    with m2:
        st.metric("Original Capacity Used", f"{orig_m/60.0:.1f} Table-Hours")
    with m3:
        st.metric("Capacity Saved (90-Min Cap)", f"{saved_h:.1f} Table-Hours", f"{saved_m:.0f} Table-Mins", delta_color="normal")
    with m4:
        st.metric("Additional Seating Slots Created", f"~{slots:.0f} Slots", "Assuming 45-min turnover")
        
    fig_sim = px.histogram(
        df_peak, x='dwell_time_min', color='Guest_type', barmode='overlay',
        nbins=20, opacity=0.7,
        labels={'dwell_time_min': 'Peak Dwell Time (Minutes)', 'Guest_type': 'Guest Type'},
        color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'}
    )
    fig_sim.add_vline(x=90, line_dash="dash", line_color="red", annotation_text="Proposed 90-Min Soft Cap")
    fig_sim.update_layout(title="Peak Window Dwell Time Distribution & Proposed 90-Min Soft Cap (08:00 - 10:00 AM)", height=380)
    st.plotly_chart(fig_sim, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("🛠️ Operational Implementation Guidelines")
    st.markdown("""
    1. **Mandatory Queue Data Logging:** Require front-desk staff to log `queue_start` and `queue_end` timestamps daily to track queue improvements continuously.
    2. **In-House Buffer Table Reservation:** Reserve 4 to 6 Indoor split tables (Tables 1A–3B) exclusively for In-house hotel guests between 07:30 and 09:30 AM to eliminate the **28.0% In-house walk-away rate**.
    3. **Hospitable Staff Soft-Cap Protocol:** Train service staff for polite minute-75 check-ins (*"May I offer you a coffee refill or dessert?"*) during peak hours, signaling table wrap-up hospitably.
    """)


# ==========================================
# PAGE 5: DATA QUALITY & EXPLORER
# ==========================================
elif page == "📋 Data Quality & Explorer":
    st.markdown('<div class="main-header">Data Quality Audit & Cleaned Dataset Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Full Data Hygiene Record, Master DQ Audit Log, and Table Double-Booking Log</div>', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Cleaned Dataset Rows", f"{len(df)} Rows", "1 Empty Row Dropped")
    with m2:
        st.metric("Master Unresolved DQ Log", f"{len(df_dq)} Issues", "Stages 0 - 4 Hygiene")
    with m3:
        st.metric("Table Double-Booking Overlaps", f"{len(df_overlap)} Events", "Mapped by Seating Units")
        
    st.markdown("---")
    
    tab_d1, tab_d2, tab_d3 = st.tabs([
        "📄 Cleaned Dataset Explorer",
        "⚠️ Master Unresolved Data Quality Log",
        "🪑 Table Double-Booking Overlap Log"
    ])
    
    with tab_d1:
        st.subheader("Cleaned Dataset (`cleaned_stage1.csv`)")
        day_filter = st.multiselect("Filter by Service Day:", options=sorted(df['day_id'].unique()), default=sorted(df['day_id'].unique()))
        guest_filter = st.multiselect("Filter by Guest Type:", options=sorted(df['Guest_type'].unique()), default=sorted(df['Guest_type'].unique()))
        
        filtered_df = df[(df['day_id'].isin(day_filter)) & (df['Guest_type'].isin(guest_filter))]
        st.dataframe(filtered_df, use_container_width=True)
        st.caption(f"Displaying {len(filtered_df)} out of {len(df)} cleaned rows.")
        
    with tab_d2:
        st.subheader("Master Unresolved Data Quality Issues (`UNRESOLVED_MASTER_LIST.csv`)")
        if not df_dq.empty:
            st.dataframe(df_dq, use_container_width=True)
        else:
            st.info("No unresolved data quality issues found.")
            
    with tab_d3:
        st.subheader("Table Double-Booking Overlap Log (`table_overlap_log.csv`)")
        if not df_overlap.empty:
            st.dataframe(df_overlap, use_container_width=True)
        else:
            st.info("No table overlap events found.")
