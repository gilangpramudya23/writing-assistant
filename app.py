import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from openai import OpenAI

# ──────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────
st.set_page_config(
    page_title="writespace",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0d0d0d;
    color: #e8e4dc;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="collapsedControl"] { display: none; }

/* Main container */
.main .block-container {
    max-width: 860px;
    padding: 3rem 2rem 6rem 2rem;
    margin: 0 auto;
}

/* ── Wordmark / Header ── */
.wordmark {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    letter-spacing: -0.03em;
    color: #e8e4dc;
    margin-bottom: 0.25rem;
}

.tagline {
    font-size: 0.72rem;
    color: #555;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Mode Selector ── */
.mode-label {
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 0.75rem;
}

div[data-testid="stHorizontalBlock"] { gap: 0.5rem; }

/* Mode buttons via radio */
div[data-testid="stRadio"] > label { display: none; }

div[data-testid="stRadio"] > div {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

div[data-testid="stRadio"] > div > label {
    display: inline-flex !important;
    align-items: center;
    border: 1px solid #222;
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: all 0.15s ease;
    background: transparent;
    color: #888;
    white-space: nowrap;
}

div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #e8e4dc;
    color: #0d0d0d;
    border-color: #e8e4dc;
    font-weight: 500;
}

div[data-testid="stRadio"] > div > label:hover {
    border-color: #444;
    color: #ccc;
}

div[data-testid="stRadio"] > div > label input { display: none; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stChatMessage"] + [data-testid="stChatMessage"] {
    margin-top: 1.5rem;
}

/* Hide default avatar */
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p {
    background: #1a1a1a;
    border: 1px solid #222;
    border-radius: 16px 16px 4px 16px;
    padding: 0.75rem 1rem !important;
    font-size: 0.875rem;
    line-height: 1.6;
    color: #e8e4dc;
    display: inline-block;
    max-width: 80%;
    float: right;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p,
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p {
    font-size: 0.875rem;
    line-height: 1.75;
    color: #c9c4bc;
}

/* Divider between sections */
.section-divider {
    border: none;
    border-top: 1px solid #1a1a1a;
    margin: 1.75rem 0;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: min(860px, 100vw);
    padding: 1rem 2rem 1.5rem;
    background: #0d0d0d;
    border-top: 1px solid #181818;
    z-index: 100;
}

[data-testid="stChatInputTextArea"] {
    background: #131313 !important;
    border: 1px solid #252525 !important;
    border-radius: 12px !important;
    color: #e8e4dc !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.15s ease;
}

[data-testid="stChatInputTextArea"]:focus {
    border-color: #444 !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: #e8e4dc !important;
    border-radius: 8px !important;
    color: #0d0d0d !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-size: 0.75rem;
    color: #555;
    letter-spacing: 0.06em;
}

/* ── Image ── */
[data-testid="stImage"] img {
    border-radius: 12px;
    border: 1px solid #1e1e1e;
    max-width: 100%;
}

/* ── Error/Info boxes ── */
[data-testid="stAlert"] {
    background: #141414 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    font-size: 0.8rem;
    color: #888 !important;
}

/* ── Mode badge in chat ── */
.mode-badge {
    display: inline-block;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #444;
    border: 1px solid #1e1e1e;
    border-radius: 999px;
    padding: 0.2rem 0.65rem;
    margin-bottom: 1.5rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────
# API SETUP
# ──────────────────────────────────────────
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    st.error("OpenAI API Key not found in secrets.")
    st.stop()


# ──────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────
def get_chatbot_response(user_input, history_messages, system_prompt):
    messages = [SystemMessage(content=system_prompt)]
    for msg in history_messages[-10:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant" and not msg.get("is_image", False):
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_input))
    response = llm.invoke(messages)
    return response.content


def get_image_response(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"A highly artistic and atmospheric illustration for a literature book. {prompt}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        return f"Terjadi kesalahan saat membuat gambar: {e}"


# ──────────────────────────────────────────
# SYSTEM PROMPTS
# ──────────────────────────────────────────
prompts = {
    "umum": """Kamu adalah asisten penulis sastra yang ramah. Bantu pengguna dengan pertanyaan umum seputar penulisan, tata bahasa, atau tips menulis santai.""",
    "plot": """Kamu adalah ahli bedah cerita (Story Doctor). Pengguna akan memberikan premis atau situasi cerita yang sedang buntu. 
    Tugasmu adalah memberikan 3 ide 'plot twist' atau belokan alur yang tidak terduga, segar, dan menghindari klise. 
    Jelaskan juga mengapa twist tersebut bisa membuat cerita lebih menarik secara emosional.""",
    "metafora": """Kamu adalah seorang penyair berbakat. Pengguna akan memberikan kalimat datar atau biasa.
    Tugasmu adalah mengubah kalimat tersebut menjadi 3-4 variasi kalimat yang sangat puitis, kaya akan majas (metafora, personifikasi), 
    dan memiliki rima yang indah. Jelaskan nuansa emosi dari masing-masing variasi tersebut.""",
    "karakter": """Kamu sekarang sedang melakukan ROLEPLAY. Pengguna akan mewawancarai karakter yang sedang mereka ciptakan.
    Berdasarkan deskripsi awal yang diberikan pengguna (atau tanya mereka jika belum jelas), JAWABLAH SEMUA PERTANYAAN SEBAGAI KARAKTER TERSEBUT.
    Gunakan sudut pandang orang pertama ("Aku/Saya"). Tunjukkan kepribadian, trauma, atau keunikan karakter melalui gaya bicaramu.""",
}

mode_labels = {
    "umum":      "✦ asisten umum",
    "plot":      "◎ plot twist",
    "metafora":  "〜 metafora",
    "karakter":  "◈ wawancara karakter",
    "ilustrasi": "⬡ ilustrasi",
}

placeholder_map = {
    "umum":      "tanya apa aja soal nulis...",
    "plot":      "ceritain premis atau scene yang lagi buntu...",
    "metafora":  "ketik kalimat yang mau diubah jadi puitis...",
    "karakter":  "tanya sesuatu ke karaktermu...",
    "ilustrasi": "deskripsiin suasana atau adegan yang mau divisualisasikan...",
}


# ──────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "umum"


# ──────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────
st.markdown('<div class="wordmark">writespace</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">your literary co-pilot</div>', unsafe_allow_html=True)

# ── Mode selector ──
st.markdown('<div class="mode-label">mode</div>', unsafe_allow_html=True)

mode = st.radio(
    "mode",
    options=list(mode_labels.keys()),
    format_func=lambda x: mode_labels[x],
    horizontal=True,
    label_visibility="collapsed",
)

# Reset chat when mode changes
if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode
    st.rerun()

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── Current mode badge ──
st.markdown(f'<span class="mode-badge">{mode_labels[mode]}</span>', unsafe_allow_html=True)


# ──────────────────────────────────────────
# CHAT HISTORY
# ──────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message.get("is_image", False):
            st.image(message["content"])
        else:
            st.markdown(message["content"])


# ──────────────────────────────────────────
# CHAT INPUT
# ──────────────────────────────────────────
if prompt := st.chat_input(placeholder_map[mode]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if mode == "ilustrasi":
            with st.spinner("generating..."):
                image_url = get_image_response(prompt)
                if image_url.startswith("http"):
                    st.image(image_url)
                    st.session_state.messages.append({"role": "assistant", "content": image_url, "is_image": True})
                else:
                    st.error(image_url)
        else:
            with st.spinner("thinking..."):
                answer = get_chatbot_response(prompt, st.session_state.messages, prompts[mode])
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer, "is_image": False})
