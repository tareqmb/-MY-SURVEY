import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

st.title("استطلاع رأي حول الأداء والتعامل المهني")
st.markdown("""
### مادة توضيحية:
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أسلوبي في العمل وكفاءتي المهنية وطريقة تعاملي الشخصية.
**الخصوصية:** هذا الاستبيان **سري تماماً** ولا يجمع أي بيانات شخصية.
""")

# الرابط الخاص بك
url = "https://docs.google.com/spreadsheets/d/1d-mPd-GaLNnbHbs7En9OqmW9sIS5N1pIlN1yVHMSSoY/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form(key="survey_form"):
    work_style = st.select_slider("1. تقييم أسلوبي في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. تقييم كفاءتي المهنية وسرعة الإنجاز:", options=[1, 2, 3, 4, 5], value=3)
    personal_interaction = st.select_slider("3. تقييم المعاملة الشخصية والتواصل الإنساني:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

    if submit_button:
        new_data = pd.DataFrame([{
            "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Work_Style": work_style,
            "Efficiency": efficiency,
            "Personal_Interaction": personal_interaction,
            "Notes": notes
        }])
        # قراءة البيانات القديمة
        existing_data = conn.read(spreadsheet=url)
        # دمج البيانات
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        # تحديث جوجل شيت
        conn.update(spreadsheet=url, data=updated_df)
        st.success("شكراً لك! تم إرسال التقييم بنجاح.")
