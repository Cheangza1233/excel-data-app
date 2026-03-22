import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. UI Configuration ---
st.set_page_config(
    page_title="DataMaster Admin",
    page_icon="📊",
    layout="wide",
)

# Custom CSS สำหรับ Admin Style
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

# --- 2. Header ---
st.title("📊 DataMaster Admin Panel")
st.write("ระบบรวมข้อมูลและวิเคราะห์ผลอัตโนมัติ")
st.markdown("---")

# --- 3. Sidebar ---
st.sidebar.title("เมนูควบคุม")
files = st.sidebar.file_uploader("📤 อัปโหลดไฟล์ Excel/CSV", accept_multiple_files=True)

if files:
    all_data = []
    for f in files:
        try:
            df = pd.read_excel(f) if f.name.endswith('.xlsx') else pd.read_csv(f)
            all_data.append(df)
        except Exception as e:
            st.sidebar.error(f"Error: {f.name}")
    
    if all_data:
        df_final = pd.concat(all_data, ignore_index=True)
        
        # 4. Metrics Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("📂 จำนวนไฟล์", f"{len(files)}")
        col2.metric("📝 รายการทั้งหมด", f"{len(df_final):,}")
        
        nums = df_final.select_dtypes(include=['number']).columns
        if len(nums) > 0:
            col3.metric(f"💰 ยอดรวม ({nums[0]})", f"{df_final[nums[0]].sum():,.0f}")

        # 5. Tabs
        t1, t2 = st.tabs(["📉 กราฟวิเคราะห์", "📋 ตารางข้อมูล"])
        
        with t1:
            c1, c2 = st.columns(2)
            with c1:
                x_axis = st.selectbox("เลือกแกน X", df_final.columns)
                y_axis = st.selectbox("เลือกแกน Y", nums if len(nums)>0 else df_final.columns)
                fig_bar = px.bar(df_final, x=x_axis, y=y_axis, color=x_axis, title="เปรียบเทียบข้อมูล")
                st.plotly_chart(fig_bar, use_container_width=True)
            with c2:
                fig_pie = px.pie(df_final, names=x_axis, title="สัดส่วนข้อมูล")
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with t2:
            st.dataframe(df_final, use_container_width=True)
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button("💾 ดาวน์โหลดไฟล์รวม (CSV)", data=csv, file_name='data_export.csv')
else:
    st.info("👈 เริ่มต้นโดยการอัปโหลดไฟล์ที่แถบด้านข้าง")
