import streamlit as st
import requests
import json
import uuid # مكتبة لتوليد معرف فريد
from extra_streamlit_components import CookieManager

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي المهني", layout="centered")

# تعريف مدير الكوكيز
cookie_manager = CookieManager()
COOKIE_NAME = "survey_lock_v5"
USER_ID_COOKIE = "user_unique_id" # كوكيز لحفظ معرف المستخدم

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 1. جلب أو إنشاء معرف فريد للمستخدم (بصمة المتصفح)
user_id = cookie_manager.get(USER_ID_COOKIE)
if not user_id:
    user_id = str(uuid.uuid4())[:8] # توليد كود من 8 أرقام وحروف
    cookie_manager.set(USER_ID_COOKIE, user_id)

# فحص البصمة لمنع التكرار في الواجهة
already_submitted = cookie_manager.get(COOKIE_NAME)

if "submitted_now" not in st.session_state:
    st.session_state.submitted_now = False

if already_submitted == "true" or st.session_state.submitted_now:
    st.success("✅ شكرًا لك! لقد تم استلام تقييمك مسبقًا.")
    st.info(f"معرفك الخاص للتدقيق: {user_id}") # يظهر للمستخدم كود لا يكشف هويته
    st.stop()

st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى التطوير الذاتي. 
هذا الاستبيان **سري تماماً**؛ المعرف الظاهري يُستخدم فقط لمنع تكرار البيانات.
<hr>
""", unsafe_allow_html=True)

script_url = "https://script.google.com/macros/s/AKfycbw0MVjJ6x0sFzFWQri9Eo5e63-UyXCNRGVSd9CHkr4Z-4oft7Ws6ibtXaZ5WvLyJESI/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

if submit_button:
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes,
        "user_id": user_id # إرسال المعرف الفريد مع البيانات
    }
    
    try:
        response = requests.post(script_url, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            cookie_manager.set(COOKIE_NAME, "true")
            st.session_state.submitted_now = True
            st.success(f"تم الإرسال بنجاح! معرفك للتدقيق هو: {user_id}")
            st.balloons()
            st.rerun()
        else:
            st.error("فشل الإرسال، حاول لاحقاً.")
    except Exception as e:
        if "Rerun" in str(type(e)):
            raise e
        else:
            st.error("حدث خطأ تقني.")
