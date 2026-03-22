import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. UI Configuration ---
st.set_page_config(page_title="DataMaster Pro", page_icon="💎", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Kanit', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    [data-testid="stSidebar"] { background-color: #0f172a; color: white; }
    div[data-testid="metric-container"] {
        background: white; padding: 25px; border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Login System ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with col2 := c2:
        st.markdown("<div style='text-align: center; padding: 50px; background: white; border-radius: 30px;'>", unsafe_allow_html=True)
        st.header("💎 เข้าสู่ระบบ")
        pw = st.text_input("รหัสผ่าน", type="password")
        if st.button("ตกลง"):
            if pw == "admin123": # <--- แก้รหัสผ่านที่นี่
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("รหัสผ่านผิด")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 3. Main Application ---
st.title("💎 DataMaster Intelligence")
st.sidebar.markdown("### 🛠️ จัดการข้อมูล")
gsheet_url = st.sidebar.text_input("🔗 ลิงก์ Google Sheets:")
files = st.sidebar.file_uploader("📤 อัปโหลดไฟล์", accept_multiple_files=True)

all_data = []

# ดึงข้อมูล Google Sheets
if gsheet_url:
    try:
        s_id = gsheet_url.split("/d/")[1].split("/")[0]
        u = f"https://docs.google.com/spreadsheets/d/{s_id}/export?format=csv"
        df_g = pd.read_csv(u)
        all_data.append(df_g)
    except:
        st.sidebar.error("ลิงก์ Sheets ผิด")

# ดึงข้อมูลไฟล์อัปโหลด
if files:
    for f in files:
        df = pd.read_excel(f) if f.name.endswith('.xlsx') else pd.read_csv(f)
        all_data.append(df)

if all_data:
    df_final = pd.concat(all_data, ignore_index=True)
    # Clean คอลัมน์ Unnamed
    df_final = df_final.loc[:, ~df_final.columns.str.contains('^Unnamed')]
    
    # Dashboard
    m1, m2, m3 = st.columns(3)
    m1.metric("📦 ทั้งหมด", f"{len(df_final):,}")
    nums = df_final.select_dtypes(include=['number']).columns
    if len(nums) > 0:
        m2.metric(f"💰 ยอดรวม ({nums[0]})", f"{df_final[nums[0]].sum():,.0f}")
        m3.metric("📈 ค่าเฉลี่ย", f"{df_final[nums[0]].mean():,.2f}")

    t1, t2 = st.tabs(["✨ กราฟวิเคราะห์", "🔍 ตารางข้อมูล"])
    with t1:
        x = st.selectbox("แกน X", df_final.columns)
        y = st.selectbox("แกน Y", nums if len(nums)>0 else df_final.columns)
        st.plotly_chart(px.bar(df_final, x=x, y=y, color=x, template="plotly_white"), use_container_width=True)
    with t2:
        st.dataframe(df_final, use_container_width=True)
        st.download_button("📥 โหลด CSV", data=df_final.to_csv(index=False).encode('utf-8'), file_name='data.csv')
else:
    st.info("👈 กรุณาเพิ่มข้อมูลที่เมนูด้านซ้าย")
