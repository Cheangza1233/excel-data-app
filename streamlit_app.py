import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Excel Pro", layout="wide")

st.title("📊 Smart Data Master")
st.write("รวมไฟล์ Excel/CSV และสร้าง Dashboard อัตโนมัติ")
st.markdown("---")

# ส่วนอัปโหลดไฟล์ที่แถบด้านข้าง
uploaded_files = st.sidebar.file_uploader("อัปโหลดไฟล์ที่นี่ (เลือกได้หลายไฟล์)", accept_multiple_files=True)

if uploaded_files:
    all_data = []
    for f in uploaded_files:
        # เช็คว่าเป็น Excel หรือ CSV
        df = pd.read_excel(f) if f.name.endswith('.xlsx') else pd.read_csv(f)
        all_data.append(df)
    
    # รวมไฟล์เป็นหนึ่งเดียว
    df_final = pd.concat(all_data, ignore_index=True)
    
    # แสดงตัวเลขสรุป
    st.metric("จำนวนรายการทั้งหมดที่รวมได้", f"{len(df_final):,} แถว")
    
    # แท็บแสดงข้อมูลและกราฟ
    tab1, tab2 = st.tabs(["📋 ตารางข้อมูล", "📈 กราฟวิเคราะห์"])
    
    with tab1:
        st.dataframe(df_final, use_container_width=True)
        # ปุ่มดาวน์โหลด
        csv = df_final.to_csv(index=False).encode('utf-8')
        st.download_button("💾 ดาวน์โหลดไฟล์ที่รวมแล้ว (CSV)", data=csv, file_name='combined_data.csv')
    
    with tab2:
        col_x = st.selectbox("เลือกข้อมูลแกน X เพื่อดูกราฟ", df_final.columns)
        fig = px.histogram(df_final, x=col_x, title=f"วิเคราะห์ข้อมูล: {col_x}")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 เริ่มต้นโดยการอัปโหลดไฟล์ที่แถบด้านข้างได้เลยครับ")
