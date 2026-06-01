import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from openai import OpenAI

st.set_page_config(
    page_title="Ruang Pena",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Styrene+A+LC:wght@400;500&family=Tiempos+Text:ital,wght@0,400;1,400&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600&family=Lora:ital,wght@0,400;1,400&display=swap');

:root {
    --bg:           #f5f0eb;
    --bg2:          #ede8e2;
    --surface:      #ffffff;
    --border:       #e0d9d0;
    --border2:      #ccc5ba;
    --text:         #1a1612;
    --text-muted:   #7a7068;
    --text-faint:   #b0a89e;
    --accent:       #c96e3f;
    --accent-soft:  rgba(201,110,63,.1);
    --sidebar-bg:   #faf7f4;
    --radius-lg:    16px;
    --radius-md:    10px;
    --radius-sm:    6px;
    --shadow-sm:    0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    --shadow-md:    0 4px 16px rgba(0,0,0,.08);
}

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 720px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stSidebar"] .stRadio > label { display: none; }

[data-testid="stSidebar"] .stRadio label {
    font-size: .875rem !important;
    font-weight: 400 !important;
    color: var(--text-muted) !important;
    padding: .5rem .65rem !important;
    border-radius: var(--radius-sm) !important;
    transition: background .15s, color .15s !important;
    line-height: 1.4 !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg2) !important;
    color: var(--text) !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] div {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

.sb-brand {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text) !important;
    letter-spacing: -.02em;
    margin-bottom: .2rem;
}
.sb-brand span { color: var(--accent); }
.sb-tagline {
    font-size: .78rem;
    color: var(--text-faint) !important;
    margin-bottom: 1.6rem;
    font-weight: 300;
}
.sb-label {
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--text-faint) !important;
    margin-bottom: .5rem;
}
.sb-desc {
    font-size: .8rem;
    color: var(--text-muted) !important;
    line-height: 1.6;
    margin-top: .65rem;
    padding: .65rem .75rem;
    background: var(--bg2);
    border-radius: var(--radius-sm);
}
.sb-footer {
    font-size: .72rem;
    color: var(--text-faint) !important;
    margin-top: auto;
    padding-top: 2rem;
    text-align: center;
}

/* ── Main content ── */
.page-eyebrow {
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: .75rem;
}
.page-title {
    font-size: 2.4rem;
    font-weight: 600;
    letter-spacing: -.04em;
    line-height: 1.15;
    color: var(--text);
    margin-bottom: .6rem;
}
.page-sub {
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 300;
    line-height: 1.6;
    margin-bottom: 2rem;
    max-width: 480px;
}

/* ── Mode pill ── */
.mode-pill {
    display: inline-flex;
    align-items: center;
    gap: .35rem;
    font-size: .75rem;
    font-weight: 500;
    padding: .3rem .75rem;
    border-radius: 100px;
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid rgba(201,110,63,.2);
    margin-bottom: 1.75rem;
    letter-spacing: .01em;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: .25rem 0 !important;
    gap: .75rem !important;
    align-items: flex-start !important;
}

/* user */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p {
    background: var(--surface);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    padding: .7rem 1rem;
    border-radius: var(--radius-md);
    font-size: .92rem;
    line-height: 1.65;
    display: inline-block;
    max-width: 86%;
    color: var(--text);
    font-weight: 400;
}

/* assistant */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: var(--surface);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    padding: .9rem 1.1rem;
    border-radius: var(--radius-md);
    font-size: .92rem;
    line-height: 1.72;
    color: var(--text);
    font-family: 'Lora', serif;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p {
    margin-bottom: .6rem;
    font-family: 'Lora', serif;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown strong {
    font-weight: 600;
    color: var(--text);
    font-family: 'Sora', sans-serif;
}

/* avatars */
[data-testid="chatAvatarIcon-user"] {
    background: var(--bg2) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    font-size: .8rem !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: var(--accent-soft) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(201,110,63,.25) !important;
    border-radius: 50% !important;
    width: 32px !important;
    height: 32px !important;
    font-size: .8rem !important;
}

/* ── Input ── */
[data-testid="stChatInput"] {
    background: var(--surface) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft), var(--shadow-md) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Sora', sans-serif !important;
    font-size: .9rem !important;
    font-weight: 300 !important;
    color: var(--text) !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-faint) !important;
}

/* ── Button ── */
.stButton button {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--text-muted) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: .8rem !important;
    font-weight: 400 !important;
    border-radius: var(--radius-sm) !important;
    letter-spacing: .01em !important;
    transition: all .18s !important;
}
.stButton button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-soft) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-family: 'Sora', sans-serif !important;
    font-size: .82rem !important;
    font-weight: 300 !important;
    color: var(--text-muted) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; opacity: 1 !important; }

/* ── Alert ── */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    font-family: 'Sora', sans-serif !important;
    font-size: .85rem !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Caption ── */
.stImage ~ p, [data-testid="stCaptionContainer"] {
    font-size: .72rem !important;
    color: var(--text-faint) !important;
    text-align: center !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ── API ──
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    st.error("API Key tidak ditemukan. Tambahkan OPENAI_API_KEY di Streamlit Secrets.")
    st.stop()


# ── Data ──
MODES = {
    "Asisten Umum": {
        "icon": "✦",
        "desc": "Teman diskusi serba-bisa untuk penulisan dan sastra.",
        "placeholder": "Apa yang ingin kamu tulis hari ini?",
        "prompt": (
            "Kamu adalah asisten penulis sastra yang cerdas dan hangat. "
            "Bantu pengguna dengan pertanyaan seputar penulisan kreatif, tata bahasa, "
            "gaya bercerita, atau obrolan santai tentang dunia sastra. "
            "Gunakan bahasa yang natural dan menginspirasi."
        ),
    },
    "Pemicu Plot Twist": {
        "icon": "◎",
        "desc": "Deblokirkan alur ceritamu dengan twist yang segar.",
        "placeholder": "Ceritakan premis atau situasi cerita yang sedang buntu...",
        "prompt": (
            "Kamu adalah Story Doctor — ahli bedah alur cerita. "
            "Berikan tepat 3 plot twist yang segar, tak terduga, dan bebas klise. "
            "Untuk setiap twist, jelaskan singkat mengapa ia menggerakkan emosi pembaca lebih dalam."
        ),
    },
    "Generator Metafora": {
        "icon": "◈",
        "desc": "Ubah kalimat biasa menjadi bahasa yang puitis.",
        "placeholder": "Ketik kalimat yang ingin diubah menjadi lebih puitis...",
        "prompt": (
            "Kamu adalah penyair berbakat. Ubah kalimat biasa yang diberikan pengguna "
            "menjadi 3–4 variasi kalimat puitis yang kaya majas: metafora, personifikasi, simile. "
            "Jelaskan nuansa emosi setiap variasi secara singkat."
        ),
    },
    "Wawancara Karakter": {
        "icon": "◉",
        "desc": "Hidupkan karaktermu lewat sesi roleplay interaktif.",
        "placeholder": "Deskripsikan karaktermu, lalu mulai bertanya...",
        "prompt": (
            "Kamu melakukan ROLEPLAY sebagai karakter fiksi yang dibuat pengguna. "
            "Jika belum ada deskripsi karakter, minta dulu. "
            "Jawab semua pertanyaan sebagai karakter tersebut dari sudut pandang orang pertama. "
            "Ekspresikan kepribadian dan keunikan karakter lewat gaya bicara."
        ),
    },
    "Generator Ilustrasi": {
        "icon": "▣",
        "desc": "Visualisasikan adegan ceritamu dengan DALL-E 3.",
        "placeholder": "Gambarkan suasana atau adegan yang ingin divisualisasikan...",
        "prompt": None,
    },
}


# ── Helpers ──
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


# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="sb-brand">Ruang<span>.</span>Pena</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-tagline">Asisten sastra & penulisan kreatif</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-label">Mode</div>', unsafe_allow_html=True)

    mode = st.radio(
        "",
        list(MODES.keys()),
        format_func=lambda x: f"{MODES[x]['icon']}  {x}",
        label_visibility="collapsed",
    )

    st.markdown(f'<div class="sb-desc">{MODES[mode]["desc"]}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Bersihkan percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown('<div class="sb-footer">Ruang Pena · 2025</div>', unsafe_allow_html=True)


# ── Session state ──
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.current_mode != mode:
    st.session_state.messages = []
    st.session_state.current_mode = mode
    st.rerun()


# ── Header ──
st.markdown('<div class="page-eyebrow">Ruang Pena</div>', unsafe_allow_html=True)
st.markdown('<div class="page-title">Asisten penulis<br>yang memahami kamu.</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Dari plot twist hingga metafora puitis — bantu kamu menulis lebih dalam dan lebih bebas.</div>', unsafe_allow_html=True)
st.markdown(f'<div class="mode-pill">{MODES[mode]["icon"]} &nbsp;{mode}</div>', unsafe_allow_html=True)


# ── Chat history ──
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("is_image"):
            st.image(msg["content"], use_column_width=True)
        else:
            st.markdown(msg["content"])


# ── Input ──
if user_input := st.chat_input(MODES[mode]["placeholder"]):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if mode == "Generator Ilustrasi":
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
