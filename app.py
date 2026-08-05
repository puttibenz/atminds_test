import os
import re
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Hotel Amber 85 — Buffet Analytics",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
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
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 1rem;
        border-left: 5px solid #2B5C8F;
    }
    .verdict-true {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        border-left: 5px solid #10B981;
    }
    .verdict-false {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        border-left: 5px solid #EF4444;
    }
    .verdict-partial {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.8rem;
        border-radius: 8px;
        font-weight: 600;
        border-left: 5px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

# Data Loader Helper
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    cleaned_path = os.path.join(base_dir, 'pipeline', 'output', 'cleaned_stage1.csv')
    unresolved_path = os.path.join(base_dir, 'pipeline', 'output', 'UNRESOLVED_MASTER_LIST.csv')
    overlap_path = os.path.join(base_dir, 'pipeline', 'output', 'table_overlap_log.csv')
    
    # Fallback to local pipeline folder if needed
    if not os.path.exists(cleaned_path):
        cleaned_path = 'pipeline/output/cleaned_stage1.csv'
        unresolved_path = 'pipeline/output/UNRESOLVED_MASTER_LIST.csv'
        overlap_path = 'pipeline/output/table_overlap_log.csv'
        
    df_cleaned = pd.read_csv(cleaned_path)
    df_unresolved = pd.read_csv(unresolved_path) if os.path.exists(unresolved_path) else pd.DataFrame()
    df_overlap = pd.read_csv(overlap_path) if os.path.exists(overlap_path) else pd.DataFrame()
    
    return df_cleaned, df_unresolved, df_overlap

df, df_unresolved, df_overlap = load_data()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/breakfast.png", width=70)
st.sidebar.title("Buffet Analytics")
st.sidebar.caption("Hotel Amber 85 · Breakfast Review")

page = st.sidebar.radio(
    "เลือกหน้าการทำงาน (Navigation)",
    [
        "📊 Executive Summary & KPIs",
        "💬 Task 1: Staff Comments Audit",
        "🛑 Task 2: Management Actions Disproof",
        "💡 Task 3: Supported Strategy",
        "📋 Data Quality & Explorer"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **ข้อมูลการประมวลผล:**\n- ข้อมูลบริการ 5 วัน (Day A-E)\n- Cleaned Records: 363 กลุ่ม\n- Logged DQ Issues: 58+ รายการ")

# ==========================================
# PAGE 1: EXECUTIVE SUMMARY & KPIS
# ==========================================
if page == "📊 Executive Summary & KPIs":
    st.markdown('<div class="main-header">📊 Executive Summary & KPIs ภาพรวม</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">สรุปผลการวิเคราะห์ข้อมูลบริการบุฟเฟ่ต์อาหารเช้า โรงแรม Hotel Amber 85</div>', unsafe_allow_html=True)
    
    # Top KPI Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("จำนวนกลุ่มลูกค้ารวม", f"{len(df)} กลุ่ม", "5 วันบริการ")
    with col2:
        valid_pax = df[df['pax'] > 0]['pax'].sum()
        st.metric("จำนวนลูกค้ารวม (Pax)", f"{int(valid_pax)} คน", "7 Pax=0 flagged")
    with col3:
        avg_wait = df[df['wait_time_min'].notnull()]['wait_time_min'].mean()
        st.metric("เวลารอคิวเฉลี่ย", f"{avg_wait:.1f} นาที", "เฉพาะกลุ่มเข้าคิว")
    with col4:
        avg_dwell = df[df['dwell_time_min'].notnull()]['dwell_time_min'].mean()
        st.metric("เวลานั่งทานเฉลี่ย", f"{avg_dwell:.1f} นาที", "มัธยฐาน 52.0 นาที")
    with col5:
        st.metric("เหตุการณ์โต๊ะนั่งซ้อน", f"{len(df_overlap)} ครั้ง", "Double-bookings")
        
    st.markdown("---")
    
    # Master Decision Table
    st.subheader("📌 ตารางสรุปข้อสรุปเชิงยุทธศาสตร์ (Master Decision Matrix)")
    
    matrix_data = [
        {"Task": "Task 1 (Comment 1)", "หัวข้อ": "In-house รอคิวนาน / Walk-in ทิ้งคิว", "ข้อเท็จจริง": "Walk-in รอ 44.5 นาที (นานกว่า In-house 28 นาที) แต่ In-house ทิ้งคิวสูงถึง 28.0% (vs Walk-in 14.6%)", "ผลสรุป": "⚠️ จริงบางส่วน (Partially True)"},
        {"Task": "Task 1 (Comment 2)", "หัวข้อ": "ยุ่งเท่ากันทุกวันในสัปดาห์", "ข้อเท็จจริง": "ปริมาณต่างกัน 50.9% (57 ถึง 86 กลุ่ม) และ Peak Concurrency ต่างกัน (16 vs 23 โต๊ะ)", "ผลสรุป": "❌ ไม่จริง (False)"},
        {"Task": "Task 1 (Comment 3)", "หัวข้อ": "Walk-in นั่งแช่ทั้งวัน ทำให็หาโต๊ะไม่ได้", "ข้อเท็จจริง": "Walk-in นั่งเฉลี่ย 72.8 นาที ครองความจุโต๊ะ 69.2% และเป็นตัวขวางโต๊ะหลัก 19 ครั้ง", "ผลสรุป": "✅ จริงอย่างยิ่ง (True)"},
        {"Task": "Task 2 (Action 1)", "หัวข้อ": "ลดเวลานั่งจาก 5 ชม. เป็นน้อยลง", "ข้อเท็จจริง": "82.8% นั่ง finished <= 90 นาที; มีแค่ 0.29% (1 กลุ่ม) นั่ง > 4 ชม. แก้ผิดจุดที่ปลายหาง", "ผลสรุป": "🛑 ไม่ได้ผล (Will NOT Work)"},
        {"Task": "Task 2 (Action 2)", "หัวข้อ": "ขึ้นราคาเป็น 259 บาททุกวัน", "ข้อเท็จจริง": "แม้วันคนน้อยสุด (Day A) ช่วง Peak ก็แน่นถึง 16 โต๊ะ ปัญหาอยู่ที่ turnover rate ช่วงพีค", "ผลสรุป": "🛑 ไม่ได้ผล (Will NOT Work)"},
        {"Task": "Task 2 (Action 3)", "หัวข้อ": "ให้ In-house แซงคิว", "ข้อเท็จจริง": "สลับคิวแต่ไม่ได้เพิ่มโต๊ะจริง Walk-in ครองโต๊ะ 69.2% ทำให้ Walk-in รอนานวิกฤต", "ผลสรุป": "🛑 ไม่ได้ผล (Will NOT Work)"},
        {"Task": "Task 3 (Supported)", "หัวข้อ": "Tiered Soft Cap (90-100 นาที)", "ข้อเท็จจริง": "คุมเวลานั่งเฉพาะช่วง Peak (08:00-10:00 น.) ประหยัดความจุได้ 22.1 Table-Hours เพิ่มรอบได้ ~29 กลุ่ม", "ผลสรุป": "💡 มาตรการที่แนะนำ (Recommended)"}
    ]
    st.table(pd.DataFrame(matrix_data))
    
    # Quick Visual Overview
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📈 จำนวนกลุ่มลูกค้ารายวัน (Daily Groups)")
        daily_cnt = df.groupby(['day_id', 'Guest_type']).size().reset_index(name='count')
        fig_daily = px.bar(daily_cnt, x='day_id', y='count', color='Guest_type', barmode='group',
                           color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                           title="จำนวนกลุ่มลูกค้าแยกตามประเภทรายวัน")
        st.plotly_chart(fig_daily, use_container_width=True)
        
    with c2:
        st.subheader("🥧 สัดส่วนประเภทลูกค้าทั้งหมด (Guest Type Share)")
        guest_cnt = df['Guest_type'].value_counts().reset_index()
        guest_cnt.columns = ['Guest_type', 'count']
        fig_pie = px.pie(guest_cnt, names='Guest_type', values='count', hole=0.4,
                         color='Guest_type', color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                         title="สัดส่วนจำนวนกลุ่ม In-house vs Walk-in")
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# PAGE 2: TASK 1 - STAFF COMMENTS AUDIT
# ==========================================
elif page == "💬 Task 1: Staff Comments Audit":
    st.markdown('<div class="main-header">💬 Task 1: พิสูจน์ / หักล้าง คำพูดพนักงาน</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">ตรวจสอบข้อร้องเรียน 3 ข้อของพนักงานด้วยข้อมูลเชิงปริมาณ</div>', unsafe_allow_html=True)
    
    t1_tab1, t1_tab2, t1_tab3 = st.tabs([
        "Comment 1: Wait Time & Walk-Away",
        "Comment 2: Daily Concurrency",
        "Comment 3: Dwell Time & Overlaps"
    ])
    
    # --- Comment 1 Tab ---
    with t1_tab1:
        st.markdown("### Comment 1: *'In-house รอโต๊ะนาน / Walk-in ทิ้งคิวเพราะรอไม่ไหว'*)")
        
        df_queue = df[df['queue_start_min'].notnull() & df['queue_end_min'].notnull()].copy()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Wait Time มัธยฐาน (Walk-in)", "44.5 นาที", "รอนานกว่า")
        m2.metric("Wait Time มัธยฐาน (In-house)", "28.0 นาที", "รอเร็วกว่า")
        m3.metric("Walk-away Rate (In-house)", "28.0%", "7/25 กลุ่ม (ทิ้งคิวสูง!)")
        m4.metric("Walk-away Rate (Walk-in)", "14.6%", "7/48 กลุ่ม (ทิ้งคิวน้อยกว่า)")
        
        c1, c2 = st.columns(2)
        with c1:
            fig_wait = px.box(df_queue[df_queue['wait_time_min'].notnull()], x='Guest_type', y='wait_time_min',
                              color='Guest_type', color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                              title="กระจายตัวเวลารอคิว (Wait Time in Minutes)")
            st.plotly_chart(fig_wait, use_container_width=True)
            
        with c2:
            walk_summary = df_queue.groupby('Guest_type').agg(
                total=('service_no.', 'count'),
                walk_away=('is_walk_away', 'sum')
            ).reset_index()
            walk_summary['rate_pct'] = (walk_summary['walk_away'] / walk_summary['total']) * 100
            
            fig_walk = px.bar(walk_summary, x='Guest_type', y='rate_pct', text_auto='.1f',
                              color='Guest_type', color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                              title="อัตราการทิ้งคิว Walk-Away Rate (%)")
            st.plotly_chart(fig_walk, use_container_width=True)
            
        st.markdown('<div class="verdict-partial">⚠️ ข้อสรุป Comment 1: จริงบางส่วน (Partially True)<br>- Walk-in รอนานกว่าจริง (44.5 นาที vs 28.0 นาที)<br>- แต่คำพูดที่ว่า Walk-in ทิ้งคิวเพราะรอไม่ไหว <b>"ไม่จริง"</b> ในเชิงสัดส่วน เพราะ In-house ทิ้งคิวสูงถึง 28.0% (ทิ้งคิวบ่อยกว่าเกือบเท่าตัว)</div>', unsafe_allow_html=True)

    # --- Comment 2 Tab ---
    with t1_tab2:
        st.markdown("### Comment 2: *'ยุ่งทุกวันในสัปดาห์เท่ากันจนธุรกิจนี้ทำต่อไม่ได้'*)")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("วันที่มีลูกค้าน้อยสุด (Day A)", "57 กลุ่ม (102 Pax)", "Peak 16 โต๊ะ")
        c2.metric("วันที่แน่นที่สุด (Day C)", "86 กลุ่ม (166 Pax)", "Peak 23 โต๊ะ")
        c3.metric("ความแตกต่างปริมาณลูกค้า", "+50.9%", "ต่างกันชัดเจน")
        
        # Concurrency 15-min
        time_slots = list(range(360, 766, 15))
        concurrency_records = []
        for day in sorted(df['day_id'].unique()):
            df_day = df[(df['day_id'] == day) & df['meal_start_min'].notnull() & df['meal_end_min'].notnull()]
            for t in time_slots:
                active = df_day[(df_day['meal_start_min'] <= t) & (df_day['meal_end_min'] > t)]
                concurrency_records.append({
                    'day_id': day,
                    'time_min': t,
                    'time_str': f"{t//60:02d}:{t%60:02d}",
                    'active_groups': len(active)
                })
        df_conc = pd.DataFrame(concurrency_records)
        
        fig_conc = px.line(df_conc, x='time_str', y='active_groups', color='day_id',
                           title="เส้นโค้ง Concurrency โต๊ะที่มีลูกค้านั่งพร้อมกันราย 15 นาที (06:00 - 12:45 น.)",
                           labels={'time_str': 'เวลา', 'active_groups': 'จำนวนโต๊ะที่ถูกนั่งพร้อมกัน'})
        st.plotly_chart(fig_conc, use_container_width=True)
        
        st.markdown('<div class="verdict-false">❌ ข้อสรุป Comment 2: ไม่จริง (False)<br>- ปริมาณลูกค้ารายวันต่างกันถึง 50.9% และความแน่นช่วง Peak ต่างกันชัดเจน (16 โต๊ะ vs 23 โต๊ะ) ภาระงานไม่ได้เท่ากันทุกวัน สามารถจัดสรรกำลังคนแบบ Dynamic ตามวันได้</div>', unsafe_allow_html=True)

    # --- Comment 3 Tab ---
    with t1_tab3:
        st.markdown("### Comment 3: *'Walk-in นั่งนานทั้งวัน หาโต๊ะให้ In-house ไม่ได้'*)")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("เวลานั่งเฉลี่ย (Walk-in)", "72.8 นาที", "มัธยฐาน 66.0 นาที")
        c2.metric("เวลานั่งเฉลี่ย (In-house)", "45.8 นาที", "มัธยฐาน 39.0 นาที")
        c3.metric("การครองความจุโต๊ะ (Walk-in)", "69.2%", "322.7 Table-Hours")
        c4.metric("Walk-in แช่ขวางโต๊ะ (Overlaps)", "19 ครั้ง", "นั่งเฉลี่ย 102.3 นาที")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            fig_dwell = px.box(df[df['dwell_time_min'].notnull()], x='Guest_type', y='dwell_time_min',
                               color='Guest_type', color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                               title="ระยะเวลานั่งทาน Dwell Time (นาที)")
            st.plotly_chart(fig_dwell, use_container_width=True)
            
        with col2:
            tbl_hours = df[df['table_minutes'].notnull()].groupby('Guest_type')['table_minutes'].sum().reset_index()
            tbl_hours['hours'] = tbl_hours['table_minutes'] / 60.0
            fig_share = px.pie(tbl_hours, names='Guest_type', values='hours', hole=0.4,
                               color='Guest_type', color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                               title="สัดส่วนการครองความจุโต๊ะ (Table-Hours)")
            st.plotly_chart(fig_share, use_container_width=True)
            
        with col3:
            blockers = df_overlap.groupby('curr_group_guest_type').size().reset_index(name='blocking_events')
            fig_block = px.bar(blockers, x='curr_group_guest_type', y='blocking_events', text_auto=True,
                               color='curr_group_guest_type', color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                               title="กลุ่มที่นั่งแช่ขวางโต๊ะในเหตุการณ์ Overlap")
            st.plotly_chart(fig_block, use_container_width=True)
            
        st.markdown('<div class="verdict-true">✅ ข้อสรุป Comment 3: จริงอย่างยิ่ง (True - Strongly Supported)<br>- Walk-in นั่งนานกว่า In-house อย่างมีนัยสำคัญ (72.8 นาที vs 45.8 นาที) และครองความจุโต๊ะรวมไปถึง 69.2% รวมถึงเป็นตัวการนั่งแช่ขวางโต๊ะถึง 19 จาก 31 เหตุการณ์</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 3: TASK 2 - MANAGEMENT ACTIONS DISPROOF
# ==========================================
elif page == "🛑 Task 2: Management Actions Disproof":
    st.markdown('<div class="main-header">🛑 Task 2: หักล้างข้อเสนอฝ่ายบริหาร</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">พิสูจน์ด้วยข้อมูลว่าทำไม 3 มาตรการเดิมจึงไม่สามารถแก้ปัญหาได้</div>', unsafe_allow_html=True)
    
    act1, act2, act3 = st.tabs([
        "Action 1: ลดเวลานั่งจาก 5 ชม.",
        "Action 2: ขึ้นราคาเป็น 259 ทุกวัน",
        "Action 3: ให้ In-house แซงคิว"
    ])
    
    # --- Action 1 ---
    with act1:
        st.markdown("### Action 1: *'ลดเวลานั่งจาก 5 ชม. เป็นน้อยลง'*")
        
        df_dwell = df[df['dwell_time_min'].notnull()].copy()
        gt_240 = (df_dwell['dwell_time_min'] > 240).sum()
        le_90 = (df_dwell['dwell_time_min'] <= 90).sum()
        
        c1, c2 = st.columns(2)
        c1.metric("กลุ่มที่นั่ง > 4 ชั่วโมง", f"{gt_240} กลุ่ม (0.29%)", "แทบไม่มีอยู่จริง!")
        c2.metric("กลุ่มที่นั่ง <= 90 นาที", f"{le_90} กลุ่ม (82.8%)", "ลูกค้าส่วนใหญ่เสร็จเร็ว")
        
        fig_hist = px.histogram(df_dwell, x='dwell_time_min', nbins=30, color='Guest_type',
                                color_discrete_map={'In house': '#2B5C8F', 'Walk in': '#D95F02'},
                                title="การกระจายตัวของระยะเวลานั่งทาน (Dwell Time Distribution)")
        fig_hist.add_vline(x=90, line_dash="dash", line_color="orange", annotation_text="82.8% นั่งเสร็จใน 90 นาที")
        fig_hist.add_vline(x=300, line_dash="dash", line_color="red", annotation_text="เพดานเดิม 5 ชม.")
        st.plotly_chart(fig_hist, use_container_width=True)
        
        st.markdown('<div class="verdict-false">🛑 ทำไม Action 1 จึงไม่ได้ผล (Disproof):<br>มีลูกค้าเพียง 0.29% (1 จาก 348 กลุ่ม) ที่นั่งเกิน 4 ชม. จริง การลดเพดานเวลาแบบเหมาเข่งทั้งวันเป็นการแก้ปัญหาผิดจุดที่ "หางของ Distribution" ไม่ช่วยเพิ่ม Turnover Rate ของโต๊ะในช่วงพีคที่ Walk-in นั่งเฉลี่ย 66-73 นาที</div>', unsafe_allow_html=True)

    # --- Action 2 ---
    with act2:
        st.markdown("### Action 2: *'ขึ้นราคาเป็น 259 บาททุกวัน'*")
        
        c1, c2 = st.columns(2)
        c1.metric("Peak Concurrency วันคนน้อย (Day A)", "16 โต๊ะพร้อมกัน", "โต๊ะแน่นแม้คนน้อย")
        c2.metric("Peak Concurrency วันคนมาก (Day C)", "23 โต๊ะพร้อมกัน", "ความแน่นพุ่งสูง")
        
        daily_grp = df.groupby('day_id').size().reset_index(name='total_groups')
        fig_vol = px.bar(daily_grp, x='day_id', y='total_groups', text_auto=True,
                         title="จำนวนกลุ่มลูกค้ารายวัน เทียบกับ Peak Concurrency",
                         color_discrete_sequence=['#2B5C8F'])
        st.plotly_chart(fig_vol, use_container_width=True)
        
        st.markdown('<div class="verdict-false">🛑 ทำไม Action 2 จึงไม่ได้ผล (Disproof):<br>แม้วันที่มีลูกค้าน้อยที่สุด (Day A: 57 กลุ่ม) ช่วง Peak ก็ยังมีลูกค้านั่งพร้อมกันถึง 16 โต๊ะ ต้นเหตุเกิดจาก "Turnover Rate ต่อโต๊ะในช่วง Peak" ไม่ใช่จำนวนคนรวมทั้งวัน การขึ้นราคาถาวรเป็นการลงโทษลูกค้าช่วง Off-peak และทำลายแคมเปญ TikTok</div>', unsafe_allow_html=True)

    # --- Action 3 ---
    with act3:
        st.markdown("### Action 3: *'ให้สิทธิ์ In-house แซงคิว (Queue-Skipping)'*")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("ความจุโต๊ะที่ Walk-in ครอง", "69.2%", "ครองโต๊ะ 2/3 ร้าน")
        c2.metric("In-house Walk-away Rate", "28.0%", "ทิ้งคิวสูงอยู่แล้ว")
        c3.metric("In-house เป็นตัวขวางโต๊ะ", "12 ครั้ง", "แช่โต๊ะเฉลี่ย 66.2 นาที")
        
        st.markdown('<div class="verdict-false">🛑 ทำไม Action 3 จึงไม่ได้ผล (Disproof):<br>การแซงคิวเป็นเพียงการ "สลับลำดับการรอ" แต่ไม่ได้เพิ่ม "จำนวนโต๊ะกายภาพ" ในเมื่อโต๊ะ 69.2% ถูก Walk-in นั่งครองอยู่ การปล่อยให้ In-house แซงคิวก็ไม่มีโต๊ะว่างให้อยู่ดี แถมยังผลักให้ Walk-in รอนานวิกฤตจนเกิดรีวิวเชิงลบ</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 4: TASK 3 - SUPPORTED STRATEGY
# ==========================================
elif page == "💡 Task 3: Supported Strategy":
    st.markdown('<div class="main-header">💡 Task 3: ข้อเสนอแนะยุทธศาสตร์ที่สนับสนุน</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">มาตรการ Tiered Peak-Window Soft Cap (90–100 นาที) เพื่อแก้ปัญหาคอขวดอย่างยั่งยืน</div>', unsafe_allow_html=True)
    
    st.info("💡 **แนวคิดยุทธศาสตร์:** นำ Action 1 มาปรับปรุงโดยเปลี่ยนจากเพดานเดี่ยวทั้งวัน เป็น **'การจำกัดเวลาแบบแบ่งช่วงเวลา (Tiered Approach)'** เพื่อรักษาจุดขาย TikTok Promo ในช่วง Off-peak และควบคุม Turnover ในช่วง Peak")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🕒 1. Off-Peak Windows (06:00-08:00 & 10:00-13:00 น.)")
        st.success("**นโยบาย:** ไม่จำกัดเวลานั่งเพิ่ม (ให้สิทธิ์ 5 ชม. ตามเดิม)\n- **ผลลัพธ์:** รักษาจุดขายแคมเปญ TikTok ('All You Can Eat / นั่งยาว 5 ชม.')")
    with c2:
        st.markdown("#### ⚡ 2. Peak Window (08:00-10:00 น.)")
        st.warning("**นโยบาย:** Soft Cap 90–100 นาที พร้อมขั้นตอนปฏิบัติการหน้าร้าน\n- **ผลลัพธ์:** ควบคุมเวลานั่งของกลุ่มที่นั่งแช่ เร่งการหมุนเวียนโต๊ะ")
        
    st.markdown("---")
    st.subheader("📊 ผลการจำลองข้อมูลการประหยัดความจุโต๊ะ (Simulation Results)")
    
    df_peak_seated = df[(df['meal_start_min'] >= 480) & (df['meal_start_min'] <= 600) & df['dwell_time_min'].notnull()].copy()
    df_peak_seated['capped_dwell_90'] = df_peak_seated['dwell_time_min'].apply(lambda x: min(x, 90.0))
    df_peak_seated['table_mins_original'] = df_peak_seated['dwell_time_min'] * df_peak_seated['n_units']
    df_peak_seated['table_mins_capped'] = df_peak_seated['capped_dwell_90'] * df_peak_seated['n_units']
    
    mins_saved = df_peak_seated['table_mins_original'].sum() - df_peak_seated['table_mins_capped'].sum()
    hours_saved = mins_saved / 60.0
    slots_created = mins_saved / 45.0
    
    s1, s2, s3 = st.columns(3)
    s1.metric("ความจุที่ประหยัดได้ช่วง Peak", f"{hours_saved:.1f} Table-Hours", f"{mins_saved:.0f} นาทีโต๊ะ")
    s2.metric("รอบโต๊ะที่เพิ่มขึ้นช่วง Peak", f"~{slots_created:.0f} กลุ่มใหม่", "คิดที่ turnover 45 นาที")
    s3.metric("กลุ่มที่ได้รับการปกป้อง", "82.8% ของลูกค้า", "นั่งเสร็จใน 90 นาทีอยู่แล้ว")
    
    fig_sim = px.histogram(df_peak_seated, x='dwell_time_min', nbins=20,
                           title="การกระจายตัวเวลานั่งทานช่วง Peak (08:00-10:00 น.) เทียบกับ Soft Cap 90 นาที",
                           color_discrete_sequence=['#2B5C8F'])
    fig_sim.add_vline(x=90, line_dash="dash", line_color="red", annotation_text="Proposed Soft Cap (90 min)")
    st.plotly_chart(fig_sim, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🛠️ ข้อเสนอแนะเชิงปฏิบัติการเพิ่มเติม (Operational Strategy)")
    st.markdown("""
    1. **Mandatory Queue Data Logging:** บังคับให้บันทึกเวลาคิว (`queue_start` / `queue_end`) ให้ครบทุกวัน เพื่อใช้วัดผลความเร็วในการระบายคิว
    2. **In-House Buffer Tables:** สำรองโต๊ะ Indoor โซนใกล้ไลน์อาหาร (โต๊ะ 1A–3B รวม 6 ยูนิตย่อย) ไว้เฉพาะ In-house ในช่วง 07:30–09:30 น. เพื่อลดอัตรา Walk-away 28.0%
    3. **Soft-Cap Service Protocol:** ฝึกพนักงานให้เข้าบริการเชิงรุกในนาทีที่ 75 (เช่น "สอบถามการรับเครื่องดื่ม/ของหวานเพิ่ม") เพื่อส่งสัญญาณเตือนอย่างสุภาพ
    """)

# ==========================================
# PAGE 5: DATA QUALITY & DATA EXPLORER
# ==========================================
elif page == "📋 Data Quality & Explorer":
    st.markdown('<div class="main-header">📋 Data Quality & Raw Data Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">สำรวจชุดข้อมูลที่ทำความสะอาดแล้ว บันทึก DQ Issues และ Log เหตุการณ์โต๊ะนั่งซ้อน</div>', unsafe_allow_html=True)
    
    dq_tab1, dq_tab2, dq_tab3 = st.tabs([
        "Cleaned Dataset (363 Rows)",
        "Data Quality Master List (58+ Issues)",
        "Table Overlap Log (31 Events)"
    ])
    
    with dq_tab1:
        st.markdown("### 🔍 Cleaned Dataset (`cleaned_stage1.csv`)")
        guest_filter = st.multiselect("กรองประเภทลูกค้า (Guest Type):", options=df['Guest_type'].unique(), default=df['Guest_type'].unique())
        day_filter = st.multiselect("กรองวันบริการ (Service Day):", options=df['day_id'].unique(), default=df['day_id'].unique())
        
        df_filtered = df[(df['Guest_type'].isin(guest_filter)) & (df['day_id'].isin(day_filter))]
        st.dataframe(df_filtered, use_container_width=True)
        st.caption(f"แสดงข้อมูล {len(df_filtered)} จากทั้งหมด {len(df)} แถว")
        
    with dq_tab2:
        st.markdown("### ⚠️ Data Quality Master List (`UNRESOLVED_MASTER_LIST.csv`)")
        if not df_unresolved.empty:
            cat_filter = st.multiselect("กรองประเภทปัญหา (Issue Category):", options=df_unresolved['issue_category'].unique(), default=df_unresolved['issue_category'].unique())
            df_unres_filtered = df_unresolved[df_unresolved['issue_category'].isin(cat_filter)]
            st.dataframe(df_unres_filtered, use_container_width=True)
            st.caption(f"แสดงปัญหา {len(df_unres_filtered)} จากทั้งหมด {len(df_unresolved)} รายการ")
        else:
            st.info("ไม่พบไฟล์ UNRESOLVED_MASTER_LIST.csv")
            
    with dq_tab3:
        st.markdown("### 🔄 Table Overlap Log (`table_overlap_log.csv`)")
        if not df_overlap.empty:
            st.dataframe(df_overlap, use_container_width=True)
            st.caption(f"แสดงเหตุการณ์โต๊ะนั่งซ้อนทั้งหมด {len(df_overlap)} ครั้ง")
        else:
            st.info("ไม่พบไฟล์ table_overlap_log.csv")
