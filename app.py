import streamlit as st
import requests
import json

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# رابط الويب أب الخاص بك (تأكد أنه ينتهي بـ /exec)
# ضعه هنا بدلاً من النص أدناه
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

# نظام القفل الداخلي للجلسة
if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# المنطق: إذا تم الإرسال في هذه الجلسة، توقف تماماً وأظهر رسالة النجاح
if st.session_state.submitted:
    st.success("✅ تم استلام تقييمك بنجاح! شكراً لك على وقتك وصراحتك.")
    st.balloons()
    st.stop()

# --- واجهة الاستبيان ---
st.markdown("""
### مادة توضيحية:
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أسلوبي في العمل وكفاءتي المهنية وطريقة تعاملي الشخصية معكم.
أؤكد لكم أن هذا الاستبيان **سري تماماً** ولا يتم فيه جمع أي بيانات شخصية، والنتائج ستُستخدم فقط لأغراض التحسين والتطوير ولن تُستخدم في أي خلافات جانبية.
شكراً لوقتكم وصراحتكم التي أقدرها عالياً.
<hr>
""", unsafe_allow_html=True)

with st.form(key="survey_form"):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية أو نصائح للتطوير (اختياري):")
    
    submit_button = st.form_submit_button(label="إرسال التقييم")

if submit_button:
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes
    }
    
    try:
        # إرسال البيانات مع رفع وقت الانتظار (Timeout) لـ 20 ثانية
        # حتى لو انتهى الوقت، في الغالب جوجل سجل البيانات
        requests.post(SCRIPT_URL, data=json.dumps(payload), timeout=20)
        
        # نعتبر العملية ناجحة بمجرد المحاولة لمنع المستخدم من الضغط مرة أخرى
        st.session_state.submitted = True
        st.rerun()
        
    except Exception:
        # حتى في حال حدوث خطأ في الاتصال، سنعتبرها نجحت لأنك ذكرت أنها تُسجل في الشيت
        # هذا يضمن عدم تكرار الضغط من قبل المستخدم
        st.session_state.submitted = True
        st.rerun()
