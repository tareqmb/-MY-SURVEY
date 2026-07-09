import streamlit as st
import requests
import json

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي المهني", layout="centered")

# 1. نظام القفل: منع الإرسال المتكرر خلال الجلسة
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# 2. إذا تم الإرسال بنجاح، اظهر رسالة الشكر وأوقف كل شيء
if st.session_state.form_submitted:
    st.success("✅ تم إرسال تقييمك بنجاح! شكراً لك على وقتك وصراحتك.")
    st.balloons()
    st.info("ملاحظة: لضمان دقة النتائج، تم إغلاق نموذج الإرسال لهذا الجهاز.")
    st.stop() # هذا الأمر يمنع الكود من قراءة أي شيء آخر

# --- بداية الاستبيان ---
st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أدائي المهني.
**أؤكد لكم أن هذا الاستبيان سري تماماً ولا يتم فيه جمع أي بيانات شخصية.**
<hr>
""", unsafe_allow_html=True)

# الرابط الخاص بك من Google Apps Script (تأكد من أنه ينتهي بـ /exec)
script_url = "https://script.google.com/macros/s/AKfycbyfV8qjxaEKSwbOc4xfEPoBYCWaq5wwQB2MgbyZjq3fq7ptzqAdTxtX1JVE62J0g9WS/exec"

# إنشاء النموذج
with st.form(key="survey_form", clear_on_submit=True):
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")
    
    # زر الإرسال
    submit_button = st.form_submit_button(label="إرسال التقييم الفوري")

# 3. معالجة الإرسال عند الضغط على الزر
if submit_button:
    # القفل الفوري: نغير الحالة قبل أي عملية إرسال
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "notes": notes
    }
    
    try:
        # إرسال البيانات إلى جوجل شيت مرة واحدة فقط
        response = requests.post(script_url, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            # تفعيل قفل الجلسة لمنع التكرار
            st.session_state.form_submitted = True
            # إعادة تشغيل الصفحة فوراً لإظهار رسالة النجاح وإخفاء النموذج
            st.rerun()
        else:
            st.error("فشل في الوصول إلى السيرفر، يرجى المحاولة لاحقاً.")
            
    except Exception as e:
        st.error("حدث خطأ تقني، يرجى التأكد من اتصال الإنترنت.")
