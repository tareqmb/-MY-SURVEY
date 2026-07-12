import streamlit as st
import requests
import json
import uuid
import extra_streamlit_components as stx

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# فرض اتجاه الكتابة من اليمين إلى اليسار على كامل الصفحة
st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        direction: rtl;
    }
    .stMarkdown, .stCaption, .stTextArea textarea, label, .stSlider {
        text-align: right;
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# --- إدارة رمز عشوائي غير مرتبط بأي هوية، لمنع التكرار فقط ---
cookie_manager = stx.CookieManager(key="cookie_manager")

if "cookie_checked" not in st.session_state:
    st.session_state.cookie_checked = False
    st.session_state.survey_token = None

if not st.session_state.cookie_checked:
    existing_token = cookie_manager.get(cookie="survey_token")
    st.session_state.cookie_checked = True
    if existing_token is not None:
        st.session_state.survey_token = existing_token
    else:
        # قد يكون هذا مجرد تأخر بمزامنة المكوّن مع المتصفح، لا "غياب فعلي" للكوكيز
        # ننتظر دورة تحميل إضافية قبل الحسم بأنها زيارة جديدة فعلاً
        st.session_state.cookie_checked = False
        st.stop()

if st.session_state.survey_token is None:
    # بعد التأكد الفعلي من غياب الكوكيز، ننشئ رمزاً جديداً مرة واحدة فقط
    st.session_state.survey_token = str(uuid.uuid4())
    cookie_manager.set("survey_token", st.session_state.survey_token, key="set_token")

respondent_token = st.session_state.survey_token

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("استطلاع رأي حول الأداء والتعامل المهني (زميلكم طارق البلاسمة)")

if st.session_state.submitted:
    st.success("✅ شكراً لك! تم استلام تقييمك بنجاح.")
    st.stop()

# ضع الرابط الخاص بك هنا (تأكد أنه بين علامتي التنصيص "")
script_url = "https://script.google.com/macros/s/AKfycbxLsDcgEpWtw0sPNTsLdjILT099ElJzeEoyP6PvANFnbVJtLiDBlrnz-6EFbKShpAuB/exec"

# سؤال السكربت مسبقاً: هل هذا الرمز قدّم الاستبيان من قبل؟
if "already_submitted" not in st.session_state:
    try:
        check_resp = requests.get(script_url, params={"token": respondent_token}, timeout=10)
        st.session_state.already_submitted = check_resp.json().get("submitted", False)
    except Exception:
        # تعذّر التحقق (مشكلة اتصال) - نفترض عدم التقديم ونكمل بشكل طبيعي
        st.session_state.already_submitted = False

if st.session_state.already_submitted:
    st.info("يبدو أنك قدّمت هذا التقييم مسبقاً، شكراً لمشاركتك!")
    st.stop()

# --- واجهة الاستبيان ---
st.markdown("""
عزيزي الزميل/ة، هذا الاستطلاع **مجهول بالكامل بالنسبة لي**؛ لا أستطيع ولا أرغب
بمعرفة هويتك أو ربط إجابتك باسمك. يُخزَّن في متصفحك رمز عشوائي (لا يحمل أي معلومة
عنك) هدفه الوحيد منع تكرار التعبئة أكثر من مرة. هدف الاستبيان تحسين الأداء والتعامل المهني.
<hr>
""", unsafe_allow_html=True)

with st.form(key="survey_form"):
    st.caption("مقياس التقييم: 1 = ضعيف  ←  →  5 = قوي")
    work_style = st.select_slider("1. أسلوبي العام في العمل وتنسيق المهام:", options=[1, 2, 3, 4, 5], value=3)
    efficiency = st.select_slider("2. كفاءتي المهنية وقدرتي على إنجاز العمل:", options=[1, 2, 3, 4, 5], value=3)
    interaction = st.select_slider("3. المعاملة الشخصية والتواصل الإنساني معكم:", options=[1, 2, 3, 4, 5], value=3)
    leadership = st.select_slider("4. قدرتي على القيادة واتخاذ القرار:", options=[1, 2, 3, 4, 5], value=3)
    communication = st.select_slider("5. وضوح تواصلي وتعليماتي بخصوص المهام:", options=[1, 2, 3, 4, 5], value=3)
    fairness = st.select_slider("6. عدالتي وموضوعيتي بالتعامل مع أعضاء الفريق:", options=[1, 2, 3, 4, 5], value=3)
    openness = st.select_slider("7. انفتاحي على أفكاركم ونقدكم البنّاء:", options=[1, 2, 3, 4, 5], value=3)
    talent_dev = st.select_slider("8. دعمي لتطوير مهاراتكم ومواهبكم:", options=[1, 2, 3, 4, 5], value=3)
    notes = st.text_area("ملاحظات إضافية (اختياري):")

    submit_button = st.form_submit_button(label="إرسال التقييم")

if submit_button:
    payload = {
        "work_style": str(work_style),
        "efficiency": str(efficiency),
        "interaction": str(interaction),
        "leadership": str(leadership),
        "communication": str(communication),
        "fairness": str(fairness),
        "openness": str(openness),
        "talent_dev": str(talent_dev),
        "notes": notes,
        "dedup_token": respondent_token,  # رمز عشوائي فقط لفلترة التكرار، لا يحمل أي هوية
    }

    try:
        resp = requests.post(script_url, data=json.dumps(payload), timeout=15)
        status = resp.json().get("status", "success")
    except Exception:
        status = "success"  # تعذّر التأكد من الاستجابة، نعرض رسالة عامة للزميل

    if status == "duplicate":
        st.session_state.already_submitted = True
    else:
        st.session_state.submitted = True

    st.rerun()
