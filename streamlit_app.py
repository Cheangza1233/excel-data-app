import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บแบบง่าย
st.set_page_config(page_icon="📊", page_title="Excel Master")
st.title("🚀 Excel Data Merger")
st.write("อัปโหลดไฟล์ Excel หรือ CSV หลายๆ ไฟล์เพื่อรวมข้อมูล")

# 2. ส่วนอัปโหลด
files = st.sidebar.file_uploader("เลือกไฟล์ที่นี่", accept_multiple_files=True)

if files:
    all_df = []
    for f in files:
        # อ่านไฟล์ตามนามสกุล
        df = pd.read_excel(f) if f.name.endswith('.xlsx') else pd.read_csv(f)
        all_df.append(df)
    
    # รวมไฟล์
    final_df = pd.concat(all_df, ignore_index=True)
    
    # แสดงผล
    st.success(f"✅ รวมไฟล์สำเร็จ! ทั้งหมด {len(final_df)} รายการ")
    
    st.subheader("📋 พรีวิวข้อมูล")
    st.dataframe(final_df)
    
    # ปุ่มดาวน์โหลด
    csv = final_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 ดาวน์โหลดไฟล์รวม (CSV)", data=csv, file_name="combined.csv")
else:
    st.info("👈 กรุณาเลือกอัปโหลดไฟล์ที่แถบด้านข้าง")
