import streamlit as st
import hashlib

st.set_page_config(
    page_title="MACCO Magic Number",
    page_icon="✨",
    layout="centered"
)

# ---------- CUSTOM DESIGN ----------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #070b14, #12182b, #1c1233);
            color: white;
        }

        .main-card {
            background: rgba(255, 255, 255, 0.08);
            padding: 28px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 10px 35px rgba(0,0,0,0.35);
            backdrop-filter: blur(10px);
            margin-top: 20px;
        }

        .brand {
            text-align: center;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: 6px;
            color: #f6c85f;
            margin-bottom: 8px;
        }

        .title {
            text-align: center;
            font-size: 44px;
            font-weight: 900;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #c9c9d4;
            font-size: 17px;
            margin-bottom: 28px;
        }

        .result-card {
            margin-top: 25px;
            padding: 28px;
            border-radius: 22px;
            text-align: center;
            background: linear-gradient(
                135deg,
                rgba(246,200,95,0.20),
                rgba(122,92,255,0.18)
            );
            border: 1px solid rgba(246,200,95,0.35);
            box-shadow: 0 8px 30px rgba(0,0,0,0.30);
        }

        .result-label {
            color: #d8d8e4;
            font-size: 16px;
        }

        .magic-number {
            font-size: 64px;
            font-weight: 900;
            color: #f6c85f;
            margin: 6px 0;
        }

        .name-text {
            font-size: 20px;
            font-weight: 700;
        }

        div.stButton > button {
            width: 100%;
            border-radius: 14px;
            height: 3.2em;
            font-size: 18px;
            font-weight: 800;
            border: none;
            background: linear-gradient(90deg, #f6c85f, #c79d33);
            color: #111111;
        }

        div.stButton > button:hover {
            transform: scale(1.02);
            transition: 0.2s;
        }

        input {
            border-radius: 12px !important;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- MAGIC FUNCTION ----------
def name_magic(first_name, last_name):
    full_name = f"{first_name.strip().lower()} {last_name.strip().lower()}"

    # Stable hidden calculation
    encoded = hashlib.sha256(full_name.encode()).hexdigest()

    number = int(encoded[:8], 16) % 90 + 10

    return number


# ---------- UI ----------
st.markdown('<div class="brand">MACCO</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="title">✨ Discover Your Magic Number</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your name carries a unique number. Enter it below and reveal yours.</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

first_name = st.text_input(
    "First Name",
    placeholder="Enter your first name"
)

last_name = st.text_input(
    "Last Name",
    placeholder="Enter your last name"
)

if st.button("✨ Reveal My Magic Number"):

    if not first_name.strip() or not last_name.strip():
        st.warning("Please enter both your first and last name.")

    else:
        magic_number = name_magic(first_name, last_name)

        st.balloons()

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Your Magic Number</div>

                <div class="magic-number">
                    {magic_number}
                </div>

                <div class="name-text">
                    ✨ {first_name.strip()} {last_name.strip()} ✨
                </div>

                <p style="color:#c9c9d4; margin-top:12px;">
                    A unique number created especially from your name.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#77798a;
        font-size:13px;
        margin-top:35px;
    ">
        Powered by MACCO ✨
    </p>
    """,
    unsafe_allow_html=True
)
