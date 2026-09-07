"""
app.py
-------
Streamlit web app: Spam Email Detector

Lets a user paste/type an email and predicts whether it is Spam or Not Spam
using a TF-IDF + Naive Bayes model trained in train_model.py.

Run locally with:
    streamlit run app.py
"""

import os
import joblib
import streamlit as st

# ---------------------------------------------------------------------------
# Page config (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Spam Email Detector",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Custom CSS — animated gradient background + glass-card styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #1e3c72, #2a5298, #6a11cb, #2575fc);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glass-morphism card wrapper */
    .glass-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    }

    .title-text {
        text-align: center;
        color: #ffffff;
        font-weight: 700;
        font-size: 2.6rem;
        margin-bottom: 0;
        text-shadow: 0 2px 12px rgba(0,0,0,0.35);
    }

    .subtitle-text {
        text-align: center;
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem;
        margin-top: 0.3rem;
        margin-bottom: 1.5rem;
    }

    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        font-size: 1rem;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff512f, #dd2476);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.6rem 0;
        border-radius: 12px;
        border: none;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
        color: white;
    }

    .result-spam {
        background: rgba(220, 53, 69, 0.85);
        color: white;
        padding: 1.2rem;
        border-radius: 14px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }

    .result-ham {
        background: rgba(40, 167, 69, 0.85);
        color: white;
        padding: 1.2rem;
        border-radius: 14px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Load model (train on the fly if the .pkl files aren't present yet, e.g.
# on a fresh deploy where only the CSV was pushed)
# ---------------------------------------------------------------------------
MODEL_PATH = "model/spam_classifier.pkl"
VECTORIZER_PATH = "model/vectorizer.pkl"


@st.cache_resource
def load_or_train_model():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        # Train automatically if the pickle files are missing
        import train_model
        train_model.main()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


model, vectorizer = load_or_train_model()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<p class="title-text">📧 Spam Email Detector</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle-text">Paste an email below and let the ML model decide '
    'if it is <b>Spam</b> or <b>Not Spam</b></p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Input card
# ---------------------------------------------------------------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

example_emails = {
    "-- Select an example (optional) --": "",
    "Example: Spam email": (
        "Congratulations! You have WON $1,000,000 in our lottery draw. "
        "Click the link below within 24 hours to claim your prize before it expires. "
        "Act now, this is a limited time offer!"
    ),
    "Example: Normal email": (
        "Hi team, just a reminder that our project standup is at 10:00 AM tomorrow. "
        "Please come prepared with an update on your current tasks. Thanks!"
    ),
}

choice = st.selectbox("Quick-fill an example", list(example_emails.keys()))
default_text = example_emails[choice]

email_text = st.text_area(
    "Email content",
    value=default_text,
    height=220,
    placeholder="Paste or type the email you want to check here...",
)

predict_clicked = st.button("🔍 Predict")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Output card
# ---------------------------------------------------------------------------
if predict_clicked:
    if not email_text.strip():
        st.warning("Please enter some email text first.")
    else:
        vec = vectorizer.transform([email_text])
        prediction = model.predict(vec)[0]
        probabilities = model.predict_proba(vec)[0]
        classes = list(model.classes_)
        spam_prob = probabilities[classes.index("spam")] * 100
        ham_prob = probabilities[classes.index("ham")] * 100

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        if prediction == "spam":
            st.markdown(
                f'<div class="result-spam">🚨 This email looks like SPAM<br>'
                f'Confidence: {spam_prob:.1f}%</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="result-ham">✅ This email looks SAFE (Not Spam)<br>'
                f'Confidence: {ham_prob:.1f}%</div>',
                unsafe_allow_html=True,
            )

        st.write("")
        col1, col2 = st.columns(2)
        col1.metric("Spam probability", f"{spam_prob:.1f}%")
        col2.metric("Not-spam probability", f"{ham_prob:.1f}%")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Footer note
# ---------------------------------------------------------------------------
st.markdown(
    '<p style="text-align:center; color: rgba(255,255,255,0.7); font-size: 0.85rem;">'
    'Built with Streamlit &bull; TF-IDF + Naive Bayes model</p>',
    unsafe_allow_html=True,
)
