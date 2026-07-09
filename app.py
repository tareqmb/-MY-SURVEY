import streamlit as st
import requests
import json

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

st.title("استطلاع رأي حول الأداء والتعامل المهني")
st.info("عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي. الردود سرية تماماً.")

# تأكد أن الرابط ينتهي بـ /exec
script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. تقييم أسلوبي في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. تقييم كفاءتي المهنية وسرعة الإنجاز:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. تقييم المعاملة الشخصية والتواصل الإنساني:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

    if submit_button:
        payload = {
            "work_style": str(work_style),
            "efficiency": str(efficiency),
            "interaction": str(interaction),
            "notes": notes
        }
        try:
            # أرسلنا البيانات وبدنا أي رد "ناجح"
            response = requests.post(script_url, data=json.dumps(payload))
            st.success("تم إرسال تقييمك بنجاح! شكراً لصراحتك.")
            st.balloons()
        except:
            st.error("عذراً، تأكد من اتصال الإنترنت أو إعدادات الرابط.")
