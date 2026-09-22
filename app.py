import streamlit as st
import hashlib
import html
import json
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MACCO Magic Number",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "macco_result" not in st.session_state:
    st.session_state.macco_result = None

if "macco_first" not in st.session_state:
    st.session_state.macco_first = ""

if "macco_last" not in st.session_state:
    st.session_state.macco_last = ""

if "reveal_id" not in st.session_state:
    st.session_state.reveal_id = 0


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ------------------------------------------------------------
   GLOBAL
------------------------------------------------------------ */

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 15%, rgba(255,0,190,.18), transparent 24%),
        radial-gradient(circle at 90% 18%, rgba(0,190,255,.18), transparent 25%),
        radial-gradient(circle at 50% 80%, rgba(125,45,255,.16), transparent 32%),
        linear-gradient(145deg, #03050d, #08091c, #120725, #05040d);

    color: white;
    overflow-x: hidden;
}

.block-container {
    max-width: 760px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}


/* ------------------------------------------------------------
   HIDE STREAMLIT CLUTTER
------------------------------------------------------------ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ------------------------------------------------------------
   AMBIENT BACKGROUND
------------------------------------------------------------ */

.macco-orb {
    position: fixed;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    opacity: .28;
    filter: blur(8px);
}

.macco-orb-one {
    width: 95px;
    height: 95px;
    left: 5%;
    top: 22%;
    background: #ff32c8;
    box-shadow: 0 0 70px #ff32c8;
    animation: floatOne 7s ease-in-out infinite alternate;
}

.macco-orb-two {
    width: 80px;
    height: 80px;
    right: 6%;
    top: 38%;
    background: #39d9ff;
    box-shadow: 0 0 70px #39d9ff;
    animation: floatTwo 8s ease-in-out infinite alternate;
}

.macco-orb-three {
    width: 65px;
    height: 65px;
    left: 17%;
    bottom: 12%;
    background: #ffd84c;
    box-shadow: 0 0 65px #ffd84c;
    animation: floatOne 9s ease-in-out infinite alternate;
}

@keyframes floatOne {
    from {
        transform: translateY(-8px) scale(.9);
    }

    to {
        transform: translateY(25px) scale(1.12);
    }
}

@keyframes floatTwo {
    from {
        transform: translateY(20px) scale(1);
    }

    to {
        transform: translateY(-20px) scale(1.15);
    }
}


/* ------------------------------------------------------------
   HEADER
------------------------------------------------------------ */

.macco-top {
    text-align: center;
    font-size: 22px;
    letter-spacing: 9px;
    margin-bottom: 10px;
    animation: twinkleTop 1.6s infinite alternate;
}

@keyframes twinkleTop {
    from {
        opacity: .55;
    }

    to {
        opacity: 1;
    }
}


/* ------------------------------------------------------------
   MAGIC ORB
------------------------------------------------------------ */

.magic-orb-wrap {
    width: 118px;
    height: 118px;
    position: relative;
    margin: 0 auto 8px auto;
}

.magic-orb-ring {
    position: absolute;
    inset: -7px;

    border-radius: 50%;

    border: 2px solid rgba(255,220,100,.35);

    box-shadow:
        0 0 18px rgba(255,65,210,.65),
        0 0 38px rgba(55,215,255,.55);

    animation: ringSpin 7s linear infinite;
}

@keyframes ringSpin {
    to {
        transform: rotate(360deg);
    }
}

.magic-orb {
    position: absolute;

    width: 100px;
    height: 100px;

    top: 9px;
    left: 9px;

    border-radius: 50%;

    background:
        repeating-linear-gradient(
            45deg,
            rgba(255,255,255,.22) 0px,
            rgba(255,255,255,.22) 5px,
            rgba(0,0,0,.05) 5px,
            rgba(0,0,0,.05) 10px
        ),
        linear-gradient(
            135deg,
            #35d9ff,
            #a747ff,
            #ff45c7,
            #ffdc5a
        );

    box-shadow:
        0 0 20px #a53cff,
        0 0 38px #35d9ff,
        0 0 55px rgba(255,75,220,.45);

    animation: orbPulse 1.8s infinite alternate;
}

@keyframes orbPulse {
    from {
        transform: scale(1);
        filter: brightness(1);
    }

    to {
        transform: scale(1.05);
        filter: brightness(1.25);
    }
}


/* ------------------------------------------------------------
   BRAND
------------------------------------------------------------ */

.macco-brand {
    text-align: center;

    font-size: 32px;
    font-weight: 900;

    letter-spacing: 11px;

    margin-top: 10px;

    background:
        linear-gradient(
            90deg,
            #fff5ad,
            #ffd452,
            #ffad16,
            #fff5ad
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0 0 15px rgba(255,200,60,.25);
}

.macco-title {
    text-align: center;

    font-size: 45px;
    line-height: 1.08;

    font-weight: 900;

    margin-top: 12px;

    background:
        linear-gradient(
            90deg,
            #ff4fc8,
            #ffd95a,
            #48d9ff,
            #a764ff,
            #ff4fc8
        );

    background-size: 300% auto;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: titleMove 5s linear infinite;
}

@keyframes titleMove {
    to {
        background-position: 300% center;
    }
}

.macco-subtitle {
    text-align: center;

    color: #d8dcec;

    max-width: 570px;

    margin: 14px auto 30px auto;

    line-height: 1.6;

    font-size: 16px;
}


/* ------------------------------------------------------------
   INPUTS
------------------------------------------------------------ */

label[data-testid="stWidgetLabel"] p {
    color: #ffd75d !important;
    font-weight: 800 !important;
    letter-spacing: .7px;
}

div[data-testid="stTextInput"] input {
    height: 55px;

    border-radius: 16px;

    font-size: 17px;

    color: white;

    background: rgba(8,10,25,.94);

    border: 1px solid rgba(255,215,90,.48);

    box-shadow:
        inset 0 0 8px rgba(255,255,255,.02),
        0 0 14px rgba(155,70,255,.07);
}

div[data-testid="stTextInput"] input:focus {
    border: 1px solid #ffd75d;

    box-shadow:
        0 0 15px rgba(255,215,90,.22);
}


/* ------------------------------------------------------------
   MAIN BUTTON
------------------------------------------------------------ */

div.stButton > button {
    width: 100%;

    height: 59px;

    margin-top: 8px;

    border-radius: 17px;

    border: 1px solid #ffe996;

    color: #171009;

    font-size: 18px;

    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #ffb51d,
            #ffe676,
            #ffbd27
        );

    box-shadow:
        0 0 13px rgba(255,205,55,.55);

    transition:
        transform .2s ease,
        box-shadow .2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 0 20px rgba(255,220,80,.75);
}


/* ------------------------------------------------------------
   RESULT
------------------------------------------------------------ */

.result-heading {
    margin-top: 40px;

    text-align: center;

    color: #ffd95e;

    font-size: 14px;

    font-weight: 900;

    letter-spacing: 3px;
}

.result-subheading {
    text-align: center;

    color: #d5d9e9;

    font-size: 13px;

    margin-top: 7px;
}


/* ------------------------------------------------------------
   MAGIC SYMBOL CARD
------------------------------------------------------------ */

.magic-stage {
    width: 100%;
    max-width: 520px;

    min-height: 430px;

    margin: 20px auto 18px auto;

    position: relative;

    overflow: hidden;

    border-radius: 32px;

    background:
        radial-gradient(
            circle at center,
            rgba(255,190,30,.09),
            transparent 43%
        ),
        linear-gradient(
            145deg,
            rgba(20,12,45,.86),
            rgba(5,8,25,.94)
        );

    border: 1px solid rgba(255,215,90,.25);

    box-shadow:
        0 0 30px rgba(150,60,255,.14),
        inset 0 0 45px rgba(255,255,255,.02);
}


/* ------------------------------------------------------------
   TRIANGLE
------------------------------------------------------------ */

.magic-triangle {
    position: absolute;

    left: 50%;
    top: 40px;

    transform: translateX(-50%);

    width: 0;
    height: 0;

    border-left: 185px solid transparent;
    border-right: 185px solid transparent;

    border-bottom: 330px solid #eeb72c;

    filter:
        drop-shadow(0 0 8px rgba(255,215,70,.9))
        drop-shadow(0 0 24px rgba(255,160,20,.42));

    animation: trianglePulse 1.8s infinite alternate;
}

.magic-triangle-inner {
    position: absolute;

    left: 50%;
    top: 62px;

    transform: translateX(-50%);

    width: 0;
    height: 0;

    border-left: 161px solid transparent;
    border-right: 161px solid transparent;

    border-bottom: 288px solid #090a1d;
}

@keyframes trianglePulse {
    from {
        filter:
            drop-shadow(0 0 7px rgba(255,215,70,.75))
            drop-shadow(0 0 18px rgba(255,160,20,.30));
    }

    to {
        filter:
            drop-shadow(0 0 13px rgba(255,235,140,1))
            drop-shadow(0 0 30px rgba(255,160,20,.55));
    }
}


/* ------------------------------------------------------------
   RESULT CONTENT
------------------------------------------------------------ */

.result-content {
    position: absolute;

    top: 91px;
    left: 0;

    width: 100%;

    text-align: center;

    z-index: 10;
}

.result-crown {
    font-size: 35px;

    animation: crownMove 1.8s ease-in-out infinite alternate;
}

@keyframes crownMove {
    to {
        transform: translateY(-5px);
    }
}

.result-number {
    font-size: 105px;

    font-weight: 900;

    line-height: 1;

    margin-top: 2px;

    background:
        linear-gradient(
            180deg,
            #fffbc7,
            #ffe15b,
            #ffae00
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    filter:
        drop-shadow(0 0 10px rgba(255,205,50,.32));

    animation: numberPulse 1.5s infinite alternate;
}

@keyframes numberPulse {
    to {
        transform: scale(1.045);
    }
}

.result-name {
    margin-top: 20px;

    font-size: 27px;

    font-weight: 900;

    letter-spacing: 2px;

    line-height: 1.3;
}

.result-first {
    color: #4bdcff;

    text-shadow:
        0 0 13px rgba(75,220,255,.45);
}

.result-last {
    color: #ff55cf;

    text-shadow:
        0 0 13px rgba(255,85,207,.45);
}


/* ------------------------------------------------------------
   CLEAN DECORATIONS
------------------------------------------------------------ */

.deco {
    position: absolute;

    z-index: 20;

    user-select: none;

    animation: decoFloat 2.4s ease-in-out infinite alternate;
}

@keyframes decoFloat {
    from {
        transform: translateY(4px) scale(.95);
    }

    to {
        transform: translateY(-7px) scale(1.05);
    }
}

.deco-one {
    top: 70px;
    left: 42px;
    font-size: 25px;
}

.deco-two {
    top: 80px;
    right: 42px;
    font-size: 25px;
}

.deco-three {
    bottom: 42px;
    left: 50px;
    font-size: 36px;
}

.deco-four {
    bottom: 42px;
    right: 50px;
    font-size: 36px;
}

.deco-five {
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 26px;
}


/* ------------------------------------------------------------
   PROFILE CARD
------------------------------------------------------------ */

.profile-card {
    max-width: 620px;

    margin: 10px auto 20px auto;

    padding: 24px;

    border-radius: 25px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.075),
            rgba(255,255,255,.025)
        );

    border:
        1px solid rgba(255,215,90,.26);

    box-shadow:
        0 0 25px rgba(145,70,255,.10);
}

.profile-title {
    text-align: center;

    color: #ffd85f;

    font-size: 19px;

    font-weight: 900;

    margin-bottom: 18px;
}

.profile-grid {
    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 10px;
}

.profile-item {
    text-align: center;

    padding: 16px 7px;

    border-radius: 16px;

    background:
        rgba(6,8,24,.75);

    border:
        1px solid rgba(255,255,255,.08);
}

.profile-icon {
    font-size: 27px;
}

.profile-value {
    color: white;

    font-size: 17px;

    font-weight: 900;

    margin-top: 5px;
}

.profile-label {
    color: #9fa8c6;

    font-size: 10px;

    letter-spacing: .9px;

    margin-top: 5px;
}

.profile-message {
    color: #e7e8f2;

    text-align: center;

    font-size: 15px;

    line-height: 1.65;

    margin-top: 20px;
}

.final-message {
    text-align: center;

    font-weight: 900;

    font-size: 17px;

    margin: 18px auto;

    background:
        linear-gradient(
            90deg,
            #ffd95b,
            #ff55d0,
            #4bdcff
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


/* ------------------------------------------------------------
   VOICE NOTE
------------------------------------------------------------ */

.voice-note {
    text-align: center;

    color: #9da6c3;

    font-size: 12px;

    margin-top: 7px;
}


/* ------------------------------------------------------------
   FOOTER
------------------------------------------------------------ */

.macco-footer {
    text-align: center;

    color: #7f879f;

    margin-top: 40px;

    font-size: 12px;

    line-height: 1.7;
}


/* ------------------------------------------------------------
   MOBILE
------------------------------------------------------------ */

@media (max-width: 520px) {

    .block-container {
        padding-left: 13px;
        padding-right: 13px;
    }

    .macco-brand {
        font-size: 27px;
        letter-spacing: 8px;
    }

    .macco-title {
        font-size: 34px;
    }

    .macco-subtitle {
        font-size: 14px;
    }

    .magic-stage {
        min-height: 365px;
        border-radius: 25px;
    }

    .magic-triangle {
        top: 40px;

        border-left-width: 145px;
        border-right-width: 145px;

        border-bottom-width: 260px;
    }

    .magic-triangle-inner {
        top: 58px;

        border-left-width: 126px;
        border-right-width: 126px;

        border-bottom-width: 226px;
    }

    .result-content {
        top: 78px;
    }

    .result-crown {
        font-size: 29px;
    }

    .result-number {
        font-size: 78px;
    }

    .result-name {
        font-size: 20px;
        margin-top: 14px;
    }

    .deco-one {
        left: 18px;
    }

    .deco-two {
        right: 18px;
    }

    .deco-three {
        left: 22px;
        bottom: 30px;
        font-size: 30px;
    }

    .deco-four {
        right: 22px;
        bottom: 30px;
        font-size: 30px;
    }

    .profile-grid {
        grid-template-columns: 1fr;
    }

    .profile-card {
        padding: 18px;
    }
}

</style>

<div class="macco-orb macco-orb-one"></div>
<div class="macco-orb macco-orb-two"></div>
<div class="macco-orb macco-orb-three"></div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# MACCO DATA
# ============================================================

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
    "Your MACCO energy represents creativity, confidence, and the courage to express what makes you different.",
    "Your MACCO energy reflects warmth, imagination, and a naturally bright presence.",
    "Your MACCO profile carries an adventurous spirit that encourages discovery and new possibilities.",
    "Your energy represents growth, determination, and the ability to turn ideas into something meaningful.",
    "Your MACCO identity reflects curiosity, originality, and positive energy.",
    "Your profile carries a calm but powerful energy that can positively influence the people around you.",
    "Your MACCO energy reflects ambition, imagination, and confidence in following your own path.",
    "Your profile combines creativity and resilience, giving your MACCO identity a distinctive glow.",
    "Your MACCO energy represents joy, possibility, and the willingness to dream beyond the ordinary.",
]


# ============================================================
# MAGIC ENGINE
# ============================================================

def macco_magic(first_name, last_name):

    normalized_name = " ".join(
        f"{first_name.strip().lower()} {last_name.strip().lower()}".split()
    )

    digest = hashlib.sha256(
        normalized_name.encode("utf-8")
    ).digest()

    magic_number = (
        int.from_bytes(digest[0:4], "big")
        % 99
    ) + 1

    power_number = (
        digest[4] % 9
    ) + 1

    aura_name, aura_icon = AURAS[
        digest[5] % len(AURAS)
    ]

    element_name, element_icon = ELEMENTS[
        digest[6] % len(ELEMENTS)
    ]

    message = MESSAGES[
        digest[7] % len(MESSAGES)
    ]

    return {
        "magic_number": magic_number,
        "power_number": power_number,
        "aura": aura_name,
        "aura_icon": aura_icon,
        "element": element_name,
        "element_icon": element_icon,
        "message": message,
    }


# ============================================================
# VOICE
# ============================================================

def macco_voice(
    first_name,
    last_name,
    result,
    reveal_id,
):

    spoken_text = (
        f"Welcome {first_name} {last_name} to MACCO Magic. "
        f"I am your MACCO voice guide. "
        f"Your magic number is {result['magic_number']}. "
        f"Your power number is {result['power_number']}. "
        f"Your MACCO aura is {result['aura']}. "
        f"Your element is {result['element']}. "
        f"{result['message']} "
        f"{first_name}, your MACCO profile is unique to your name. "
        f"Keep shining, keep creating, and remember: "
        f"you are unique, you are color, and you are magic."
    )

    text_json = json.dumps(spoken_text)

    # reveal_id is included so a fresh component is generated
    # after each successful reveal.
    component_key = json.dumps(str(reveal_id))

    voice_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

html,
body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, Helvetica, sans-serif;
}}

.voice-card {{
    box-sizing: border-box;

    width: 100%;

    padding: 13px;

    text-align: center;

    border-radius: 16px;

    border:
        1px solid rgba(255,215,90,.30);

    background:
        linear-gradient(
            90deg,
            rgba(255,190,35,.10),
            rgba(255,70,200,.10),
            rgba(65,215,255,.10)
        );
}}

.voice-label {{
    color: #ffe47a;

    font-size: 12px;

    font-weight: 800;

    margin-bottom: 8px;
}}

.voice-button {{
    border:
        1px solid rgba(255,230,135,.75);

    border-radius: 13px;

    padding: 10px 18px;

    cursor: pointer;

    color: #171008;

    font-size: 14px;

    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #ffbb25,
            #ffe878
        );

    box-shadow:
        0 0 12px rgba(255,205,60,.25);
}}

.voice-button:hover {{
    transform: scale(1.02);
}}

</style>
</head>

<body>

<div class="voice-card">

    <div class="voice-label">
        🔊 MACCO VOICE
    </div>

    <button
        class="voice-button"
        onclick="speakMacco()"
    >
        🔊 Hear My Reading
    </button>

</div>

<script>

const maccoText = {text_json};
const revealID = {component_key};

function chooseVoice() {{

    const voices =
        window.speechSynthesis.getVoices();

    if (!voices || voices.length === 0) {{
        return null;
    }}

    const preferred = [
        "Microsoft Aria",
        "Microsoft Jenny",
        "Samantha",
        "Google US English",
        "Microsoft Zira",
        "Karen",
        "Moira"
    ];

    for (const wanted of preferred) {{

        const found =
            voices.find(
                voice =>
                    voice.name
                        .toLowerCase()
                        .includes(
                            wanted.toLowerCase()
                        )
            );

        if (found) {{
            return found;
        }}
    }}

    const englishVoice =
        voices.find(
            voice =>
                voice.lang &&
                voice.lang
                    .toLowerCase()
                    .startsWith("en")
        );

    return englishVoice || voices[0];
}}


function speakMacco() {{

    if (!("speechSynthesis" in window)) {{

        alert(
            "Voice is not supported on this browser."
        );

        return;
    }}

    window.speechSynthesis.cancel();

    const speech =
        new SpeechSynthesisUtterance(
            maccoText
        );

    const selectedVoice =
        chooseVoice();

    if (selectedVoice) {{
        speech.voice = selectedVoice;
    }}

    speech.lang = "en-US";

    speech.rate = 0.90;

    speech.pitch = 1.05;

    speech.volume = 1.0;

    window.speechSynthesis.speak(
        speech
    );
}}


function prepareVoices() {{

    window.speechSynthesis.getVoices();
}}


if ("speechSynthesis" in window) {{

    prepareVoices();

    window.speechSynthesis.onvoiceschanged =
        prepareVoices;

}}

</script>

</body>
</html>
"""

    components.html(
        voice_html,
        height=92,
        scrolling=False,
    )


# ============================================================
# HEADER
# ============================================================

header_html = """
<div class="macco-top">✦ ✨ ✦</div>
<div class="magic-orb-wrap">
    <div class="magic-orb-ring"></div>
    <div class="magic-orb"></div>
</div>
<div class="macco-brand">MACCO</div>
<div class="macco-title">YOUR MAGIC NUMBER</div>
<div class="macco-subtitle">
Enter your name and discover your personal MACCO number,
power number, aura and element.
</div>
"""

st.markdown(
    header_html,
    unsafe_allow_html=True,
)


# ============================================================
# INPUTS
# ============================================================

first_name = st.text_input(
    "✨ FIRST NAME",
    placeholder="Enter your first name",
)

last_name = st.text_input(
    "✨ LAST NAME",
    placeholder="Enter your last name",
)


# ============================================================
# REVEAL
# ============================================================

reveal_clicked = st.button(
    "✨ REVEAL MY MACCO MAGIC ✨",
    use_container_width=True,
)


if reveal_clicked:

    clean_first = first_name.strip()
    clean_last = last_name.strip()

    if not clean_first or not clean_last:

        st.warning(
            "Please enter both your first and last name."
        )

    else:

        st.session_state.macco_first = clean_first

        st.session_state.macco_last = clean_last

        st.session_state.macco_result = macco_magic(
            clean_first,
            clean_last,
        )

        st.session_state.reveal_id += 1

        st.balloons()


# ============================================================
# RESULT
# ============================================================

if st.session_state.macco_result is not None:

    result = st.session_state.macco_result

    first = st.session_state.macco_first
    last = st.session_state.macco_last

    safe_first = html.escape(
        first.upper()
    )

    safe_last = html.escape(
        last.upper()
    )

    safe_aura = html.escape(
        result["aura"]
    )

    safe_element = html.escape(
        result["element"]
    )

    safe_message = html.escape(
        result["message"]
    )

    magic_number = result[
        "magic_number"
    ]

    power_number = result[
        "power_number"
    ]

    aura_icon = result[
        "aura_icon"
    ]

    element_icon = result[
        "element_icon"
    ]


    # ========================================================
    # IMPORTANT:
    # HTML is intentionally compact and left aligned.
    # This prevents Streamlit/Markdown from showing HTML
    # tags as code on the screen.
    # ========================================================

    result_html = (
        f'<div class="result-heading">✦ YOUR MACCO MAGIC ✦</div>'
        f'<div class="result-subheading">Your unique MACCO identity has been revealed.</div>'

        f'<div class="magic-stage">'

        f'<div class="magic-triangle"></div>'
        f'<div class="magic-triangle-inner"></div>'

        f'<div class="deco deco-one">✨</div>'
        f'<div class="deco deco-two">✨</div>'
        f'<div class="deco deco-three">🌸</div>'
        f'<div class="deco deco-four">🌺</div>'
        f'<div class="deco deco-five">✦</div>'

        f'<div class="result-content">'

        f'<div class="result-crown">👑</div>'

        f'<div class="result-number">'
        f'{magic_number}'
        f'</div>'

        f'<div class="result-name">'

        f'<div class="result-first">'
        f'{safe_first}'
        f'</div>'

        f'<div class="result-last">'
        f'{safe_last}'
        f'</div>'

        f'</div>'

        f'</div>'

        f'</div>'

        f'<div class="profile-card">'

        f'<div class="profile-title">'
        f'✨ YOUR MACCO PROFILE ✨'
        f'</div>'

        f'<div class="profile-grid">'

        f'<div class="profile-item">'
        f'<div class="profile-icon">⚡</div>'
        f'<div class="profile-value">{power_number}</div>'
        f'<div class="profile-label">POWER NUMBER</div>'
        f'</div>'

        f'<div class="profile-item">'
        f'<div class="profile-icon">{aura_icon}</div>'
        f'<div class="profile-value">{safe_aura}</div>'
        f'<div class="profile-label">AURA</div>'
        f'</div>'

        f'<div class="profile-item">'
        f'<div class="profile-icon">{element_icon}</div>'
        f'<div class="profile-value">{safe_element}</div>'
        f'<div class="profile-label">ELEMENT</div>'
        f'</div>'

        f'</div>'

        f'<div class="profile-message">'
        f'{safe_message}'
        f'</div>'

        f'</div>'

        f'<div class="final-message">'
        f'✨ YOU ARE UNIQUE • YOU ARE COLOR • YOU ARE MAGIC ✨'
        f'</div>'
    )


    st.markdown(
        result_html,
        unsafe_allow_html=True,
    )


    # ========================================================
    # VOICE
    # ========================================================

    macco_voice(
        first_name=first,
        last_name=last,
        result=result,
        reveal_id=st.session_state.reveal_id,
    )


    st.markdown(
        '<div class="voice-note">'
        'Tap the voice button to hear MACCO welcome you '
        'and explain your result.'
        '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================

footer_html = (
    '<div class="macco-footer">'
    '✨ 🌸 ✨<br>'
    '<b>Powered by MACCO</b><br>'
    'Every name carries its own sparkle.'
    '</div>'
)

st.markdown(
    footer_html,
    unsafe_allow_html=True,
)
