import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. การตั้งค่าหน้าตาเว็บ (UI Configuration) ---
st.set_page_config(
    page_title="Excel Pro Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS เพื่อปรับแต่ง UI ให้ดูทันสมัย
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stExpander"] {
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        background-color: white;
    }
    </style>
    """, unsafe_allow_status=True)

# --- 2. ส่วนหัวแอป (Header Section) ---
with st.container():
    st.title("📊 Smart Data Master")
    st.subheader("เปลี่ยนข้อมูลรกๆ ให้เป็น Dashboard ในคลิกเดียว")
    st.markdown("---")

# --- 3. ส่วนการทำงานหลัก (Sidebar & Upload) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/732/732220.png", width=50) # Icon Excel
st.sidebar.header("⚙️ เมนูควบคุม")

uploaded_files = st.sidebar.file_uploader(
    "อัปโหลดไฟล์ (Excel/CSV/TXT)", 
    accept_multiple_files=True, 
    help="คุณสามารถลากไฟล์หลายๆ ไฟล์มาวางพร้อมกันได้เลย"
)

if uploaded_files:
    with st.spinner('กำลังประมวลผลข้อมูล...'):
        all_data = []
        for file in uploaded_files:
            try:
                if file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    df = pd.read_csv(file)
                all_data.append(df)
            except Exception as e:
                st.error(f"ไม่สามารถอ่านไฟล์ {file.name} ได้: {e}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # ส่วนตัวกรองข้อมูล (Filters)
            st.sidebar.markdown("---")
            st.sidebar.subheader("🎯 กรองข้อมูล")
            filter_col = st.sidebar.selectbox("เลือกหัวข้อที่จะกรอง:", combined_df.columns)
            unique_vals = combined_df[filter_col].unique()
            selected_vals = st.sidebar.multiselect(f"ระบุ {filter_col}:", options=unique_vals, default=unique_vals)
            
            # กรองข้อมูล
            final_df = combined_df[combined_df[filter_col].isin(selected_vals)]

            # --- 4. ส่วนแสดงผล (Main Dashboard) ---
            
            # แสดงตัวเลขสำคัญ (KPI Metrics) แบบการ์ด
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("📂 จำนวนไฟล์", len(uploaded_files))
            m2.metric("📝 รายการทั้งหมด", f"{len(final_df):,}")
            
            num_cols = final_df.select_dtypes(include=['number']).columns
            if len(num_cols) > 0:
                m3.metric("💰 ยอดรวมหลัก", f"{final_df[num_cols[0]].sum():,.0f}")
                m4.metric("📈 ค่าเฉลี่ย", f"{final_df[num_cols[0]].mean():,.0f}")
            else:
                m3.metric("💰 ยอดรวมหลัก", "N/A")
                m4.metric("📈 ค่าเฉลี่ย", "N/A")

            st.markdown("###") # เว้นระยะห่าง

            # ส่วนกราฟและตาราง (Tabs)
            t1, t2, t3 = st.tabs(["📉 กราฟวิเคราะห์", "🔍 เจาะลึกตาราง", "📥 ดาวน์โหลด"])

            with t1:
                st.subheader("Visual Analysis")
                c1, c2 = st.columns([1, 1])
                
                with c1:
                    target_x = st.selectbox("เลือกแกน X:", combined_df.columns, key="x_axis")
                    target_y = st.selectbox("เลือกแกน Y (ตัวเลข):", num_cols if len(num_cols)>0 else combined_df.columns, key="y_axis")
                    fig_bar = px.bar(final_df, x=target_x, y=target_y, color=target_x, title=f"กราฟแท่งเปรียบเทียบ {target_y}")
                    st.plotly_chart(fig_bar, use_container_width=True)

                with c2:
                    fig_pie = px.pie(final_df, names=target_x, title=f"สัดส่วนของ {target_x}")
                    st.plotly_chart(fig_pie, use_container_width=True)

            with t2:
                st.subheader("Data Explorer")
                st.dataframe(final_df, use_container_width=True, height=400)

            with t3:
                st.subheader("Export Data")
                st.info("คุณสามารถบันทึกข้อมูลที่ผ่านการรวมและกรองเรียบร้อยแล้วไปใช้ต่อได้ที่นี่")
                csv = final_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 ดาวน์โหลดเป็นไฟล์ CSV",
                    data=csv,
                    file_name='clean_data_export.csv',
                    mime='text/csv',
                )
        
            st.toast("อัปเดตข้อมูลเรียบร้อยแล้ว!", icon='✅')

else:
    # หน้าจอ Welcome เมื่อยังไม่ได้ลงไฟล์
    st.empty()
    st.markdown("""
        <div style="text-align: center; padding: 100px;">
            <h1 style="font-size: 70px;">📤</h1>
            <h2>ยินดีต้อนรับสู่ Smart Data Master</h2>
            <p>กรุณาอัปโหลดไฟล์ที่แถบด้านข้างเพื่อเริ่มสร้าง Dashboard ของคุณ</p>
        </div>
    """, unsafe_allow_status=True)
