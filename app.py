import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from openai import OpenAI

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Ruang Pena · Asisten Sastra",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — "Ink & Parchment" aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=IM+Fell+English:ital@0;1&family=Crimson+Pro:ital,wght@0,300;0,400;1,300;1,400&display=swap');

/* ── Palette ── */
:root {
    --parchment:   #f5f0e8;
    --parchment2:  #ede6d5;
    --ink:         #1c1410;
    --ink-faded:   #4a3f35;
    --sepia:       #8b6b4a;
    --sepia-light: #c4a882;
    --gold:        #b8860b;
    --gold-light:  #d4a832;
    --crimson:     #8b1a1a;
    --sidebar-bg:  #211a14;
    --sidebar-txt: #e8dcc8;
    --shadow:      rgba(28,20,16,.18);
}

/* ── Base / Body ── */
html, body, [class*="css"] {
    font-family: 'Crimson Pro', Georgia, serif;
    background-color: var(--parchment);
    color: var(--ink);
}

/* ── Parchment texture overlay ── */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.045'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 860px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 2px solid var(--gold) !important;
}
[data-testid="stSidebar"] * {
    color: var(--sidebar-txt) !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.05rem !important;
    letter-spacing: .03em;
    transition: color .2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--gold-light) !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] div {
    background-color: var(--gold) !important;
    border-color: var(--gold) !important;
}
/* sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: var(--sepia) !important;
    opacity: .4;
}

/* ── Sidebar header ── */
.sidebar-header {
    font-family: 'IM Fell English', serif;
    font-size: 1.55rem;
    color: var(--gold-light);
    text-align: center;
    line-height: 1.3;
    margin-bottom: .2rem;
}
.sidebar-sub {
    font-family: 'Crimson Pro', serif;
    font-size: .85rem;
    color: var(--sepia-light);
    text-align: center;
    font-style: italic;
    margin-bottom: 1.2rem;
    letter-spacing: .06em;
}
.sidebar-divider {
    text-align: center;
    color: var(--gold);
    letter-spacing: .2em;
    font-size: .7rem;
    margin: 1rem 0;
    opacity: .6;
}

/* ── Main title block ── */
.main-title {
    font-family: 'IM Fell English', serif;
    font-size: 2.6rem;
    color: var(--ink);
    text-align: center;
    line-height: 1.2;
    margin-bottom: .15rem;
}
.main-title span { color: var(--crimson); }
.main-sub {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    color: var(--sepia);
    text-align: center;
    font-style: italic;
    letter-spacing: .08em;
    margin-bottom: .6rem;
}
.ornament {
    text-align: center;
    color: var(--gold);
    font-size: 1.3rem;
    letter-spacing: .3em;
    margin: .4rem 0 1.2rem;
}

/* ── Mode badge ── */
.mode-badge {
    display: inline-block;
    background: var(--ink);
    color: var(--gold-light);
    font-family: 'Cormorant Garamond', serif;
    font-size: .82rem;
    letter-spacing: .12em;
    padding: .22rem .85rem;
    border-radius: 2px;
    border: 1px solid var(--gold);
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* ── Chat container card ── */
.chat-wrapper {
    background: var(--parchment2);
    border: 1px solid var(--sepia-light);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 4px 24px var(--shadow), inset 0 0 60px rgba(180,150,100,.06);
    min-height: 200px;
    margin-bottom: 1rem;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: .2rem 0 !important;
}
/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p {
    background: var(--ink);
    color: var(--parchment) !important;
    padding: .7rem 1.1rem;
    border-radius: 2px 14px 14px 14px;
    display: inline-block;
    font-size: 1.02rem;
    line-height: 1.6;
    max-width: 88%;
    font-family: 'Crimson Pro', serif;
    letter-spacing: .01em;
}
/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: linear-gradient(135deg, rgba(255,255,255,.55), rgba(245,240,232,.8));
    border-left: 3px solid var(--gold);
    padding: .8rem 1.1rem;
    border-radius: 0 14px 14px 2px;
    font-size: 1.05rem;
    line-height: 1.75;
    font-family: 'Crimson Pro', serif;
    box-shadow: 0 2px 8px var(--shadow);
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p {
    margin-bottom: .5rem;
}
/* Avatars */
[data-testid="chatAvatarIcon-user"] {
    background: var(--ink) !important;
    color: var(--gold-light) !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: var(--gold) !important;
    color: var(--ink) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    border: 1.5px solid var(--sepia-light) !important;
    border-radius: 4px !important;
    background: var(--parchment) !important;
    box-shadow: 0 2px 12px var(--shadow) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.05rem !important;
    color: var(--ink) !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--sepia-light) !important;
    font-style: italic !important;
}

/* ── Clear button ── */
.stButton button {
    background: transparent !important;
    border: 1px solid var(--sepia-light) !important;
    color: var(--sepia) !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: .9rem !important;
    letter-spacing: .08em !important;
    border-radius: 2px !important;
    transition: all .25s !important;
}
.stButton button:hover {
    background: var(--ink) !important;
    color: var(--gold-light) !important;
    border-color: var(--gold) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic !important;
    color: var(--sepia) !important;
    letter-spacing: .06em;
}

/* ── Info / error boxes ── */
.stAlert {
    font-family: 'Crimson Pro', serif !important;
    border-radius: 3px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--parchment2); }
::-webkit-scrollbar-thumb { background: var(--sepia-light); border-radius: 3px; }

/* ── Responsive ── */
@media (max-width: 768px) {
    .main-title { font-size: 1.9rem; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
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
    st.error("🔑 OpenAI API Key tidak ditemukan. Mohon konfigurasikan di Streamlit Cloud Secrets.")
    st.stop()


# ─────────────────────────────────────────────
#  SYSTEM PROMPTS
# ─────────────────────────────────────────────
PROMPTS = {
    "✒️ Asisten Umum": (
        "Kamu adalah asisten penulis sastra yang hangat, bijaksana, dan puitis. "
        "Bantu pengguna dengan segala pertanyaan seputar penulisan kreatif, tata bahasa, "
        "gaya bercerita, atau sekadar obrolan santai soal dunia sastra. "
        "Gunakan bahasa yang elegan namun mudah dipahami."
    ),
    "🌀 Pemicu Plot Twist": (
        "Kamu adalah seorang Story Doctor — ahli bedah alur cerita yang jenius. "
        "Ketika pengguna memberikan premis atau situasi cerita yang buntu, "
        "berikan tepat 3 ide 'plot twist' yang segar, tak terduga, dan bebas klise. "
        "Untuk setiap twist, jelaskan mengapa ia mampu menggerakkan emosi pembaca secara lebih dalam. "
        "Gunakan gaya bahasa yang dramatis dan menginspirasi."
    ),
    "🌹 Generator Metafora": (
        "Kamu adalah seorang penyair berbakat yang hidup di persimpangan antara bahasa dan perasaan. "
        "Ketika pengguna memberikan kalimat biasa, ubah menjadi 3–4 variasi kalimat puitis "
        "yang kaya majas: metafora, personifikasi, simile, dan imaji indrawi. "
        "Sertakan rima jika alami. Jelaskan nuansa emosi setiap variasi dengan singkat dan indah."
    ),
    "🎭 Wawancara Karakter": (
        "Kamu sedang melakukan ROLEPLAY. Pengguna akan mewawancarai sebuah karakter fiksi. "
        "Minta pengguna mendeskripsikan karakternya jika belum jelas. "
        "Lalu JAWAB SEMUA PERTANYAAN SEPENUHNYA SEBAGAI KARAKTER TERSEBUT — "
        "gunakan sudut pandang orang pertama (Aku/Saya). "
        "Ekspresikan kepribadian, luka batin, dan keunikan karakter lewat pilihan kata dan ritme bicaranya. "
        "Tetap dalam karakter selama percakapan berlangsung."
    ),
    "🖼️ Generator Ilustrasi": None,  # handled separately
}

MODE_PLACEHOLDERS = {
    "✒️ Asisten Umum":         "Apa yang ingin kamu tulis hari ini?",
    "🌀 Pemicu Plot Twist":    "Ceritakan premis atau situasi yang sedang buntu...",
    "🌹 Generator Metafora":   "Ketik kalimat yang ingin diubah menjadi puisi...",
    "🎭 Wawancara Karakter":   "Deskripsikan karaktermu, lalu mulai bertanya...",
    "🖼️ Generator Ilustrasi": "Gambarkan suasana atau adegan yang ingin kamu visualisasikan...",
}


# ─────────────────────────────────────────────
#  CORE FUNCTIONS
# ─────────────────────────────────────────────
def get_chat_response(user_input: str, history: list, system_prompt: str) -> str:
    messages = [SystemMessage(content=system_prompt)]
    for msg in history[-10:]:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant" and not msg.get("is_image"):
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=user_input))
    return llm.invoke(messages).content


def get_image_url(prompt: str) -> str:
    try:
        resp = client.images.generate(
            model="gpt-image-1-mini",
            prompt=(
                "A highly artistic, atmospheric, painterly illustration for a literary novel — "
                "warm sepia and ink tones, fine detail, storytelling mood. "
                f"{prompt}"
            ),
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return resp.data[0].url
    except Exception as exc:
        return f"ERROR:{exc}"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">🪶 Ruang Pena</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Asisten Sastra & Penulis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-divider">⊱ ── ✦ ── ⊰</div>', unsafe_allow_html=True)

    mode = st.radio(
        "Pilih Mode Asisten:",
        list(PROMPTS.keys()),
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-divider">⊱ ── ✦ ── ⊰</div>', unsafe_allow_html=True)

    # Mode description cards
    descriptions = {
        "✒️ Asisten Umum":         "Teman diskusi serba-bisa untuk pertanyaan penulisan dan sastra.",
        "🌀 Pemicu Plot Twist":    "Deblokirkan alur ceritamu dengan 3 twist tak terduga.",
        "🌹 Generator Metafora":   "Ubah kalimat biasa menjadi untaian kata yang puitis.",
        "🎭 Wawancara Karakter":   "Hidupkan karaktermu lewat sesi roleplay interaktif.",
        "🖼️ Generator Ilustrasi": "Visualisasikan adegan ceritamu dengan DALL-E 3.",
    }
    st.markdown(
        f"<p style='font-style:italic; font-size:.88rem; color:#c4a882; line-height:1.5;'>"
        f"{descriptions[mode]}</p>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-divider">⊱ ── ✦ ── ⊰</div>', unsafe_allow_html=True)

    if st.button("🗑️  Bersihkan Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<p style='font-size:.75rem; color:#6b5c4c; text-align:center; margin-top:2rem; "
        "font-style:italic;'>\"Setiap kalimat adalah pintu menuju dunia baru.\"</p>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
#  SESSION STATE — reset on mode change
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
    '<div class="main-title">Ruang <span>Pena</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="main-sub">Di sinilah kata-kata menemukan jiwa mereka</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="ornament">❧ ─── ✦ ─── ❧</div>', unsafe_allow_html=True)
st.markdown(f'<div class="mode-badge">{mode}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CHAT HISTORY DISPLAY
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("is_image"):
            st.image(msg["content"], use_column_width=True)
        else:
            st.markdown(msg["content"])


# ─────────────────────────────────────────────
#  CHAT INPUT & RESPONSE
# ─────────────────────────────────────────────
placeholder = MODE_PLACEHOLDERS.get(mode, "Ketik pesanmu di sini...")

if user_input := st.chat_input(placeholder):
    # Save & display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate & display assistant response
    with st.chat_message("assistant"):
        if mode == "🖼️ Generator Ilustrasi":
            with st.spinner("Melukis imajinasimu di atas kanvas digital..."):
                url = get_image_url(user_input)
                if url.startswith("ERROR:"):
                    st.error(f"Terjadi kesalahan: {url[6:]}")
                else:
                    st.image(url, use_column_width=True)
                    st.caption("_Ilustrasi dibuat dengan DALL-E 3 · klik kanan untuk menyimpan_")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": url, "is_image": True}
                    )
        else:
            with st.spinner("Merangkai kata-kata untukmu..."):
                system_prompt = PROMPTS[mode]
                reply = get_chat_response(user_input, st.session_state.messages, system_prompt)
                st.markdown(reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": reply, "is_image": False}
                )
