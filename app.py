import streamlit as st
import hashlib
import html
import json
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MACCO Magic Number",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "first_name" not in st.session_state:
    st.session_state.first_name = ""

if "last_name" not in st.session_state:
    st.session_state.last_name = ""

if "reveal_id" not in st.session_state:
    st.session_state.reveal_id = 0


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

/* =======================================================
   GLOBAL
   ======================================================= */

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 15%, rgba(255, 0, 180, .22), transparent 25%),
        radial-gradient(circle at 88% 12%, rgba(0, 205, 255, .22), transparent 28%),
        radial-gradient(circle at 50% 75%, rgba(155, 0, 255, .20), transparent 35%),
        radial-gradient(circle at 15% 90%, rgba(255, 185, 0, .12), transparent 25%),
        linear-gradient(135deg, #02030a, #09051c, #17072d, #05030d);

    color: white;
    overflow-x: hidden;
}

.block-container {
    max-width: 790px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}


/* =======================================================
   FLOATING BACKGROUND LIGHTS
   ======================================================= */

.bg-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(6px);
    opacity: .35;
    z-index: 0;
    pointer-events: none;
    animation: floatOrb 8s ease-in-out infinite alternate;
}

.orb1 {
    width: 100px;
    height: 100px;
    left: 5%;
    top: 18%;
    background: #ff37c7;
    box-shadow: 0 0 80px #ff37c7;
}

.orb2 {
    width: 80px;
    height: 80px;
    right: 5%;
    top: 35%;
    background: #35d9ff;
    box-shadow: 0 0 80px #35d9ff;
    animation-delay: 1s;
}

.orb3 {
    width: 65px;
    height: 65px;
    left: 15%;
    bottom: 12%;
    background: #ffd342;
    box-shadow: 0 0 70px #ffd342;
    animation-delay: 2s;
}

@keyframes floatOrb {
    from {
        transform: translateY(-10px) scale(.9);
    }
    to {
        transform: translateY(30px) scale(1.15);
    }
}


/* =======================================================
   TOP DECORATION
   ======================================================= */

.top-decoration {
    text-align: center;
    font-size: 26px;
    letter-spacing: 15px;
    margin-bottom: 8px;
    animation: topTwinkle 1.5s infinite alternate;
}

@keyframes topTwinkle {
    from {
        opacity: .55;
        transform: scale(.97);
    }
    to {
        opacity: 1;
        transform: scale(1.04);
    }
}


/* =======================================================
   DISCO BALL
   ======================================================= */

.disco-wrap {
    position: relative;
    width: 125px;
    height: 125px;
    margin: 0 auto 8px auto;
}

.disco-ring {
    position: absolute;
    inset: -10px;
    border-radius: 50%;
    border: 2px solid rgba(255, 215, 70, .35);
    box-shadow:
        0 0 20px #ff40d0,
        0 0 45px #34d9ff,
        inset 0 0 20px rgba(255,255,255,.1);

    animation: ringRotate 8s linear infinite;
}

@keyframes ringRotate {
    to {
        transform: rotate(360deg);
    }
}

.disco-ball {
    width: 105px;
    height: 105px;
    position: absolute;
    left: 10px;
    top: 10px;
    border-radius: 50%;

    background:
        repeating-linear-gradient(
            45deg,
            rgba(255,255,255,.30) 0px,
            rgba(255,255,255,.30) 5px,
            rgba(0,0,0,.08) 5px,
            rgba(0,0,0,.08) 10px
        ),
        linear-gradient(
            135deg,
            #3bcfff,
            #ae48ff,
            #ff4dc4,
            #ffd95c
        );

    box-shadow:
        0 0 18px #a53cff,
        0 0 38px #3bcfff,
        0 0 65px rgba(255,75,220,.65);

    animation: pulseBall 1.8s infinite alternate;
}

@keyframes pulseBall {
    from {
        transform: scale(1) rotate(-4deg);
        filter: brightness(1);
    }
    to {
        transform: scale(1.06) rotate(4deg);
        filter: brightness(1.35);
    }
}


/* =======================================================
   MACCO BRAND
   ======================================================= */

.macco {
    text-align: center;
    font-size: 34px;
    font-weight: 900;
    letter-spacing: 12px;
    margin-top: 12px;

    background: linear-gradient(
        90deg,
        #fff4a5,
        #ffd64e,
        #ffad00,
        #fff4a5
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 8px rgba(255,215,80,.7),
        0 0 22px rgba(255,180,20,.45);
}

.magic-title {
    text-align: center;
    font-size: 48px;
    font-weight: 900;
    line-height: 1.05;
    margin-top: 13px;

    background: linear-gradient(
        90deg,
        #ff55d7,
        #ffd85b,
        #4bd8ff,
        #9d62ff,
        #ff55d7
    );

    background-size: 300% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleFlow 5s linear infinite;
}

@keyframes titleFlow {
    to {
        background-position: 300% center;
    }
}

.subtitle {
    text-align: center;
    color: #e2e5f4;
    font-size: 17px;
    line-height: 1.65;
    margin: 14px auto 30px auto;
    max-width: 600px;
}


/* =======================================================
   INPUT AREA
   ======================================================= */

.input-card {
    border: 1px solid rgba(255,215,90,.25);
    background: rgba(8,8,25,.45);
    border-radius: 25px;
    padding: 8px 16px 4px 16px;
    margin-bottom: 8px;
    box-shadow:
        0 0 25px rgba(157,98,255,.10),
        inset 0 0 25px rgba(255,255,255,.02);
}

label[data-testid="stWidgetLabel"] p {
    font-weight: 900 !important;
    color: #ffd75d !important;
    letter-spacing: 1px;
}

div[data-testid="stTextInput"] input {
    height: 58px;
    border-radius: 17px;
    font-size: 18px;
    background-color: rgba(10,12,28,.96);
    color: white;

    border: 1px solid rgba(255,215,90,.55);

    box-shadow:
        inset 0 0 8px rgba(255,255,255,.03),
        0 0 12px rgba(255,80,220,.08);
}

div[data-testid="stTextInput"] input:focus {
    border: 1px solid #ffd75d;
    box-shadow:
        0 0 12px rgba(255,215,93,.35),
        0 0 22px rgba(255,80,220,.18);
}


/* =======================================================
   BUTTON
   ======================================================= */

div.stButton > button {
    width: 100%;
    height: 62px;
    border-radius: 19px;

    border: 1px solid #fff1a3;

    font-size: 20px;
    font-weight: 900;
    color: #16100a;

    background:
        linear-gradient(
            90deg,
            #ffae16,
            #ffe979,
            #ffbc22,
            #ffe979,
            #ffae16
        );

    background-size: 250% auto;

    box-shadow:
        0 0 12px rgba(255,215,70,.85),
        0 0 32px rgba(255,170,0,.42);

    animation: buttonGold 4s linear infinite;

    transition: .2s;
}

@keyframes buttonGold {
    to {
        background-position: 250% center;
    }
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.012);

    box-shadow:
        0 0 18px rgba(255,225,100,1),
        0 0 45px rgba(255,100,210,.45);
}


/* =======================================================
   RESULT HEADER
   ======================================================= */

.symbol-label {
    margin-top: 42px;
    text-align: center;
    color: #ffd85f;
    font-weight: 900;
    letter-spacing: 3px;
    font-size: 16px;
}

.reveal-text {
    text-align: center;
    margin-top: 8px;
    color: #f5eaff;
    font-size: 14px;
}


/* =======================================================
   MAGIC STAGE
   ======================================================= */

.stage {
    position: relative;
    width: 460px;
    min-height: 510px;
    margin: 15px auto 0 auto;
}


/* =======================================================
   TRIANGLE
   ======================================================= */

.triangle {
    position: absolute;

    top: 25px;
    left: 50%;

    transform: translateX(-50%);

    width: 0;
    height: 0;

    border-left: 215px solid transparent;
    border-right: 215px solid transparent;
    border-bottom: 385px solid #f2ba2f;

    filter:
        drop-shadow(0 0 8px #ffd760)
        drop-shadow(0 0 20px rgba(255,183,30,.85))
        drop-shadow(0 0 40px rgba(255,105,0,.40));

    animation: triangleGlow 1.6s infinite alternate;
}

@keyframes triangleGlow {
    from {
        filter:
            drop-shadow(0 0 7px #ffd760)
            drop-shadow(0 0 18px rgba(255,183,30,.65));
    }
    to {
        filter:
            drop-shadow(0 0 13px #fff3ac)
            drop-shadow(0 0 35px rgba(255,183,30,1));
    }
}

.triangle-inner {
    position: absolute;

    top: 49px;
    left: 50%;

    transform: translateX(-50%);

    width: 0;
    height: 0;

    border-left: 187px solid transparent;
    border-right: 187px solid transparent;
    border-bottom: 335px solid rgba(4,8,24,.97);
}


/* =======================================================
   NUMBER CONTENT
   ======================================================= */

.triangle-content {
    position: absolute;

    top: 100px;
    left: 0;

    width: 100%;

    text-align: center;
    z-index: 10;
}

.crown {
    font-size: 40px;
    margin-bottom: 5px;

    filter:
        drop-shadow(0 0 12px rgba(255,205,50,.85));

    animation: crownFloat 1.6s ease-in-out infinite alternate;
}

@keyframes crownFloat {
    to {
        transform: translateY(-7px) rotate(4deg);
    }
}

.magic-number {
    font-size: 118px;
    font-weight: 900;
    line-height: .95;

    background:
        linear-gradient(
            180deg,
            #fffbd1,
            #ffe462,
            #ffaf00,
            #fff1a0
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 12px rgba(255,220,80,.55),
        0 0 30px rgba(255,180,0,.35);

    animation: numberPulse 1.25s infinite alternate;
}

@keyframes numberPulse {
    from {
        transform: scale(1);
    }
    to {
        transform: scale(1.055);
    }
}

.name-wrap {
    margin-top: 22px;

    font-size: 30px;
    font-weight: 900;
    letter-spacing: 3px;
    line-height: 1.3;
}

.first-name {
    color: #4bd8ff;

    text-shadow:
        0 0 7px #4bd8ff,
        0 0 18px rgba(75,216,255,.55);
}

.last-name {
    color: #ff4fd8;

    text-shadow:
        0 0 7px #ff4fd8,
        0 0 18px rgba(255,79,216,.55);
}


/* =======================================================
   FLOWERS
   ======================================================= */

.flower {
    position: absolute;
    z-index: 20;

    animation: flowerGlow 1.8s infinite alternate;
}

@keyframes flowerGlow {
    from {
        filter:
            drop-shadow(0 0 6px rgba(255,255,255,.35));

        transform: scale(.95) rotate(-5deg);
    }

    to {
        filter:
            drop-shadow(0 0 18px rgba(255,80,220,.85));

        transform: scale(1.08) rotate(5deg);
    }
}

.flower1 {
    left: -3px;
    top: 275px;
    font-size: 54px;
}

.flower2 {
    right: -3px;
    top: 275px;
    font-size: 54px;
}

.flower3 {
    left: 48px;
    top: 350px;
    font-size: 40px;
}

.flower4 {
    right: 48px;
    top: 350px;
    font-size: 40px;
}

.flower5 {
    left: 100px;
    top: 395px;
    font-size: 30px;
}

.flower6 {
    right: 100px;
    top: 395px;
    font-size: 30px;
}


/* =======================================================
   SPARKLES
   ======================================================= */

.sparkle {
    position: absolute;
    z-index: 30;

    animation:
        twinkle 1.1s infinite alternate;
}

.spark1 {
    top: 90px;
    left: 55px;
}

.spark2 {
    top: 125px;
    right: 55px;
}

.spark3 {
    top: 220px;
    left: 12px;
}

.spark4 {
    top: 230px;
    right: 12px;
}

.spark5 {
    top: 55px;
    right: 110px;
}

.spark6 {
    top: 55px;
    left: 110px;
}

@keyframes twinkle {
    from {
        opacity: .35;
        transform: scale(.7) rotate(0deg);
    }
    to {
        opacity: 1;
        transform: scale(1.45) rotate(25deg);
    }
}


/* =======================================================
   BUTTERFLIES
   ======================================================= */

.butterfly {
    position: absolute;
    z-index: 25;
    font-size: 30px;

    animation: butterflyFly 3s ease-in-out infinite alternate;
}

.butterfly1 {
    left: 25px;
    top: 175px;
}

.butterfly2 {
    right: 25px;
    top: 170px;
    animation-delay: 1s;
}

@keyframes butterflyFly {
    from {
        transform: translateY(5px) rotate(-8deg);
    }
    to {
        transform: translateY(-16px) rotate(8deg);
    }
}


/* =======================================================
   PLATFORM
   ======================================================= */

.platform {
    position: absolute;

    bottom: 18px;
    left: 50%;

    transform: translateX(-50%);

    width: 340px;
    height: 42px;

    border-radius: 50%;

    background:
        linear-gradient(
            90deg,
            #4e1eff,
            #ff35cf,
            #ffd542,
            #3bcfff,
            #4e1eff
        );

    background-size: 300% auto;

    box-shadow:
        0 0 14px #8a39ff,
        0 0 35px rgba(255,60,220,.55);

    animation: platformGlow 3s linear infinite;
}

@keyframes platformGlow {
    to {
        background-position: 300% center;
    }
}


/* =======================================================
   RESULT INFO CARD
   ======================================================= */

.magic-card {
    margin: 5px auto 20px auto;
    max-width: 620px;

    padding: 26px;

    border-radius: 27px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.10),
            rgba(255,255,255,.025)
        );

    border: 1px solid rgba(255,215,100,.38);

    backdrop-filter: blur(14px);

    box-shadow:
        0 0 30px rgba(160,70,255,.15),
        inset 0 0 20px rgba(255,255,255,.025);
}

.card-title {
    text-align: center;
    color: #ffd75d;
    font-size: 22px;
    font-weight: 900;
    margin-bottom: 20px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}

.stat {
    text-align: center;

    background: rgba(7,8,25,.72);

    border: 1px solid rgba(255,255,255,.10);

    border-radius: 18px;

    padding: 17px 8px;
}

.stat-icon {
    font-size: 28px;
}

.stat-value {
    font-size: 19px;
    font-weight: 900;
    color: white;
    margin-top: 5px;
}

.stat-label {
    color: #aeb5d0;
    font-size: 11px;
    margin-top: 5px;
    letter-spacing: 1px;
}

.explanation {
    text-align: center;
    color: #e9e8f7;
    line-height: 1.7;
    margin-top: 20px;
    font-size: 15px;
}


/* =======================================================
   MESSAGE
   ======================================================= */

.message {
    text-align: center;
    margin-top: 14px;

    font-size: 19px;
    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #ffd75d,
            #ff55d8,
            #49d9ff,
            #ffd75d
        );

    background-size: 250% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: messageFlow 4s linear infinite;
}

@keyframes messageFlow {
    to {
        background-position: 250% center;
    }
}


/* =======================================================
   VOICE LABEL
   ======================================================= */

.voice-note {
    text-align: center;

    color: #aeb6d6;

    font-size: 13px;

    margin: 8px auto 20px auto;
}


/* =======================================================
   FOOTER
   ======================================================= */

.footer {
    text-align: center;

    margin-top: 45px;

    color: #858ca8;

    font-size: 13px;
}


/* =======================================================
   MOBILE
   ======================================================= */

@media (max-width: 520px) {

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .magic-title {
        font-size: 35px;
    }

    .macco {
        font-size: 28px;
        letter-spacing: 8px;
    }

    .subtitle {
        font-size: 15px;
    }

    .stage {
        width: 340px;
        min-height: 420px;
    }

    .triangle {
        top: 25px;

        border-left-width: 165px;
        border-right-width: 165px;
        border-bottom-width: 300px;
    }

    .triangle-inner {
        top: 45px;

        border-left-width: 143px;
        border-right-width: 143px;
        border-bottom-width: 260px;
    }

    .triangle-content {
        top: 82px;
    }

    .crown {
        font-size: 31px;
    }

    .magic-number {
        font-size: 84px;
    }

    .name-wrap {
        font-size: 22px;
        margin-top: 16px;
    }

    .flower1,
    .flower2 {
        top: 225px;
        font-size: 41px;
    }

    .flower3,
    .flower4 {
        top: 285px;
        font-size: 31px;
    }

    .flower5,
    .flower6 {
        top: 320px;
        font-size: 25px;
    }

    .flower5 {
        left: 75px;
    }

    .flower6 {
        right: 75px;
    }

    .platform {
        width: 265px;
        height: 34px;
        bottom: 20px;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .butterfly1 {
        left: 10px;
    }

    .butterfly2 {
        right: 10px;
    }
}

</style>

<div class="bg-orb orb1"></div>
<div class="bg-orb orb2"></div>
<div class="bg-orb orb3"></div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# MACCO MAGIC ENGINE
# =========================================================

AURAS = [
    ("Golden", "🌟"),
    ("Rose", "🌹"),
    ("Violet", "💜"),
    ("Aqua", "💎"),
    ("Emerald", "🌿"),
    ("Solar", "☀️"),
    ("Moonlight", "🌙"),
    ("Rainbow", "🌈"),
    ("Crystal", "🔮"),
]

ELEMENTS = [
    ("Fire", "🔥"),
    ("Water", "💧"),
    ("Earth", "🌍"),
    ("Air", "🌬️"),
    ("Light", "✨"),
]

MESSAGES = [
    "Your energy carries creativity, confidence, and the courage to stand out.",
    "Your MACCO energy reflects warmth, imagination, and a naturally bright presence.",
    "You carry an adventurous energy that encourages discovery and new possibilities.",
    "Your energy represents growth, determination, and the ability to create something meaningful.",
    "Your MACCO identity shines through curiosity, originality, and positive energy.",
    "You carry a calm but powerful energy that can inspire the people around you.",
    "Your magic reflects ambition, imagination, and the confidence to follow your own path.",
    "Your energy combines creativity and resilience, giving your MACCO identity a distinctive glow.",
    "Your MACCO energy represents joy, possibility, and a willingness to dream beyond the ordinary.",
]


def macco_magic(first_name, last_name):
    """
    Deterministically creates a MACCO profile from the full name.

    Same normalized name = same MACCO profile.
    """

    normalized = " ".join(
        f"{first_name.strip().lower()} {last_name.strip().lower()}".split()
    )

    digest = hashlib.sha256(normalized.encode("utf-8")).digest()

    # Main number: 1-99
    magic_number = int.from_bytes(digest[0:4], "big") % 99 + 1

    # Power number: 1-9
    power_number = digest[4] % 9 + 1

    # Aura
    aura_name, aura_icon = AURAS[digest[5] % len(AURAS)]

    # Element
    element_name, element_icon = ELEMENTS[digest[6] % len(ELEMENTS)]

    # Message
    message = MESSAGES[digest[7] % len(MESSAGES)]

    return {
        "magic_number": magic_number,
        "power_number": power_number,
        "aura": aura_name,
        "aura_icon": aura_icon,
        "element": element_name,
        "element_icon": element_icon,
        "message": message,
    }


# =========================================================
# BROWSER VOICE
# =========================================================

def speak_macco_result(
    first_name,
    last_name,
    magic_number,
    power_number,
    aura,
    element,
    message,
    reveal_id,
):

    # json.dumps safely prepares Python strings for JavaScript.
    spoken_text = (
        f"Welcome {first_name} {last_name}, to MACCO Magic. "
        f"Your MACCO magic number is {magic_number}. "
        f"Your power number is {power_number}. "
        f"Your aura is {aura}, and your element is {element}. "
        f"{message} "
        f"Remember, {first_name}, you are unique. You are magic. "
        f"Welcome to your MACCO identity."
    )

    spoken_json = json.dumps(spoken_text)

    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">

        <style>

            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: Arial, Helvetica, sans-serif;
            }}

            .voice-box {{
                width: 100%;
                box-sizing: border-box;

                padding: 13px;

                border-radius: 18px;

                background:
                    linear-gradient(
                        90deg,
                        rgba(255,184,30,.15),
                        rgba(255,60,205,.15),
                        rgba(60,210,255,.15)
                    );

                border:
                    1px solid rgba(255,220,100,.35);

                text-align: center;
            }}

            .voice-title {{
                color: #ffe273;
                font-size: 13px;
                font-weight: 800;
                margin-bottom: 9px;
            }}

            button {{
                border: 1px solid rgba(255,230,130,.8);

                border-radius: 14px;

                padding: 10px 18px;

                background:
                    linear-gradient(
                        90deg,
                        #ffbc25,
                        #ffe76e
                    );

                color: #17100a;

                font-size: 14px;

                font-weight: 900;

                cursor: pointer;

                box-shadow:
                    0 0 12px rgba(255,200,40,.35);
            }}

            button:hover {{
                transform: scale(1.03);
            }}

        </style>

    </head>

    <body>

        <div class="voice-box">

            <div class="voice-title">
                🔊 MACCO VOICE GUIDE
            </div>

            <button onclick="speakMacco()">
                🔊 Hear My MACCO Reading
            </button>

        </div>


        <script>

            const textToSpeak = {spoken_json};

            function findPreferredVoice() {{

                const voices =
                    window.speechSynthesis.getVoices();

                if (!voices || voices.length === 0) {{
                    return null;
                }}

                /*
                Prefer natural English voices when available.
                Exact voices depend on the visitor's device/browser.
                */

                const preferredNames = [
                    "Samantha",
                    "Google US English",
                    "Microsoft Aria Online",
                    "Microsoft Jenny Online",
                    "Microsoft Zira",
                    "Karen",
                    "Moira"
                ];

                for (const preferred of preferredNames) {{

                    const voice = voices.find(v =>
                        v.name.toLowerCase().includes(
                            preferred.toLowerCase()
                        )
                    );

                    if (voice) {{
                        return voice;
                    }}
                }}

                const englishVoice = voices.find(v =>
                    v.lang &&
                    v.lang.toLowerCase().startsWith("en")
                );

                return englishVoice || voices[0];
            }}


            function speakMacco() {{

                if (!("speechSynthesis" in window)) {{
                    alert(
                        "Voice is not supported by this browser."
                    );
                    return;
                }}

                window.speechSynthesis.cancel();

                const speech =
                    new SpeechSynthesisUtterance(
                        textToSpeak
                    );

                const voice =
                    findPreferredVoice();

                if (voice) {{
                    speech.voice = voice;
                }}

                speech.lang = "en-US";

                /*
                Slightly slower rate gives the reading
                a more polished storytelling feeling.
                */

                speech.rate = 0.88;

                speech.pitch = 1.08;

                speech.volume = 1.0;

                window.speechSynthesis.speak(
                    speech
                );
            }}


            /*
            Browsers may block automatic speech until
            the visitor interacts with the page.

            We attempt auto-play after the result appears.
            If blocked, the voice button remains available.
            */

            function attemptAutoWelcome() {{

                setTimeout(() => {{

                    try {{
                        speakMacco();
                    }}
                    catch (error) {{
                        console.log(
                            "Automatic MACCO voice waiting for user interaction."
                        );
                    }}

                }}, 700);
            }}


            if (
                "speechSynthesis" in window
            ) {{

                window.speechSynthesis.onvoiceschanged =
                    function() {{
                        window.speechSynthesis.getVoices();
                    }};

                attemptAutoWelcome();
            }}

        </script>

    </body>
    </html>
    """

    components.html(
        component_html,
        height=100,
        scrolling=False,
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="top-decoration">
    ✦ ✨ 🌸 ✨ ✦
</div>

<div class="disco-wrap">
    <div class="disco-ring"></div>
    <div class="disco-ball"></div>
</div>

<div class="macco">
    ✦ MACCO ✦
</div>

<div class="magic-title">
    ✨ YOUR MAGIC NUMBER ✨
</div>

<div class="subtitle">
    Enter your name and step into the colorful world of MACCO.
    Discover your Magic Number, Power Number, Aura and Element.
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# INPUTS
# =========================================================

first_name = st.text_input(
    "✨ FIRST NAME",
    placeholder="Enter your first name",
    key="first_name_input",
)

last_name = st.text_input(
    "🌸 LAST NAME",
    placeholder="Enter your last name",
    key="last_name_input",
)


# =========================================================
# REVEAL BUTTON
# =========================================================

if st.button(
    "✨ REVEAL MY MACCO MAGIC ✨",
    use_container_width=True,
):

    clean_first = first_name.strip()
    clean_last = last_name.strip()

    if not clean_first or not clean_last:

        st.warning(
            "✨ Please enter both your first and last name."
        )

    else:

        st.session_state.result = macco_magic(
            clean_first,
            clean_last,
        )

        st.session_state.first_name = clean_first
        st.session_state.last_name = clean_last

        st.session_state.reveal_id += 1

        st.balloons()


# =========================================================
# DISPLAY RESULT
# =========================================================

if st.session_state.result:

    result = st.session_state.result

    first = st.session_state.first_name
    last = st.session_state.last_name

    safe_first = html.escape(first.upper())
    safe_last = html.escape(last.upper())

    safe_aura = html.escape(result["aura"])
    safe_element = html.escape(result["element"])
    safe_message = html.escape(result["message"])

    magic_number = result["magic_number"]
    power_number = result["power_number"]

    aura_icon = result["aura_icon"]
    element_icon = result["element_icon"]

    result_html = f"""

<div class="symbol-label">
    ✦ YOUR MACCO MAGIC SYMBOL ✦
</div>

<div class="reveal-text">
    Your unique MACCO identity has been revealed.
</div>


<div class="stage">

    <div class="triangle"></div>
    <div class="triangle-inner"></div>


    <div class="sparkle spark1">
        ✨
    </div>

    <div class="sparkle spark2">
        ✨
    </div>

    <div class="sparkle spark3">
        ✦
    </div>

    <div class="sparkle spark4">
        ✦
    </div>

    <div class="sparkle spark5">
        ⭐
    </div>

    <div class="sparkle spark6">
        ⭐
    </div>


    <div class="butterfly butterfly1">
        🦋
    </div>

    <div class="butterfly butterfly2">
        🦋
    </div>


    <div class="flower flower1">
        🌸
    </div>

    <div class="flower flower2">
        🌺
    </div>

    <div class="flower flower3">
        🌼
    </div>

    <div class="flower flower4">
        🌷
    </div>

    <div class="flower flower5">
        🌹
    </div>

    <div class="flower flower6">
        🌻
    </div>


    <div class="triangle-content">

        <div class="crown">
            👑
        </div>

        <div class="magic-number">
            {magic_number}
        </div>

        <div class="name-wrap">

            <div class="first-name">
                {safe_first}
            </div>

            <div class="last-name">
                {safe_last}
            </div>

        </div>

    </div>


    <div class="platform"></div>

</div>


<div class="magic-card">

    <div class="card-title">
        ✨ YOUR MACCO PROFILE ✨
    </div>


    <div class="stats-grid">

        <div class="stat">

            <div class="stat-icon">
                ⚡
            </div>

            <div class="stat-value">
                {power_number}
            </div>

            <div class="stat-label">
                POWER NUMBER
            </div>

        </div>


        <div class="stat">

            <div class="stat-icon">
                {aura_icon}
            </div>

            <div class="stat-value">
                {safe_aura}
            </div>

            <div class="stat-label">
                MACCO AURA
            </div>

        </div>


        <div class="stat">

            <div class="stat-icon">
                {element_icon}
            </div>

            <div class="stat-value">
                {safe_element}
            </div>

            <div class="stat-label">
                ELEMENT
            </div>

        </div>

    </div>


    <div class="explanation">
        {safe_message}
    </div>

</div>


<div class="message">
    ✨ YOU ARE UNIQUE • YOU ARE COLOR • YOU ARE MAGIC ✨
</div>

"""

    st.markdown(
        result_html,
        unsafe_allow_html=True,
    )


    # =====================================================
    # VOICE READING
    # =====================================================

    speak_macco_result(
        first_name=first,
        last_name=last,
        magic_number=magic_number,
        power_number=power_number,
        aura=result["aura"],
        element=result["element"],
        message=result["message"],
        reveal_id=st.session_state.reveal_id,
    )

    st.markdown(
        """
<div class="voice-note">
    🔊 MACCO will welcome you and explain your reading.
    If your browser blocks automatic audio, tap
    <b>Hear My MACCO Reading</b>.
</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">

    🌸 ✨ 🦋 ✨ 🌺

    <br><br>

    Powered by <b>MACCO</b> ✨

    <br>

    <span style="font-size:11px;">
        Every name carries its own MACCO sparkle.
    </span>

</div>
""",
    unsafe_allow_html=True,
)
