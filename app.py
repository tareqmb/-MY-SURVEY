import streamlit as st
import requests
import json
from extra_streamlit_components import CookieManager

st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# إعداد مدير الكوكيز
cookie_manager = CookieManager()

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# فحص إذا كان الشخص قد أرسل سابقاً (من خلال الكوكيز)
has_submitted_cookie = cookie_manager.get("has_submitted_survey")

if has_submitted_cookie == "true":
    st.success("✅ شكرًا لك! لقد قمت بإرسال تقييمك مسبقاً.")
    st.info("لضمان دقة الاستطلاع، يُسمح لكل زميل بإرسال الرد مرة واحدة فقط.")
    st.balloons()
else:
    st.info("عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي. الردود سرية تماماً.")

    # رابط الويب أب الخاص بك
    script_url = "رابط_الويب_أب_الخاص_بك_هنا"

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
                # إرسال البيانات لجوجل شيت
                requests.post(script_url, data=json.dumps(payload))
                
                # وضع "كوكي" في متصفح المستخدم تنتهي بعد 30 يوم
                cookie_manager.set("has_submitted_survey", "true", key="set_cookie")
                
                st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
                st.rerun() # إعادة تحميل الصفحة لتفعيل المنع
                
            except:
                st.error("حدث خطأ في الإرسال، يرجى المحاولة لاحقاً.")
