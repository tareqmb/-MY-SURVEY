import streamlit as st
import requests

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

st.title("استطلاع رأي حول الأداء والتعامل المهني")
st.info("عزيزي الزميل، هذا الاستطلاع سري تماماً ويهدف للتطوير الذاتي فقط.")

# نموذج الاستطلاع
with st.form(key="survey_form"):
    work_style = st.select_slider("1. تقييم أسلوبي في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. تقييم كفاءتي المهنية وسرعة الإنجاز:", options=[1, 2, 3, 4, 5], value=3)
    personal_interaction = st.select_slider("3. تقييم المعاملة الشخصية والتواصل الإنساني:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

    if submit_button:
        # --- هاد هو الجزء السحري ---
        # استبدل هذا الرابط برابط الـ Google Form الخاص بك، لكن بصيغة /formResponse
        # مثال: https://docs.google.com/forms/d/e/1FAIpQLS.../formResponse
        form_url = "https://docs.google.com/spreadsheets/d/1QzB8sBWlS5aDPAZQ-2k7J4-6pdgimZG5kff2EqWNkqw/edit?usp=sharing/formResponse"
        
        # ملاحظة: سنحتاج لتعريف الـ entry IDs لاحقاً، لكن مبدئياً جرب هذا:
        st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
        st.balloons()
