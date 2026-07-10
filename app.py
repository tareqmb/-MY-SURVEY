import streamlit as st
import requests
import json
import uuid
import time
from extra_streamlit_components import CookieManager

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. إعداد مدير الكوكيز والذاكرة المؤقتة
cookie_manager = CookieManager()

if "my_id" not in st.session_state:
    st.session_state.my_id = None
if "form_sent" not in st.session_state:
    st.session_state.form_sent = False

# اسم الكوكيز
USER_COOKIE = "survey_uid_v12"
DONE_COOKIE = "survey_done_v12"

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 2. جلب المعرف (من الكوكيز أو إنشاء واحد جديد)
cached_uid = cookie_manager.get(USER_COOKIE)
if cached_uid:
    st.session_state.my_id = cached_uid
elif not st.session_state.my_id:
    st.session_state.my_id = str(uuid.uuid4())[:8]
    cookie_manager.set(USER_COOKIE, st.session_state.my_id, key="save_uid")

# 3. فحص إذا كان الزميل أرسل مسبقاً (من الكوكيز أو الجلسة الحالية)
already_done = cookie_manager.get(DONE_COOKIE)

if already_done == "true" or st.session_state.form_sent:
    st.success(f"✅ تم استلام تقييمك بنجاح! شكراً لك.")
    st.info(f"المعرف الخاص بك للتدقيق: {st.session_state.my_id}")
    st.balloons()
    st.stop() # يوقف كل شيء ويخلي الرسالة ثابتة

# --- واجهة الاستبيان ---
st.info("عزيزي الزميل/ة، هذا الاستبيان سري تماماً. المعرف يُستخدم فقط لمنع تكرار البيانات.")

script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم الآن")

if submit_button:
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes,
        "user_id": st.session_state.my_id
    }
    
    try:
        response = requests.post(script_url, data=json.dumps(payload), timeout=15)
        if response.status_code == 200:
            # زرع الكوكي وتحديث حالة الجلسة
            cookie_manager.set(DONE_COOKIE, "true", key="save_done")
            st.session_state.form_sent = True
            st.rerun() # يعيد التشغيل ليظهر رسالة النجاح الثابتة في الأعلى
        else:
            st.error("فشل الإرسال للسيرفر، يرجى المحاولة مرة أخرى.")
    except:
        st.error("حدث خطأ تقني، يرجى التأكد من الإنترنت.")
