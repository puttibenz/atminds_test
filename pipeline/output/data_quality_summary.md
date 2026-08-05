# Data Quality & Cleaning Summary — Pipeline Stages 0 to 4
**Hotel Amber 85 · Breakfast Buffet Data Analysis**

---

## 1. ภาพรวมการดำเนินงาน (Executive Overview)

การประมวลผลข้อมูลในส่วนนี้ครอบคลุม **Pipeline Stage 0 ถึง Stage 4** ตามข้อกำหนดในคู่มือการวิเคราะห์ โดยประมวลผลจากไฟล์ข้อมูลดิบ `2026 Data Test1 Final - Busy Buffet Dataset.xlsx` จำนวน 5 Sheet (`133`, `143`, `153`, `173`, `183`) รวมเป็นข้อมูลบริการ 5 วัน (Day A ถึง Day E)

### 📊 สรุปจำนวนข้อมูลในแต่ละ Stage
* **Raw Data (Stage 0):** 364 แถว
* **Completely Empty Row:** 1 แถว (Day D, service_no 70) ➔ ถูกตัดออกในการ Cleaning (Stage 2)
* **Cleaned Dataset (Stage 2–4):** **363 แถว** (บันทึกใน [`cleaned_stage1.csv`])
* **Data Quality Issues Logged:** บันทึกลง [`UNRESOLVED_MASTER_LIST.csv`]
* **Table Double-Booking Overlaps:** 31 เหตุการณ์ (บันทึกใน [`table_overlap_log.csv`])

---

## 2. รายละเอียดข้อบกพร่องของข้อมูล (Data Quality Audit Summary)

เพื่อรักษาความน่าเชื่อถือของการวิเคราะห์ **ไม่มีการลบแถวข้อมูลที่มีประโยชน์ทิ้ง** (ยกเว้นแถวว่างเปล่า 1 แถว) โดยใช้วิธี Flag และบันทึกปัญหาลงใน Master List แล้วคัดออกเฉพาะในการคำนวณ Metric ที่อาจเกิดความบิดเบือนเท่านั้น

| หมวดหมู่ปัญหา | จำนวน | ตัวอย่าง / ตำแหน่งที่พบ | วิธีการจัดการใน Pipeline |
|---|---|---|---|
| **1. Empty Row** | 1 | Day D, service_no 70 (ไม่มีข้อมูลทุกฟีลด์) | Drop แถวออก |
| **2. Invalid Pax (`pax = 0` / null)** | 8 | Day C: service_no 7, 21, 28, 40, 49, 60, 78 + Day D: 70 | กำหนดเป็น Unknown pax, ยกเว้นเฉพาะ pax-weighted metric |
| **3. Negative Dwell Time** | 1 | Day E, service_no 62 (`meal_start` 11:53 ➔ `meal_end` 11:28) | กำหนด `dwell_time_min = NaN`, ยกเว้นเฉพาะการหาค่าเฉลี่ย Dwell time |
| **4. Unmapped Table / Table 16** | 24 | พบโต๊ะระบุเลข "16" (ไม่มีในผังร้าน) 24 กลุ่ม | กำหนดเป็น Unknown Zone/Table, ยกเว้นเฉพาะ Capacity metric |
| **5. Missing Seated Table** | 5 | กลุ่มที่ได้นั่งทานอาหาร แต่ไม่บันทึกเลขโต๊ะ | กำหนดเป็น Unknown Table |
| **6. Ambiguous Outdoor Section Suffix** | 19 | โต๊ะ 7, 8, 9, 10, 11 เขียนเลขเดี่ยว ไม่มี A/B/C | Map เข้า Outdoor Zone โดยถือเป็นโต๊ะรวมทุกยูนิตย่อย |
| **7. Table Setup Discrepancy (15A/15B)** | 5 | ระบุ 15A / 15B (ขัดกับคู่มือที่บอกโต๊ะ 15 เป็นโต๊ะเต็ม) | Map เข้า Outdoor Zone |
| **8. Cross-Zone Combined Table** | 1 | ระบุโต๊ะ `4A/11B` (รวมโต๊ะ Indoor 4A กับ Outdoor 11B) | แยกยูนิตเป็น 4A (Indoor) และ 11B (Outdoor) |

---

## 3. สรุปกระบวนการ Cleaning & Feature Engineering

### 3.1 การแปลงค่าและ Standardize ข้อมูล (Stage 2)
1. **Time Parsing:** แปลง `queue_start`, `queue_end`, `meal_start`, `meal_end` จากข้อความ HH:MM:SS ให้เป็นตัวเลขนาทีนับจากเที่ยงคืน (เช่น 06:00 = 360 นาที) เพื่อให้คำนวณระยะเวลาได้ถูกต้อง 100%
2. **Table Unit Parsing:** แยกตัวเชื่อม `-` และ `/` ออกเป็นยูนิตโต๊ะย่อยทางกายภาพ (Physical Units):
   - `13-14` ➔ `['13', '14']`
   - `1A-1B` ➔ `['1A', '1B']`
   - `4A/11B` ➔ `['4A', '11B']`
3. **Zone Mapping (การกำหนดโซนที่นั่ง):**
   - **Indoor Zone:** `1A, 1B, 2A, 2B, 3A, 3B, 4A, 4B, 5A, 5B, 6A, 6B`
   - **Outdoor Zone:** `7A..7C, 8A..8C, 9A..9C, 10A..10B, 11A..11B, 12, 13, 14, 15, 15A, 15B`
   - **Queueing Area:** `99`
   - **Unknown Zone:** `16` หรือ null

### 3.2 ฟีเจอร์ใหม่ที่สร้างขึ้น (Stage 3)
* `wait_time_min`: ระยะเวลารอคิว (นาที) = `queue_end - queue_start`
* `dwell_time_min`: ระยะเวลาในการรับประทานอาหาร (นาที) = `meal_end - meal_start`
* `is_walk_away`: Flag (`True`/`False`) กลุ่มที่รอคิวแต่ทิ้งคิวไม่ได้นั่งทาน (`queue` มีข้อมูล + `meal_start` ไม่มีข้อมูล)
* `is_direct_seating`: Flag (`True`/`False`) กลุ่มที่ได้นั่งทานทันทีโดยไม่ต้องรอคิว
* `n_units`: จำนวนยูนิตโต๊ะที่กลุ่มนั้นใช้งาน
* `table_minutes`: `dwell_time_min × n_units` (ปริมาณการครองความจุโต๊ะจริง)
* `primary_zone`: โซนหลักของกลุ่มลูกค้า (`Indoor`, `Outdoor`, `Queueing Area`, `Cross-Zone`, `Unknown`)

---

## 4. ผลการตรวจสอบ Validation & Table Overlaps (Stage 4)

จากการตรวจสอบช่วงเวลานั่งทานจริงเทียบตามยูนิตโต๊ะรายวัน (Double-booking / Overlap Audit):
* พบการนั่งซ้อนกันของกลุ่มลูกค้าบนโต๊ะย่อยเดียวกันในเวลาเดียวกัน **31 ครั้ง** (เช่น กลุ่มก่อนหน้ายังไม่ลุก แต่กลุ่มถัดมาระบุเวลาเริ่มนั่งทับช่วงกัน)
* รายละเอียดทั้งหมดถูกบันทึกไว้ใน [`table_overlap_log.csv`] เพื่อนำไปวิเคราะห์ผลกระทบใน Task 1 Comment 3 ต่อไป

---

## 5. ไฟล์ผลลัพธ์ (Deliverable Files)

1. **Jupyter Notebook:** [`notebook/data_quality_and_cleaning.ipynb`] (ซอร์สโค้ดและคำอธิบาย End-to-End)
2. **Cleaned Dataset:** [`pipeline/output/cleaned_stage1.csv`] (ชุดข้อมูลที่ทำความสะอาดและใส่ฟีเจอร์แล้ว 363 แถว)
3. **Data Quality Master Log:** [`pipeline/output/UNRESOLVED_MASTER_LIST.csv`] (บันทึกข้อบกพร่องของข้อมูล)
4. **Table Overlap Log:** [`pipeline/output/table_overlap_log.csv`] (บันทึกเหตุการณ์นั่งซ้อน 31 ครั้ง)
