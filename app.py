import streamlit as st
import requests
import json
from extra_streamlit_components import CookieManager

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي المهني", layout="centered")

# 1. تعريف مدير الكوكيز
cookie_manager = CookieManager()
COOKIE_NAME = "survey_strict_lock_v7" # اسم جديد لضمان تفعيل القفل المحدث

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 2. جلب البصمة من المتصفح
already_submitted = cookie_manager.get(COOKIE_NAME)

# 3. القفل الأول: إذا وجدنا البصمة، نوقف البرنامج فوراً ولا نظهر الاستبيان
if already_submitted == "true":
    st.success("✅ شكرًا لك! لقد تم استلام تقييمك مسبقًا.")
    st.info("لضمان دقة النتائج، يُسمح بإرسال الرد مرة واحدة فقط.")
    st.stop() 

# --- إذا وصل الكود هنا، يعني أن المستخدم لم يرسل بعد ---

st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أدائي. 
**الردود سرية تماماً** ولن يتم جمع أي بيانات شخصية.
<hr>
""", unsafe_allow_html=True)

script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

# 4. القفل الثاني: التحقق داخل منطق الإرسال
if submit_button:
    # نتحقق مرة أخيرة قبل الإرسال الفعلي
    check_again = cookie_manager.get(COOKIE_NAME)
    
    if check_again == "true":
        st.warning("لقد قمت بالإرسال للتو، لا يمكن التكرار.")
        st.stop()
    else:
        payload = {
            "work_style": str(work_style),
            "efficiency": str(efficiency),
            "interaction": str(interaction),
            "notes": notes
        }
        
        try:
            # إرسال البيانات
            response = requests.post(script_url, data=json.dumps(payload), timeout=10)
            
            if response.status_code == 200:
                # 5. زرع البصمة فوراً
                cookie_manager.set(COOKIE_NAME, "true")
                st.success("تم إرسال تقييمك بنجاح! شكراً لك.")
                st.balloons()
                # إعادة التشغيل لتفعيل القفل الأول وإخفاء النموذج
                st.rerun()
            else:
                st.error("فشل الإرسال، يرجى المحاولة لاحقاً.")
        except Exception as e:
            if "Rerun" in str(type(e)):
                raise e
            else:
                st.error("حدث خطأ تقني.")
