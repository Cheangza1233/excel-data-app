import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. การตั้งค่าหน้าเว็บ (Config) ---
st.set_page_config(page_title="DataMaster Pro (Private)", page_icon="🔒", layout="wide")

# --- 2. ระบบความปลอดภัย (Login System) ---
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        # *** คุณสามารถเปลี่ยนรหัสผ่านตรง 'admin123' เป็นคำที่ต้องการได้ ***
        if st.session_state["password"] == "admin123": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # ลบรหัสออกจาก session เพื่อความปลอดภัย
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # หน้าจอ Login
        st.markdown("<h2 style='text-align: center;'>🔒 กรุณาใส่รหัสผ่านเพื่อเข้าใช้งาน</h2>", unsafe_allow_html=True)
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='text-align: center;'>🔒 กรุณาใส่รหัสผ่านเพื่อเข้าใช้งาน</h2>", unsafe_allow_html=True)
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("❌ รหัสผ่านไม่ถูกต้อง")
        return False
    else:
        return True

# ตรวจสอบรหัสผ่านก่อนรันแอปส่วนที่เหลือ
if not check_password():
    st.stop()

# --- 3. ส่วนของ UI Dashboard (จะทำงานเมื่อ Login ผ่านแล้วเท่านั้น) ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stSidebar"] { background-color: #1a2a3a; color: white; }
    div[data-testid="metric-container"] {
        background-color: white; padding: 20px; border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2f1;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 DataMaster Admin Panel (Secure Mode)")
st.markdown("---")

# --- 4. เมนู Sidebar (รวม Google Sheets + Upload ไฟล์) ---
st.sidebar.title("🛠️ จัดการข้อมูล")

# ส่วนที่ 1: เชื่อมต่อ Google Sheets (Google Drive)
st.sidebar.subheader("🔗 เชื่อม Google Sheets")
gsheet_url = st.sidebar.text_input("วางลิงก์ Google Sheets (ต้องเปิดแชร์สาธารณะ):")

# ส่วนที่ 2: อัปโหลดไฟล์จากคอมพิวเตอร์
st.sidebar.subheader("📤 หรืออัปโหลดไฟล์ตรง")
uploaded_files = st.sidebar.file_uploader("เลือกไฟล์ Excel/CSV", accept_multiple_files=True)

# ส่วนประมวลผลข้อมูล
all_data = []

# ดึงข้อมูลจาก Google Sheets (ถ้ามีลิงก์)
if gsheet_url:
    try:
        sheet_id = gsheet_url.split("/d/")[1].split("/")[0]
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df_gs = pd.read_csv(url)
        # Clean Unnamed columns
        df_gs = df_gs.loc[:, ~df_gs.columns.str.contains('^Unnamed')]
        all_data.append(df_gs)
        st.sidebar.success("✅ เชื่อมต่อ Sheets สำเร็จ")
    except:
        st.sidebar.error("❌ ลิงก์ Sheets ไม่ถูกต้อง")

# ดึงข้อมูลจากไฟล์ที่อัปโหลด (ถ้ามี)
if uploaded_files:
    for f in uploaded_files:
        df = pd.read_excel(f) if f.name.endswith('.xlsx') else pd.read_csv(f)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        all_data.append(df)

# --- 5. แสดงผล Dashboard ---
if all_data:
    df_final = pd.concat(all_data, ignore_index=True).dropna(how='all')
    
    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("📝 รายการทั้งหมด", f"{len(df_final):,}")
    nums = df_final.select_dtypes(include=['number']).columns
    if len(nums) > 0:
        c2.metric(f"💰 ยอดรวม ({nums[0]})", f"{df_final[nums[0]].sum():,.0f}")
        c3.metric(f"📈 ค่าเฉลี่ย ({nums[0]})", f"{df_final[nums[0]].mean():,.2f}")

    # Tabs
    t1, t2 = st.tabs(["📉 วิเคราะห์กราฟ", "📋 ตารางข้อมูล"])
    with t1:
        x_axis = st.selectbox("แกน X", df_final.columns)
        y_axis = st.selectbox("แกน Y", nums if len(nums)>0 else df_final.columns)
        fig = px.bar(df_final, x=x_axis, y=y_axis, color=x_axis, title="ผลการวิเคราะห์")
        st.plotly_chart(fig, use_container_width=True)
    with t2:
        st.dataframe(df_final, use_container_width=True)
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("💾 ดาวน์โหลดไฟล์รวม (CSV)", data=csv, file_name='data_cleaned.csv')
else:
    st.info("💡 กรุณาใส่ลิงก์ Google Sheets หรืออัปโหลดไฟล์ที่แถบด้านข้างเพื่อเริ่มงาน")
