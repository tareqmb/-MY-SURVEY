import streamlit as st
import requests
import json
from extra_streamlit_components import CookieManager

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي المهني", layout="centered")

# تعريف مدير الكوكيز
cookie_manager = CookieManager()

# نستخدم اسم بصمة فريد لضمان عدم التداخل مع المحاولات السابقة
COOKIE_NAME = "survey_lock_final_v5"

st.title("استطلاع رأي حول الأداء والتعامل المهني")

# فحص البصمة في المتصفح
already_submitted = cookie_manager.get(COOKIE_NAME)

# استخدام session_state كدعم إضافي لمنع التكرار في نفس اللحظة
if "submitted_now" not in st.session_state:
    st.session_state.submitted_now = False

# منطق العرض: إذا أرسل سابقاً (عن طريق الكوكيز أو الجلسة الحالية)
if already_submitted == "true" or st.session_state.submitted_now:
    st.success("✅ شكرًا لك! لقد تم استلام تقييمك مسبقًا.")
    st.info("لضمان دقة النتائج، يُسمح بإرسال الرد مرة واحدة فقط لكل زميل.")
    st.balloons()
    st.stop() # توقف الكود هنا تماماً للمستخدمين الذين أرسلوا مسبقاً

# إذا لم يرسل مسبقاً، يظهر الاستبيان
st.markdown("""
عزيزي الزميل/ة، يهدف هذا الاستطلاع إلى قياس مدى رضاكم عن أسلوبي في العمل وكفاءتي المهنية. 
هذا الاستبيان **سري تماماً** ولا يتم فيه جمع أي بيانات شخصية أو بريد إلكتروني.
<hr>
""", unsafe_allow_html=True)

# الرابط الخاص بك من Google Apps Script (تأكد أنه ينتهي بـ /exec)
script_url = "ضع_رابط_الويب_أب_هنا"

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
        # إرسال البيانات إلى جوجل شيت
        response = requests.post(script_url, data=json.dumps(payload), timeout=10)
        
        if response.status_code == 200:
            # 1. زرع البصمة في المتصفح للمرات القادمة
            cookie_manager.set(COOKIE_NAME, "true")
            
            # 2. تحديث حالة الجلسة الحالية للإخفاء الفوري
            st.session_state.submitted_now = True
            
            # 3. إظهار رسالة النجاح
            st.success("تم إرسال تقييمك بنجاح! شكراً لصراحتك ووقتك.")
            st.balloons()
            
            # 4. إعادة تشغيل بسيطة لتنظيف الشاشة وإظهار رسالة المنع
            st.rerun()
        else:
            st.error("فشل الإرسال، يرجى التأكد من رابط جوجل شيت وصلاحيات الوصول.")
            
    except Exception as e:
        # التعامل مع استثناء إعادة التشغيل الخاص بـ Streamlit
        if "Rerun" in str(type(e)):
            raise e
        else:
            st.error("حدث خطأ تقني، يرجى المحاولة مرة أخرى.")
