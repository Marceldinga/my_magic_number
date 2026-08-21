
import streamlit as st
import hashlib
import html

st.set_page_config(
    page_title="MACCO Magic Number",
    page_icon="✨",
    layout="centered"
)

# =========================================================
# STYLES
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(255,0,180,0.15), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(0,180,255,0.18), transparent 28%),
        radial-gradient(circle at 50% 75%, rgba(145,0,255,0.14), transparent 35%),
        linear-gradient(135deg, #03050d, #08091c, #100729, #05040d);
    color: white;
    overflow-x: hidden;
}

.block-container {
    max-width: 760px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* DISCO BALL */
.disco-ball {
    width: 105px;
    height: 105px;
    margin: 0 auto 12px auto;
    border-radius: 50%;
    background:
        repeating-linear-gradient(
            45deg,
            rgba(255,255,255,0.18) 0px,
            rgba(255,255,255,0.18) 6px,
            rgba(0,0,0,0.08) 6px,
            rgba(0,0,0,0.08) 12px
        ),
        linear-gradient(135deg, #3bcfff, #ae48ff, #ff4dc4, #ffd95c);
    box-shadow:
        0 0 18px #a53cff,
        0 0 35px #3bcfff,
        0 0 55px rgba(255,75,220,0.5);
    animation: pulseBall 2s infinite alternate;
}

@keyframes pulseBall {
    from {
        transform: scale(1);
        filter: brightness(1);
    }
    to {
        transform: scale(1.05);
        filter: brightness(1.25);
    }
}

/* MACCO */
.macco {
    text-align: center;
    font-size: 32px;
    font-weight: 900;
    letter-spacing: 12px;
    margin-bottom: 6px;

    background: linear-gradient(
        90deg,
        #fff3a2,
        #ffd34f,
        #ffb000,
        #fff3a2
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 8px rgba(255,215,80,0.7),
        0 0 20px rgba(255,180,20,0.5);
}

/* TITLE */
.magic-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    line-height: 1.05;
    margin-top: 10px;

    background: linear-gradient(
        90deg,
        #ff55d7,
        #ffd85b,
        #4bd8ff,
        #9d62ff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 20px rgba(255,80,220,0.15);
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: #e2e5f4;
    font-size: 17px;
    margin-top: 12px;
    margin-bottom: 34px;
}

/* INPUT LABELS */
label[data-testid="stWidgetLabel"] p {
    font-weight: 800 !important;
    color: #ffd75d !important;
}

/* INPUTS */
div[data-testid="stTextInput"] input {
    height: 56px;
    border-radius: 17px;
    font-size: 18px;
    background-color: rgba(10,12,28,0.92);
    color: white;
    border: 1px solid rgba(255,215,90,0.55);
    box-shadow:
        inset 0 0 8px rgba(255,255,255,0.03),
        0 0 12px rgba(255,80,220,0.08);
}

/* BUTTON */
div.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 18px;
    border: 1px solid #ffe17a;
    font-size: 20px;
    font-weight: 900;
    color: #111;

    background: linear-gradient(
        90deg,
        #ffbd22,
        #ffe56e,
        #ffb800
    );

    box-shadow:
        0 0 10px rgba(255,215,70,0.8),
        0 0 30px rgba(255,170,0,0.45);

    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow:
        0 0 14px rgba(255,225,100,1),
        0 0 40px rgba(255,170,0,0.55);
}

/* SECTION */
.symbol-label {
    margin-top: 42px;
    text-align: center;
    color: #ffd85f;
    font-weight: 900;
    letter-spacing: 3px;
    font-size: 16px;
}

/* OUTER STAGE */
.stage {
    position: relative;
    width: 430px;
    min-height: 490px;
    margin: 22px auto 0 auto;
}

/* TRIANGLE */
.triangle {
    position: absolute;
    top: 18px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;

    border-left: 205px solid transparent;
    border-right: 205px solid transparent;
    border-bottom: 365px solid #f2ba2f;

    filter:
        drop-shadow(0 0 6px #ffd760)
        drop-shadow(0 0 18px rgba(255,183,30,0.85))
        drop-shadow(0 0 35px rgba(255,105,0,0.45));

    animation: triangleGlow 1.8s infinite alternate;
}

@keyframes triangleGlow {
    from {
        filter:
            drop-shadow(0 0 6px #ffd760)
            drop-shadow(0 0 16px rgba(255,183,30,0.6));
    }
    to {
        filter:
            drop-shadow(0 0 10px #fff0a0)
            drop-shadow(0 0 30px rgba(255,183,30,0.95));
    }
}

/* INNER TRIANGLE */
.triangle-inner {
    position: absolute;
    top: 40px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;

    border-left: 180px solid transparent;
    border-right: 180px solid transparent;
    border-bottom: 320px solid rgba(4,8,24,0.96);
}

/* CONTENT */
.triangle-content {
    position: absolute;
    top: 102px;
    left: 0;
    width: 100%;
    text-align: center;
    z-index: 10;
}

/* CROWN */
.crown {
    font-size: 36px;
    margin-bottom: 4px;
    filter: drop-shadow(0 0 10px rgba(255,205,50,0.7));
}

/* NUMBER */
.magic-number {
    font-size: 112px;
    font-weight: 900;
    line-height: 0.95;

    background: linear-gradient(
        180deg,
        #fff7b0,
        #ffd84c,
        #ffaf00,
        #fff1a0
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 12px rgba(255,220,80,0.55),
        0 0 28px rgba(255,180,0,0.35);

    animation: numberPulse 1.5s infinite alternate;
}

@keyframes numberPulse {
    from {
        transform: scale(1);
    }
    to {
        transform: scale(1.04);
    }
}

/* FULL NAME */
.name-wrap {
    margin-top: 24px;
    font-size: 31px;
    font-weight: 900;
    letter-spacing: 3px;
    line-height: 1.25;
}

.first-name {
    color: #4bd8ff;
    text-shadow:
        0 0 7px #4bd8ff,
        0 0 18px rgba(75,216,255,0.5);
}

.last-name {
    color: #ff4fd8;
    text-shadow:
        0 0 7px #ff4fd8,
        0 0 18px rgba(255,79,216,0.5);
}

/* FLOWERS */
.flower {
    position: absolute;
    z-index: 20;
    font-size: 48px;
    animation: flowerGlow 2s infinite alternate;
}

@keyframes flowerGlow {
    from {
        filter: drop-shadow(0 0 6px rgba(255,255,255,0.35));
    }
    to {
        filter: drop-shadow(0 0 18px rgba(255,80,220,0.75));
    }
}

.flower1 {
    left: -8px;
    top: 275px;
}

.flower2 {
    right: -8px;
    top: 275px;
}

.flower3 {
    left: 42px;
    top: 335px;
    font-size: 38px;
}

.flower4 {
    right: 42px;
    top: 335px;
    font-size: 38px;
}

/* SPARKLES */
.sparkle {
    position: absolute;
    z-index: 30;
    animation: twinkle 1.2s infinite alternate;
}

.spark1 {
    top: 85px;
    left: 60px;
}

.spark2 {
    top: 120px;
    right: 58px;
}

.spark3 {
    top: 220px;
    left: 18px;
}

.spark4 {
    top: 225px;
    right: 18px;
}

@keyframes twinkle {
    from {
        opacity: 0.4;
        transform: scale(0.8);
    }
    to {
        opacity: 1;
        transform: scale(1.3);
    }
}

/* PLATFORM */
.platform {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    width: 320px;
    height: 38px;
    border-radius: 50%;
    background: linear-gradient(
        90deg,
        #4e1eff,
        #ff35cf,
        #3bcfff
    );
    box-shadow:
        0 0 12px #8a39ff,
        0 0 30px rgba(255,60,220,0.5);
}

/* MESSAGE */
.message {
    text-align: center;
    margin-top: 4px;
    font-size: 17px;
    font-weight: 700;

    background: linear-gradient(
        90deg,
        #ffd75d,
        #ff55d8,
        #49d9ff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 42px;
    color: #a4aac2;
    font-size: 13px;
}

/* MOBILE */
@media (max-width: 520px) {

    .magic-title {
        font-size: 36px;
    }

    .stage {
        width: 340px;
        min-height: 410px;
    }

    .triangle {
        border-left-width: 165px;
        border-right-width: 165px;
        border-bottom-width: 300px;
    }

    .triangle-inner {
        top: 36px;
        border-left-width: 145px;
        border-right-width: 145px;
        border-bottom-width: 262px;
    }

    .triangle-content {
        top: 88px;
    }

    .magic-number {
        font-size: 88px;
    }

    .name-wrap {
        font-size: 24px;
    }

    .flower1, .flower2 {
        top: 235px;
        font-size: 40px;
    }

    .flower3, .flower4 {
        top: 285px;
        font-size: 32px;
    }

    .platform {
        width: 270px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HIDDEN CALCULATION
# =========================================================

def name_magic(first_name, last_name):
    full_name = f"{first_name.strip().lower()} {last_name.strip().lower()}"
    encoded = hashlib.sha256(full_name.encode("utf-8")).hexdigest()

    return int(encoded[:10], 16) % 99 + 1

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="disco-ball"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="macco">✦ MACCO ✦</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="magic-title">✨ YOUR MAGIC NUMBER ✨</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Enter your name and discover the number hidden within your MACCO identity.'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# INPUTS
# =========================================================

first_name = st.text_input(
    "FIRST NAME",
    placeholder="Enter your first name"
)

last_name = st.text_input(
    "LAST NAME",
    placeholder="Enter your last name"
)

# =========================================================
# RESULT
# =========================================================

if st.button(
    "✨ REVEAL MY MAGIC NUMBER",
    use_container_width=True
):

    first_name = first_name.strip()
    last_name = last_name.strip()

    if not first_name or not last_name:

        st.warning(
            "Please enter both your first and last name."
        )

    else:

        result = name_magic(first_name, last_name)

        safe_first = html.escape(first_name.upper())
        safe_last = html.escape(last_name.upper())

        st.balloons()

        result_html = (
            '<div class="symbol-label">'
            'YOUR MACCO MAGIC SYMBOL'
            '</div>'

            '<div class="stage">'

            '<div class="triangle"></div>'
            '<div class="triangle-inner"></div>'

            '<div class="sparkle spark1">✨</div>'
            '<div class="sparkle spark2">✨</div>'
            '<div class="sparkle spark3">✦</div>'
            '<div class="sparkle spark4">✦</div>'

            '<div class="flower flower1">🌸</div>'
            '<div class="flower flower2">🌺</div>'
            '<div class="flower flower3">🌼</div>'
            '<div class="flower flower4">🌷</div>'

            '<div class="triangle-content">'

            '<div class="crown">👑</div>'

            f'<div class="magic-number">'
            f'{result}'
            '</div>'

            '<div class="name-wrap">'

            f'<div class="first-name">'
            f'{safe_first}'
            '</div>'

            f'<div class="last-name">'
            f'{safe_last}'
            '</div>'

            '</div>'

            '</div>'

            '<div class="platform"></div>'

            '</div>'

            '<div class="message">'
            '✨ YOU ARE UNIQUE. YOU ARE MAGIC. ✨'
            '</div>'
        )

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'Powered by MACCO ✨'
    '</div>',
    unsafe_allow_html=True
)
