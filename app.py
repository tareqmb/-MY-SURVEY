import streamlit as st
import requests
import json

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

st.title("استطلاع رأي حول الأداء والتعامل المهني")
st.info("عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي. الردود سرية تماماً.")

# حط الرابط اللي نسخته من الخطوة السابقة بين القوسين
script_url = "https://script.google.com/macros/s/AKfycbxyZ8XOHpv0k6ohmdLNmwDQVfBkbNwxsG73khEAUWTZjxsLhtu_ycUnIfw9pcnUdsba/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. تقييم أسلوبي في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. تقييم كفاءتي المهنية وسرعة الإنجاز:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. تقييم المعاملة الشخصية والتواصل الإنساني:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

    if submit_button:
        # تجهيز البيانات
        payload = {
            "work_style": work_style,
            "efficiency": efficiency,
            "interaction": interaction,
            "notes": notes
        }
        # إرسال البيانات للجسر
        try:
            response = requests.post(script_url, data=json.dumps(payload))
            if response.status_code == 200:
                st.success("شكراً لك! تم استلام تقييمك بنجاح وبكل سرية.")
                st.balloons()
            else:
                st.error("عذراً، حدث خطأ أثناء الإرسال.")
        except:
            st.error("فشل الاتصال بالسيرفر.")
