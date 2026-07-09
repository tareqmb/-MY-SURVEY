
import streamlit as st
import requests
import json
from extra_streamlit_components import CookieManager

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. إعداد مدير الكوكيز
cookie_manager = CookieManager()

# خطوة ضرورية لضمان تحميل الكوكيز
st.write("") 

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 2. فحص إذا كان الشخص قد أرسل سابقاً
# ملاحظة: الكوكيز قد تستغرق ثانية للتحميل
has_submitted = cookie_manager.get("submitted_survey_v1")

if has_submitted == "true":
    st.success("✅ شكرًا لك! لقد قمت بإرسال تقييمك مسبقاً.")
    st.info("لضمان دقة الاستطلاع، يُسمح بإرسال الرد مرة واحدة فقط.")
    st.balloons()
else:
    st.info("عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي. الردود سرية تماماً.")

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
        
        # تنفيذ الإرسال خارج الـ Form لضمان الاستقرار
        success_flag = False
        try:
            response = requests.post(script_url, data=json.dumps(payload))
            if response.status_code == 200:
                success_flag = True
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")

        if success_flag:
            # 3. حفظ الكوكي في المتصفح
            cookie_manager.set("submitted_survey_v1", "true", key="unique_set_cookie")
            st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
            st.balloons()
            # التوقف قليلاً ثم إعادة التشغيل لتثبيت الحالة
            st.info("سيتم تحديث الصفحة خلال لحظات...")
            st.rerun()
