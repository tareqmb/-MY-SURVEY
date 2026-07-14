import streamlit as st
import requests
import json
import uuid

# إعداد الصفحة
st.set_page_config(page_title="استطلاع رأي مهني", layout="centered")

# فرض اتجاه الكتابة من اليمين إلى اليسار على كامل الصفحة + لمسات تصميم حيوية
st.markdown("""
    <style>
    html, body, [class*="css"], .stApp {
        direction: rtl;
    }
    .stMarkdown, .stCaption, .stTextArea textarea, label, .stSlider {
        text-align: right;
        direction: rtl;
    }
    .survey-header {
        background: linear-gradient(135deg, #0F766E 0%, #14B8A6 100%);
        padding: 28px 24px;
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(15, 118, 110, 0.25);
    }
    .survey-header h1 {
        color: white !important;
        font-size: 26px;
        margin: 0;
        text-align: center;
    }
    .survey-header p {
        color: #E6FFFA;
        text-align: center;
        margin-top: 8px;
        font-size: 15px;
    }
    .form-card {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 20px 24px;
        border: 1px solid #E2E8F0;
        margin-bottom: 12px;
    }
    div[data-testid="stForm"] {
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px;
        background-color: #FAFFFE;
    }
    .stButton>button, .stFormSubmitButton>button {
        background-color: #0F766E;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 22px;
    }
    </style>
""", unsafe_allow_html=True)

# --- الحصول على رمز عشوائي لمنع التكرار، عبر رابط Streamlit أصلي (بدون أي إطار أو جافاسكربت) ---
# هذا الرابط جزء طبيعي من صفحة التطبيق نفسها (وليس داخل iframe)، لذلك يعمل
# بنفس الطريقة تماماً على كل المتصفحات والأجهزة بدون استثناء.
respondent_token = st.query_params.get("token")

if not respondent_token:
    st.markdown("""
        <div class="survey-header">
            <h1>📋 استطلاع رأي حول الأداء والتعامل المهني</h1>
            <p>زميلكم طارق البلاسمة</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("اضغط الرابط أدناه للمتابعة إلى الاستبيان:")
    new_token = str(uuid.uuid4())
    st.link_button("ابدأ الاستبيان ←", f"?token={new_token}")
    st.stop()

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.markdown("""
    <div class="survey-header">
        <h1>📋 استطلاع رأي حول الأداء والتعامل المهني</h1>
        <p>زميلكم طارق البلاسمة</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.submitted:
    st.success("✅ شكراً لك! تم استلام تقييمك بنجاح.")
    st.stop()

# ضع الرابط الخاص بك هنا (تأكد أنه بين علامتي التنصيص "")
script_url = "https://script.google.com/macros/s/AKfycbxT4UXKVfbe0P3XyzD--0l49b9GdnMwzNm9depvX3xTTx-_90bC13kGdaC0Z_31sHg9/exec"

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
<div class="form-card">
عزيزي الزميل/ة، هذا الاستطلاع <b>مجهول بالكامل بالنسبة لي</b>؛ لا أستطيع ولا أرغب
بمعرفة هويتك أو ربط إجابتك باسمك. هدف الاستبيان تحسين الأداء والتعامل المهني. 🌟
</div>
""", unsafe_allow_html=True)

# مقياس تقييم وصفي بتدرّج (نفس القيم الرقمية 1-5 من الخلف، لكن بعرض وصفي أوضح)
SCALE_LABELS = {
    1: "1 – ضعيف 🔴",
    2: "2 – دون المتوسط 🟠",
    3: "3 – متوسط 🟡",
    4: "4 – جيد 🟢",
    5: "5 – ممتاز 💚",
}

with st.form(key="survey_form"):
    st.caption("مقياس التقييم يتدرّج من الأحمر (ضعيف) إلى الأخضر (ممتاز)")
    work_style = st.select_slider("🗂️ 1. أسلوبي العام في العمل وتنسيق المهام:",
                                   options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    efficiency = st.select_slider("⚡ 2. كفاءتي المهنية وقدرتي على إنجاز العمل:",
                                   options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    interaction = st.select_slider("🤝 3. المعاملة الشخصية والتواصل الإنساني معكم:",
                                    options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    leadership = st.select_slider("🎯 4. قدرتي على القيادة واتخاذ القرار:",
                                   options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    communication = st.select_slider("💬 5. وضوح تواصلي وتعليماتي بخصوص المهام:",
                                      options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    fairness = st.select_slider("⚖️ 6. عدالتي وموضوعيتي بالتعامل مع أعضاء الفريق:",
                                 options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    openness = st.select_slider("💡 7. انفتاحي على أفكاركم ونقدكم البنّاء:",
                                 options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    talent_dev = st.select_slider("🌱 8. دعمي لتطوير مهاراتكم ومواهبكم:",
                                   options=[1, 2, 3, 4, 5], value=3, format_func=lambda x: SCALE_LABELS[x])
    notes = st.text_area("📝 ملاحظات إضافية (اختياري):")

    submit_button = st.form_submit_button(label="إرسال التقييم 🚀")

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
