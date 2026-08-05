# HOTEL AMBER 85 — BREAKFAST BUFFET DATA ANALYTICS & STRATEGIC REVIEW
**Executive Report & Commentary for Management**  
*Atmind Data Analytics Test 2026 — Busy Buffet Project*

---

## EXECUTIVE SUMMARY

Following a highly successful promotion on TikTok featuring an "All You Can Eat / 159 THB weekday & 199 THB weekend / 5-Hour Seating Time" offer, Hotel Amber 85 experienced a sudden influx of walk-in guests. While demand surged, operational management faced severe customer queueing, table shortages, and friction between hotel guests (In-house) and walk-in visitors.

To resolve these challenges empirically, the Data Analytics Team conducted an end-to-end evaluation of **5 operational service days** (363 cleaned customer group records). This report presents the definitive findings across three key tasks:

1. **Task 1 (Staff Comments Audit):** Evaluated three front-line staff claims. Proved that Walk-in guests wait longer (44.5 min median) but In-house guests abandon queues at nearly double the rate (28.0% vs 14.6%). Confirmed that Walk-in guests sit significantly longer (72.8 min avg) and consume **69.2% of total table capacity**, creating the primary operational bottleneck. Disproved the claim that daily workload is uniform across the week.
2. **Task 2 (Management Actions Disproof):** Evaluated three candidate management actions. Proved why a flat seating limit reduction targets the wrong tail (82.8% finish <= 90 mins; only 0.29% stay > 4 hrs), why a daily price hike fails (peak congestion reaches 16 tables even on the lightest day), and why queue-skipping for In-house guests fails to create physical table capacity.
3. **Task 3 (Supported Strategy):** Formulated a **Tiered Peak-Window Soft Cap Strategy (90–100 minutes between 08:00–10:00 AM)**. Preserves the viral TikTok promotion during off-peak hours while liberating **22.1 Table-Hours** of peak capacity, creating **~29 additional seating slots** during peak breakfast hours.

---

### EXECUTIVE MASTER DECISION MATRIX

| Task / Area | Subject / Proposal | Key Empirical Data Finding | Verdict & Operational Impact |
|---|---|---|---|
| **Task 1: Comment 1** | In-house wait long / Walk-in abandon queue | Walk-in wait median is 44.5 m (vs In-house 28.0 m). In-house walk-away rate is 28.0% (vs Walk-in 14.6%). | **PARTIALLY TRUE** — Must prioritize In-house queue retention. |
| **Task 1: Comment 2** | Equal workload every day of the week | Daily group volume varies by 50.9% (57 to 86 groups). Peak concurrency varies from 16 to 23 tables. | **FALSE** — Dynamic staffing & buffer allocation required. |
| **Task 1: Comment 3** | Walk-in sit all day & block tables | Walk-in average dwell is 72.8 m (vs In-house 45.8 m). Walk-in holds 69.2% capacity & causes 19 blocker overlaps. | **TRUE** — Walk-in dwell is the core operational bottleneck. |
| **Task 2: Action 1** | Reduce 5-hr limit to less (Flat) | Only 0.29% (1 group) stays > 4 hrs. 82.8% finish <= 90 mins. Targets non-existent tail problem. | **WILL NOT WORK** — Flat reduction lacks operational focus. |
| **Task 2: Action 2** | Increase price to 259 THB daily | Peak concurrency reaches 16 tables even on lightest day (Day A). Congestion is peak turnover, not daily volume. | **WILL NOT WORK** — Punishes off-peak guests; damages brand momentum. |
| **Task 2: Action 3** | In-house queue-skipping priority | Walk-in holds 69.2% of physical tables. Skipping queue does not add physical seats. | **WILL NOT WORK** — Pushes Walk-in wait into extreme crisis. |
| **Task 3: Strategy** | **Tiered Peak Soft Cap (90–100 min)** | Enforce 90-100 min soft cap ONLY during 08:00-10:00 AM peak; maintain 5-hr unlimited benefit off-peak. | **RECOMMENDED STRATEGY** — Saves 22.1 Table-Hours (+29 slots). |

---

## 1. DATA PIPELINE & DATA QUALITY OVERVIEW

The dataset provided (`2026 Data Test1 Final - Busy Buffet Dataset.xlsx`) contains 5 independent service days (`133`, `143`, `153`, `173`, `183` mapped as `Day A` through `Day E`). Across 364 raw records, rigorous Data Quality auditing was performed:

- **1 Completely Empty Row:** Day D service_no 70 dropped from dataset.
- **7 Invalid Pax Records (`pax = 0`):** Flagged as Unknown pax to prevent distortion of pax-weighted averages while retaining timing data.
- **1 Negative Dwell Time Record:** Day E service_no 62 (`meal_start` 11:53 -> `meal_end` 11:28) flagged as NaN dwell time.
- **58+ Master Data Quality Issues:** Logged comprehensively into `UNRESOLVED_MASTER_LIST.csv`.
- **Physical Table Unit Parsing:** Split combined table strings (`13-14`, `1A-1B`, `4A/11B`) into constituent seating units and mapped to `Indoor`, `Outdoor`, and `Queueing Area` zones.
- **Table Double-Booking Overlaps:** Detected 31 instances where two groups occupied the same table unit concurrently on the same day (`table_overlap_log.csv`).

---

## 2. TASK 1: PROVING & DISPROVING STAFF COMMENTS

### 2.1 Comment 1 Audit: Wait Time & Queue Abandonment
> **Staff Claim:** *"In-house customers are unhappy that they have to wait for a table. Walk-in customers are also unhappy, when they queue up for a long time and leave the queue because they don't want to wait any longer."*

To test this claim, we analyzed all queuing groups (recorded on Day B & Day C, total 73 queuing groups):

1. **Queue Wait Duration:** Walk-in guests experience longer queue times (Median **44.5 minutes**, Mean **38.4 minutes**) compared to In-house hotel guests (Median **28.0 minutes**, Mean **30.6 minutes**).
2. **Queue Abandonment (Walk-Away Rate):** Contrary to staff perceptions, **In-house hotel guests abandon queues at nearly double the rate of Walk-in guests**. 7 out of 25 queuing In-house groups walked away (**28.0% walk-away rate**), whereas only 7 out of 48 queuing Walk-in groups abandoned (**14.6% walk-away rate**).

`[INSERT_CHART_HERE: Wait Time Distribution Boxplot (In-House vs Walk-In)]`

`[INSERT_CHART_HERE: Walk-Away Rate Percentage Bar Chart]`

**Verdict: PARTIALLY TRUE**  
Walk-in guests do wait longer, but staff mistakenly assumed Walk-in guests abandon queues most often. In reality, hotel guests have much lower wait tolerance and represent the primary walk-away risk.

---

### 2.2 Comment 2 Audit: Daily Operational Workload
> **Staff Claim:** *"We are very busy every day of the week. If it's going to be this busy every week I think it's impossible to sustain this business."*

To test operational uniformity, we evaluated total customer volume and constructed **15-minute sliding window seated concurrency curves** (06:00 to 12:45 AM):

1. **Daily Volume Variation:** Customer volume varies significantly across days, ranging from **57 groups (102 Pax) on Day A** to **86 groups (166 Pax) on Day C** — representing a **50.9% volume difference**.
2. **Peak Concurrency Variation:** Seated concurrency on Day A peaked at only 16 simultaneous groups, whereas Day C and Day D reached peak stress levels of 20 to 23 simultaneous groups.

`[INSERT_CHART_HERE: Total Serviced Groups per Day Bar Chart]`

`[INSERT_CHART_HERE: 15-Minute Seated Concurrency Curves (06:00 - 12:45)]`

**Verdict: FALSE**  
Operational load is not uniform across days. Management can optimize staffing dynamically based on day-of-week demand patterns rather than treating every day as an unsustainably heavy day.

---

### 2.3 Comment 3 Audit: Walk-In Dwell Time & Table Bottlenecks
> **Staff Claim:** *"Walk-in customers sit the whole day. It's very difficult to find seats for in-house customers. We don't have enough tables so when one customer sits for a long time it makes the queue very long."*

To evaluate capacity monopolization, we analyzed customer dwell duration, total table-capacity hours (`dwell_time * n_units`), and table double-booking overlap logs:

1. **Dwell Time Disparity:** Walk-in guests sit significantly longer than In-house guests. Walk-in dwell averages **72.8 minutes** (Median **66.0 minutes**, P75 **91.5 minutes**), whereas In-house dwell averages **45.8 minutes** (Median **39.0 minutes**).
2. **Table Capacity Monopolization:** Walk-in guests consume **69.2% of total table-capacity hours** (322.7 Table-Hours), leaving only **30.8%** (143.5 Table-Hours) for hotel guests.
3. **Table Blocking Overlaps:** Out of 31 table double-booking events, Walk-in guests were the overstaying "blocking group" in **19 instances**, with an average blocking dwell time of **102.3 minutes**.

`[INSERT_CHART_HERE: Customer Dwell Time Distribution Boxplot]`

`[INSERT_CHART_HERE: Table Capacity Share Pie Chart (Table-Hours)]`

`[INSERT_CHART_HERE: Double-Booking Blocker Events Bar Chart]`

**Verdict: TRUE (Strongly Supported)**  
Walk-in guests sit substantially longer, monopolize over two-thirds of restaurant capacity, and represent the primary cause of table bottlenecks and queue backup.

---

## 3. TASK 2: DISPROVING RECOMMENDED MANAGEMENT ACTIONS

Prior to data collection, hotel management considered three potential interventions. Our empirical analysis disproves all three options:

---

### 3.1 Disproving Action 1: Reduce Seating Time Limit (5 Hours to Less)
> **Management Proposal:** *"Reduce seating time limit from 5 hours to a shorter duration across the board."*

**Empirical Disproof:**
1. **Extremely Low Occurrence of 4–5 Hour Stays:** Out of 348 valid customer groups, **only 1 group (0.29%)** stayed longer than 4 hours.
2. **Most Customers Finish Quickly:** **82.8% of all customer groups finish dining within 90 minutes**.

`[INSERT_CHART_HERE: Customer Dwell Time Histogram with 90-Min and 300-Min Cutoffs]`

**Why It Fails:**  
Imposing a flat daily limit reduction (e.g. capping seating at 3 hours) targets a non-existent tail problem. It does nothing to accelerate table turnover during the 08:00–10:00 AM peak window where median Walk-in dwell is 66–73 minutes.

**Verdict: WILL NOT WORK**

---

### 3.2 Disproving Action 2: Increase Price Everyday to 259 THB
> **Management Proposal:** *"Increase buffet price to 259 THB every day of the week."*

**Empirical Disproof:**
1. **Peak Congestion Occurs Even on Low-Volume Days:** On Day A (the lightest day with only 57 groups), peak seated concurrency still reached **16 simultaneous tables** during 08:30–09:30 AM, causing queue congestion.

`[INSERT_CHART_HERE: Daily Total Groups vs Peak Hour Seated Concurrency Combo Chart]`

**Why It Fails:**  
Congestion is driven by **table turnover rate during peak morning hours**, not by total daily volume. A flat price hike penalizes off-peak customers, damages viral TikTok marketing momentum, and fails to control peak-hour table hogging.

**Verdict: WILL NOT WORK**

---

### 3.3 Disproving Action 3: Queue-Skipping Priority for In-House Guests
> **Management Proposal:** *"Give In-house hotel guests queue-skipping priority over Walk-in guests."*

**Empirical Disproof:**
1. **Does Not Create Table Supply:** Walk-in guests occupy **69.2% of physical tables**. Skipping the queue changes the order of waiting but creates zero physical seats.
2. **Increases Walk-In Frustration:** Walk-in guests already wait 44.5 minutes. Pushing them back in line will cause extreme wait times and bad online reviews.
3. **In-House Guests Also Block Tables:** In-house guests were the blocking group in 12 overlap events (avg dwell 66.2 mins).

`[INSERT_CHART_HERE: Action 3 Comparative Metrics Bar Chart]`

**Verdict: WILL NOT WORK**

---

## 4. TASK 3: SUPPORTED RECOMMENDED STRATEGY

### 4.1 Recommended Solution: Tiered Peak-Window Soft Cap (90–100 Minutes)

We adapt Management Action 1 into a **Time-Tiered Soft Cap Strategy**:

- **Off-Peak Windows (06:00–08:00 AM & 10:00 AM–01:00 PM):** Maintain full 5-hour unlimited seating benefit. Preserves the core promotional promise of the TikTok marketing campaign.
- **Peak Window (08:00–10:00 AM):** Enforce a **Soft Cap of 90–100 Minutes** on seating.

---

### 4.2 Quantitative Capacity Simulation

Capping peak Walk-in dwell times at 90 minutes yields significant capacity gains:
- **Peak Table Capacity Saved:** **22.1 Table-Hours** (1,324 table-minutes) liberated during 08:00–10:00 AM.
- **Additional Seating Slots:** Creates **~29 additional table seating slots** during peak hours (assuming 45-minute turnover), directly resolving table shortages without capital expenditure.
- **Protects 82.8% of Guests:** 82.8% of customers naturally finish within 90 minutes and experience zero disruption.

`[INSERT_CHART_HERE: Peak Window Dwell Time Histogram & 90-Min Soft Cap Overlay]`

---

### 4.3 Operational Implementation Guidelines

1. **Mandatory Queue Data Logging:** Require front-desk staff to log `queue_start` and `queue_end` every day to track wait time improvements continuously.
2. **In-House Buffer Table Reservation:** Reserve 4 to 6 Indoor split tables (Tables 1A–3B) exclusively for In-house guests between 07:30 and 09:30 AM to eliminate the 28.0% In-house walk-away rate.
3. **Staff Soft-Cap Service Protocol:** Train staff to offer proactive table check-ins at minute 75 ("May I offer you a coffee refill or dessert?") during peak hours, creating a subtle, hospitable signal for table wrap-up.

---

## 5. CONCLUSION & ACTION MATRIX

By implementing the **Tiered Peak-Window Soft Cap Strategy**, Hotel Amber 85 can resolve peak breakfast congestion, protect hotel guest satisfaction, and sustain profitable walk-in buffet revenue.
