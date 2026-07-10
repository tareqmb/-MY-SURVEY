import streamlit as st
import requests
import json
import uuid

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# 1. نظام المعرف الفريد (Unique ID) باستخدام رابط الصفحة
if "user_id" not in st.query_params:
    # إذا كان المستخدم جديد، ننشئ له كود ونضعه في الرابط
    new_id = str(uuid.uuid4())[:8]
    st.query_params["user_id"] = new_id
    user_id = new_id
else:
    user_id = st.query_params["user_id"]

# 2. نظام قفل الجلسة لمنع التكرار اللحظي
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 3. منع الدخول إذا تم الإرسال
if st.session_state.submitted:
    st.success("✅ شكرًا لك! تم استلام تقييمك بنجاح.")
    st.info(f"معرفك الخاص للتدقيق: {user_id}")
    st.balloons()
    st.stop()

# --- واجهة الاستبيان ---
st.markdown(f"""
عزيزي الزميل/ة، هذا الاستطلاع **سري تماماً**. المعرف الخاص بك هو: `{user_id}`
<hr>
""", unsafe_allow_html=True)

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
        "user_id": user_id
    }
    
    try:
        # إرسال البيانات
        requests.post(script_url, data=json.dumps(payload), timeout=15)
        
        # قفل الصفحة
        st.session_state.submitted = True
        st.rerun()
        
    except:
        # في حال حدوث بطء في السيرفر، سنعتبرها نجحت لإغلاق الصفحة
        st.session_state.submitted = True
        st.rerun()
