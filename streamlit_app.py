import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. การตั้งค่าหน้าเว็บและสไตล์ (Theme & CSS) ---
st.set_page_config(
    page_title="DataMaster Admin",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS เพื่อคุมโทน Admin Dashboard
st.markdown("""
    <style>
    /* ปรับพื้นหลังหลัก */
    .stApp {
        background-color: #f4f7f6;
    }
    /* ปรับสไตล์ Sidebar (แถบข้าง) ให้เข้ม */
    [data-testid="stSidebar"] {
        background-color: #1a2a3a;
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white;
    }
    /* ปรับสไตล์ Metrics (การ์ดสรุปตัวเลข) */
    div[data-testid="metric-container"] {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #eef2f1;
    }
    div[data-testid="metric-container"] label {
        color: #5f6c7b;
        font-weight: bold;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #1a2a3a;
        font-size: 2rem;
    }
    /* ปรับสไตล์ Tab */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        color: #5f6c7b;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }
    </style>
    """, unsafe_allow_status=True)

# --- 2. ส่วนหัวแอป (Header Section) ---
with st.container():
    st.markdown("<h1 style='color: #1a2a3a;'>📊 DataMaster Admin Panel</h1>", unsafe_allow_status=True)
    st.markdown("<p style='color: #5f6c7b; font-size: 1.1rem;'>รวมข้อมูลและวิเคราะห์ผลแบบ Real-time</p>", unsafe_allow_status=True)
    st.markdown("---")

# --- 3. แถบเมนูด้านข้าง (Sidebar) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/732/732220.png", width=60) # Excel Icon
st.sidebar.title("Data Integration")
st.sidebar.markdown("---")

uploaded_files = st.sidebar.file_uploader(
    "📤 อัปโหลดไฟล์ (Excel/CSV)", 
    accept_multiple_files=True, 
    help="ลากไฟล์หลายๆ ไฟล์มาวางพร้อมกันได้เลย"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 ทริค: รวมไฟล์เสร็จแล้ว อย่าลืมกดดาวน์โหลดที่แท็บ '📥 ส่งออกข้อมูล'")

if uploaded_files:
    with st.spinner('⌛ กำลังประมวลผลข้อมูล...'):
        all_data = []
        for file in uploaded_files:
            try:
                if file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    df = pd.read_csv(file)
                # เพิ่ม Column บอกชื่อไฟล์ต้นทาง (Optional, useful)
                df['Source_File'] = file.name 
                all_data.append(df)
            except Exception as e:
                st.error(f"❌ ไม่สามารถอ่านไฟล์ {file.name} ได้: {e}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # --- 4. พื้นที่แสดงผลหลัก (Main Dashboard Context) ---
            
            # 4.1 การ์ดสรุปตัวเลขสำคัญ (KPI Cards)
            st.markdown("<h3 style='color: #1a2a3a; margin-bottom: 20px;'>📉 สรุปข้อมูลภาพรวม</h3>", unsafe_allow_status=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("📂 ไฟล์ที่โหลด", f"{len(uploaded_files)} ไฟล์")
            m2.metric("📝 รายการทั้งหมด", f"{len(combined_df):,}")
            
            # หาคอลัมน์ตัวเลขเพื่อทำ KPI ต่อ
            num_cols = combined_df.select_dtypes(include=['number']).columns
            if len(num_cols) > 0:
                # สมมติใช้คอลัมน์ตัวเลขแรกเป็นยอดหลัก (คุณปรับเปลี่ยนชื่อคอลัมน์ได้)
                main_num_col = num_cols[0]
                m3.metric(f"💰 ยอดรวม ({main_num_col})", f"{combined_df[main_num_col].sum():,.0f}")
                m4.metric(f"📊 ค่าเฉลี่ย ({main_num_col})", f"{combined_df[main_num_col].mean():,.0f}")
            else:
                m3.metric("💰 ยอดรวมหลัก", "N/A")
                m4.metric("📊 ค่าเฉลี่ย", "N/A")

            st.markdown("###") # เว้นระยะห่าง

            # 4.2 แท็บแสดงตารางและกราฟ (Tabs)
            t1, t2 = st.tabs(["📉 กราฟวิเคราะห์ผล", "📋 ตารางข้อมูล & ส่งออก"])

            with t1:
                st.markdown("<h3 style='color: #1a2a3a;'>📈 Visual Analytics</h3>", unsafe_allow_status=True)
                c1, c2 = st.columns([1, 1])
                
                # กราฟแท่งแบบสมัยใหม่
                with c1:
                    target_x = st.selectbox("เลือกข้อมูลแกน X:", combined_df.columns, key="x_axis")
                    # ใช้ Column ตัวเลขเป็นแกน Y
                    target_y = st.selectbox("เลือกข้อมูลแกน Y (ตัวเลข):", num_cols if len(num_cols)>0 else combined_df.columns, key="y_axis")
                    
                    fig_bar = px.bar(
                        combined_df, 
                        x=target_x, 
                        y=target_y, 
                        color=target_x, 
                        title=f"เปรียบเทียบ {target_y} ตาม {target_x}",
                        color_discrete_sequence=px.colors.qualitative.Safe # สีโทนสะอาด
                    )
                    fig_bar.update_layout(plot_bgcolor='white', paper_bgcolor='white') # พื้นหลังกราฟขาว
                    st.plotly_chart(fig_bar, use_container_width=True)

                # กราฟวงกลม
                with c2:
                    fig_pie = px.pie(
                        combined_df, 
                        names=target_x, 
                        title=f"สัดส่วนของ {target_x}",
                        color_discrete_sequence=px.colors.qualitative.Safe
                    )
                    fig_pie.update_layout(paper_bgcolor='white')
                    st.plotly_chart(fig_pie, use_container_width=True)

            with t2:
                st.markdown("<h3 style='color: #1a2a3a;'>🔍 Data Explorer</h3>", unsafe_allow_status=True)
                # ตัวกรองข้อมูลแบบง่ายๆ ในหน้าตาราง
                search_term = st.text_input("🔍 ค้นหาข้อมูลในตาราง:", "")
                if search_term:
                    # ค้นหาแบบง่ายๆ ในทุก Column (อาจจะช้าถ้าข้อมูลเยอะมาก)
                    mask = combined_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
                    final_df = combined_df[mask]
                else:
                    final_df = combined_df

                st.dataframe(final_df, use_container_width=True, height=450)
                
                st.markdown("---")
                st.markdown("<h4 style='color: #1a2a3a;'>📥 ส่งออกข้อมูล (Export)</h4>", unsafe_allow_status=True)
                csv = final_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 ดาวน์โหลดข้อมูลที่รวมแล้วเป็นไฟล์ CSV",
                    data=csv,
                    file_name='combined_admin_data.csv',
                    mime='text/csv',
                    help="คลิกเพื่อบันทึกไฟล์ข้อมูลทั้งหมดลงคอมพิวเตอร์ของคุณ"
                )
        
            st.toast("✅ อัปเดตข้อมูลภาพรวมเรียบร้อยแล้ว!", icon='🎉')

else:
    # หน้าจอ Welcome เมื่อยังไม่ได้ลงไฟล์ (ปรับให้สวยงามขึ้น)
    st.markdown("""
        <div style="text-align: center; padding: 120px; background-color: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <h1 style="font-size: 80px; color: #3b82f6;">📤</h1>
            <h2 style="color: #1a2a3a;">ยินดีต้อนรับสู่ Admin Panel</h2>
            <p style="color: #5f6c7b; font-size: 1.2rem;">เริ่มต้นใช้งานโดยการ <span style="color: #3b82f6; font-weight: bold;">ลากไฟล์ Excel หรือ CSV</span> มาวางที่แถบเมนูด้านข้าง</p>
            <p style="color: #a0aec0; font-size: 0.9rem; margin-top: 20px;">ระบบจะทำการรวมข้อมูลและสร้าง Dashboard ให้คุณอัตโนมัติ</p>
        </div>
    """, unsafe_allow_status=True)
