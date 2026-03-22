import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. UI Configuration (หน้าตาแอป) ---
st.set_page_config(page_title="DataMaster Pro", page_icon="💎", layout="wide")

# --- 2. Custom CSS (หัวใจของความสวยงาม) ---
st.markdown("""
    <style>
    /* ปรับแต่งฟอนต์และพื้นหลังหลัก */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Kanit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* ปรับแต่ง Sidebar ให้ดูหรูหรา */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* สไตล์การ์ดตัวเลข (Metrics) */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }

    /* ปรับแต่งปุ่มและ Input */
    .stButton>button {
        background: linear-gradient(45deg, #3b82f6, #2563eb);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 25px;
        font-weight: 500;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        transform: scale(1.02);
    }

    /* ปรับแต่ง Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: white;
        border-radius: 12px;
        padding: 0 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ระบบความปลอดภัย (Login System) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "admin123": # <--- แก้รหัสผ่านที่นี่
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<div style='text-align: center; padding: 50px; background: white; border-radius: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
            st.image("https://cdn-icons-png.flaticon.com/512/6195/6195700.png", width=100)
            st.header("ยินดีต้อนรับกลับมา")
            st.text_input("กรุณาใส่รหัสผ่าน", type="password", on_change=password_entered, key="password")
            st.markdown("</div>", unsafe_allow_html=True)
        return False
    elif not st.session_state["password_correct"]:
        st.error("❌ รหัสผ่านไม่ถูกต้อง")
        return False
    return True

if not check_password():
    st.stop()

# --- 4. Main Application (เมื่อ Login ผ่านแล้ว) ---

# ส่วนหัว (Header)
c_head1, c_head2 = st.columns([4, 1])
with c_head1:
    st.title("💎 DataMaster Intelligence")
    st.markdown("<p style='font-size: 1.2rem; color: #64748b;'>ระบบจัดการและวิเคราะห์ข้อมูลอัจฉริยะ</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 🛠️ เครื่องมือจัดการ")
gsheet_url = st.sidebar.text_input("🔗 เชื่อม Google Sheets:")
uploaded_files = st.sidebar.file_uploader("📤 อัปโหลดไฟล์โดยตรง", accept_multiple_files=True)

all_data = []

# ดึงข้อมูล (Logic เดิมที่ทำงานได้ดีอยู่แล้ว)
if gsheet_url:
    try:
        sheet_id = gsheet_url.split("/d/")[1].split("/")[0]
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df_gs = pd.read_csv(url)
        df_gs = df_gs.loc[:, ~df_gs.columns.str.contains
