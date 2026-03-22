import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Excel Master Web App", layout="wide")

st.title("🚀 Web App รวมไฟล์ & Dashboard อัตโนมัติ")
st.write("โยนไฟล์ Excel/CSV หลายๆ ไฟล์ลงที่นี่ เพื่อรวมข้อมูลและดูรีพอร์ตทันที")

# 1. อัปโหลดไฟล์ (รองรับหลายไฟล์)
uploaded_files = st.file_uploader("เลือกไฟล์ที่ต้องการรวม", accept_multiple_files=True, type=['xlsx', 'csv', 'txt'])

if uploaded_files:
    all_data = []
    for file in uploaded_files:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
        all_data.append(df)
    
    # 2. รวมข้อมูล (เหมือน Power Query Append)
    combined_df = pd.concat(all_data, ignore_index=True)
    
    st.success(f"✅ รวมไฟล์สำเร็จ! พบข้อมูลทั้งหมด {len(combined_df)} แถว")

    # 3. ส่วน Dashboard แบบง่าย
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 พรีวิวข้อมูลที่รวมแล้ว")
        st.dataframe(combined_df.head(10))
    
    with col2:
        st.subheader("📈 วิเคราะห์เบื้องต้น")
        # ตัวอย่างกราฟ (ปรับเปลี่ยนตามชื่อ Column ของคุณได้)
        column_to_plot = st.selectbox("เลือก Column ที่ต้องการดูกราฟ", combined_df.columns)
        fig = px.histogram(combined_df, x=column_to_plot)
        st.plotly_chart(fig)

    # 4. ปุ่มดาวน์โหลดไฟล์ที่รวมเสร็จแล้ว
    st.download_button(
        label="📥 ดาวน์โหลดไฟล์ที่รวมแล้ว (Excel)",
        data=combined_df.to_csv(index=False).encode('utf-8'),
        file_name='combined_data.csv',
        mime='text/csv',
    )
