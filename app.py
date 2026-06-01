import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from openai import OpenAI

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Ruang Pena",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS — Clean Dark Minimalist
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=DM+Serif+Display:ital@0;1&display=swap');

:root {
    --bg:          #0f0f0f;
    --surface:     #161616;
    --surface2:    #1e1e1e;
    --border:      #2a2a2a;
    --border2:     #333333;
    --text:        #f0f0f0;
    --text-muted:  #888888;
    --text-faint:  #444444;
    --accent:      #e8ff47;
    --accent-dim:  rgba(232,255,71,.12);
    --accent-glow: rgba(232,255,71,.06);
    --user-bg:     #1e1e1e;
    --ai-bg:       #161616;
    --radius:      10px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 780px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stSidebar"] .stRadio > label {
    display: none;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 2px;
    display: flex;
    flex-direction: column;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: .92rem !important;
    font-weight: 400 !important;
    letter-spacing: .01em;
    padding: .55rem .75rem !important;
    border-radius: 6px !important;
    transition: background .15s, color .15s;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--surface2) !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] div {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    width: 10px !important;
    height: 10px !important;
}

/* ── Sidebar logo area ── */
.sb-logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.45rem;
    color: var(--text);
    margin-bottom: .15rem;
    letter-spacing: -.02em;
}
.sb-logo span { color: var(--accent); }
.sb-tagline {
    font-size: .78rem;
    color: var(--text-muted);
    margin-bottom: 1.8rem;
    letter-spacing: .03em;
}
.sb-section-label {
    font-size: .68rem;
    text-transform: uppercase;
    letter-spacing: .12em;
    color: var(--text-faint);
    margin-bottom: .6rem;
    margin-top: 1.4rem;
}
.sb-desc {
    font-size: .82rem;
    color: var(--text-muted);
    line-height: 1.55;
    padding: .7rem .8rem;
    background: var(--surface2);
    border-radius: 6px;
    border-left: 2px solid var(--accent);
    margin-top: .8rem;
}
.sb-footer {
    font-size: .72rem;
    color: var(--text-faint);
    margin-top: 2.5rem;
    text-align: center;
    line-height: 1.6;
}

/* ── Main title ── */
.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    letter-spacing: -.03em;
    color: var(--text);
    margin-bottom: .2rem;
    line-height: 1.1;
}
.page-title span { color: var(--accent); }
.page-sub {
    font-size: .88rem;
    color: var(--text-muted);
    margin-bottom: 1.6rem;
    letter-spacing: .01em;
}
.mode-pill {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    font-size: .75rem;
    font-weight: 500;
    letter-spacing: .06em;
    text-transform: uppercase;
    padding: .28rem .75rem;
    border-radius: 100px;
    background: var(--accent-dim);
    color: var(--accent);
    border: 1px solid rgba(232,255,71,.25);
    margin-bottom: 1.4rem;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: .3rem 0 !important;
    gap: .8rem !important;
}

/* user bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p {
    background: var(--user-bg);
    border: 1px solid var(--border2);
    padding: .75rem 1rem;
    border-radius: var(--radius);
    font-size: .95rem;
    line-height: 1.65;
    display: inline-block;
    max-width: 88%;
    color: var(--text);
}

/* assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: var(--ai-bg);
    border: 1px solid var(--border);
    border-left: 2px solid var(--accent);
    padding: .85rem 1.1rem;
    border-radius: var(--radius);
    font-size: .95rem;
    line-height: 1.7;
    color: var(--text);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p {
    margin-bottom: .5rem;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown strong {
    color: var(--accent);
    font-weight: 500;
}

/* avatars */
[data-testid="chatAvatarIcon-user"] {
    background: var(--surface2) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border2) !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: var(--accent-dim) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(232,255,71,.3) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius) !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'DM Sans', sans-serif !important;
    font-size: .93rem !important;
    color: var(--text) !important;
    background: transparent !important;
    caret-color: var(--accent) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-faint) !important;
}

/* ── Buttons ── */
.stButton button {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--text-muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .82rem !important;
    font-weight: 400 !important;
    border-radius: 6px !important;
    letter-spacing: .02em !important;
    transition: all .18s !important;
    padding: .35rem .9rem !important;
}
.stButton button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-dim) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-muted) !important;
    font-size: .85rem !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Error / info ── */
.stAlert {
    background: var(--surface2) !important;
    border-color: var(--border2) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .88rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* ── Caption ── */
.stImage + p, .caption {
    font-size: .75rem !important;
    color: var(--text-faint) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  API INIT
# ─────────────────────────────────────────────
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    st.error("API Key tidak ditemukan. Tambahkan OPENAI_API_KEY di Streamlit Secrets.")
    st.stop()


# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────
MODES = {
    "✒️  Asisten Umum": {
        "desc": "Teman diskusi serba-bisa untuk penulisan dan sastra.",
        "placeholder": "Apa yang ingin kamu tulis hari ini?",
        "prompt": (
            "Kamu adalah asisten penulis sastra yang cerdas dan hangat. "
            "Bantu pengguna dengan pertanyaan seputar penulisan kreatif, tata bahasa, "
            "gaya bercerita, atau obrolan santai tentang dunia sastra. "
            "Gunakan bahasa yang natural, lugas, dan menginspirasi."
        ),
    },
    "🌀  Pemicu Plot Twist": {
        "desc": "Deblokirkan alur ceritamu dengan twist yang segar.",
        "placeholder": "Ceritakan premis atau situasi cerita yang sedang buntu...",
        "prompt": (
            "Kamu adalah Story Doctor — ahli bedah alur cerita. "
            "Berikan tepat 3 plot twist yang segar, tak terduga, dan bebas klise. "
            "Untuk setiap twist, jelaskan singkat mengapa ia menggerakkan emosi pembaca lebih dalam."
        ),
    },
    "🌹  Generator Metafora": {
        "desc": "Ubah kalimat biasa menjadi bahasa yang puitis.",
        "placeholder": "Ketik kalimat yang ingin diubah menjadi lebih puitis...",
        "prompt": (
            "Kamu adalah penyair berbakat. Ubah kalimat biasa yang diberikan pengguna "
            "menjadi 3–4 variasi kalimat puitis yang kaya majas: metafora, personifikasi, simile. "
            "Jelaskan nuansa emosi setiap variasi secara singkat."
        ),
    },
    "🎭  Wawancara Karakter": {
        "desc": "Hidupkan karaktermu lewat sesi roleplay interaktif.",
        "placeholder": "Deskripsikan karaktermu, lalu mulai bertanya...",
        "prompt": (
            "Kamu melakukan ROLEPLAY sebagai karakter fiksi yang dibuat pengguna. "
            "Jika belum ada deskripsi karakter, minta dulu. "
            "Jawab semua pertanyaan sebagai karakter tersebut dari sudut pandang orang pertama. "
            "Ekspresikan kepribadian dan keunikan karakter lewat gaya bicara."
        ),
    },
    "🖼️  Generator Ilustrasi": {
        "desc": "Visualisasikan adegan ceritamu dengan DALL-E 3.",
        "placeholder": "Gambarkan suasana atau adegan yang ingin divisualisasikan...",
        "prompt": None,
    },
}


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def get_chat_response(user_input, history, system_prompt):
    messages = [SystemMessage(content=system_prompt)]
    for msg in history[-10:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant" and not msg.get("is_image"):
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_input))
    return llm.invoke(messages).content


def get_image_url(prompt):
    try:
        resp = client.images.generate(
            model="dall-e-3",
            prompt=f"Cinematic, painterly illustration for a literary story. Clean composition, moody atmosphere. {prompt}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return resp.data[0].url
    except Exception as e:
        return f"ERROR:{e}"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-logo">Ruang<span>.</span>Pena</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tagline">Asisten sastra & penulisan kreatif</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">Mode</div>', unsafe_allow_html=True)
    mode = st.radio("", list(MODES.keys()), label_visibility="collapsed")

    st.markdown(
        f'<div class="sb-desc">{MODES[mode]["desc"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Bersihkan percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sb-footer">Dibuat dengan ♡ untuk para penulis</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode
    st.rerun()


# ─────────────────────────────────────────────
#  MAIN HEADER
# ─────────────────────────────────────────────
st.markdown(
    '<div class="page-title">Ruang<span>.</span>Pena</div>'
    '<div class="page-sub">Di sinilah kata-kata menemukan bentuknya</div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="mode-pill">{mode.strip()}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CHAT HISTORY
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("is_image"):
            st.image(msg["content"], use_column_width=True)
        else:
            st.markdown(msg["content"])


# ─────────────────────────────────────────────
#  INPUT & RESPONSE
# ─────────────────────────────────────────────
if user_input := st.chat_input(MODES[mode]["placeholder"]):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if mode == "🖼️  Generator Ilustrasi":
            with st.spinner("Membuat ilustrasi..."):
                url = get_image_url(user_input)
                if url.startswith("ERROR:"):
                    st.error(f"Gagal membuat gambar: {url[6:]}")
                else:
                    st.image(url, use_column_width=True)
                    st.caption("Ilustrasi oleh DALL-E 3")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": url, "is_image": True}
                    )
        else:
            with st.spinner("Sedang menulis..."):
                reply = get_chat_response(
                    user_input,
                    st.session_state.messages,
                    MODES[mode]["prompt"],
                )
                st.markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply, "is_image": False}
                )
