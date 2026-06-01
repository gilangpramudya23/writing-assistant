import streamlit as st
from langchain_openai import ChatOpenAI

# ── Page Config ──
st.set_page_config(
    page_title="Asisten Menulis",
    page_icon="✏️",
    layout="centered"
)

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #212121;
    color: #ececec;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

.main .block-container {
    max-width: 720px;
    padding: 2rem 1.5rem 7rem 1.5rem;
    margin: 0 auto;
}

/* Title */
h1 {
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    color: #ececec !important;
    margin-bottom: 0.25rem !important;
}

/* Hide avatars */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    display: flex;
    justify-content: flex-end;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
    background: #2f2f2f;
    border-radius: 18px 18px 4px 18px;
    padding: 0.65rem 1rem;
    max-width: 80%;
    font-size: 0.9rem;
    line-height: 1.6;
    color: #ececec;
}

/* Assistant message */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: transparent;
    padding: 0;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown p {
    font-size: 0.9rem;
    line-height: 1.75;
    color: #ececec;
}

/* Chat input */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: min(720px, 100vw);
    padding: 1rem 1.5rem 1.5rem;
    background: #212121;
    border-top: 1px solid #2a2a2a;
    z-index: 100;
}

[data-testid="stChatInputTextArea"] {
    background: #2f2f2f !important;
    border: 1px solid #3a3a3a !important;
    border-radius: 12px !important;
    color: #ececec !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.875rem !important;
}

[data-testid="stChatInputTextArea"]:focus {
    border-color: #555 !important;
    box-shadow: none !important;
}

[data-testid="stChatInputSubmitButton"] {
    background: #ececec !important;
    border-radius: 8px !important;
}

/* Spinner */
[data-testid="stSpinner"] p {
    font-size: 0.8rem;
    color: #888;
}
</style>
""", unsafe_allow_html=True)

# ── API Setup ──
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
else:
    st.error("OpenAI API Key tidak ditemukan di secrets.")
    st.stop()

# ── Helper ──
def get_chatbot_response(user_input, history):
    prompt_chatbot = f"""Kamu adalah seorang asisten chatbot yang sangat ahli dalam bidang penulisan sastra.
    Kamu memahami dengan sangat baik tentang berbagai genre sastra, teknik penulisan, dan gaya bahasa yang berbeda.
    Kamu memahami dengan sangat baik tentang bagaimana membangun karakter yang kuat, menciptakan plot yang menarik, dan menggunakan bahasa yang efektif untuk menyampaikan pesan atau emosi dalam tulisan.
    Selain itu, kamu juga memahami bagaimana emosi dan pengalaman pribadi dapat mempengaruhi gaya penulisan seseorang, dan kamu dapat memberikan saran yang sesuai untuk membantu penulis mengembangkan gaya mereka sendiri.

    Jawablah pertanyaan pengguna dengan gaya santai dan ramah, seolah-olah kamu adalah seorang teman yang sedang berbicara dengan pengguna.
    Kamu bisa menggunakan bahasa sehari-hari, tetapi tetap menjaga kejelasan dan kesopanan dalam menjawab pertanyaan.

    Respon kamu harus informatif, memberikan wawasan yang mendalam, dan membantu pengguna memahami konsep atau teknik penulisan dengan lebih baik.

    Jawablah sesuai dengan permintaan pengguna. Jika pengguna meminta informasi yang detail, berikanlah jawaban yang detail. Jika pengguna meminta penjelasan singkat, berikanlah jawaban yang singkat dan padat.

    Berikut ini riwayat percakapan:
    {history}

    User : {user_input}"""
    response = llm.invoke(prompt_chatbot)
    return response

# ── Session State ──
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ──
st.title("Asisten Menulis")

# ── Chat History ──
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Input ──
if prompt := st.chat_input("Mau nulis apa hari ini?"):
    history = st.session_state.messages[-10:]

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = get_chatbot_response(prompt, history)
            answer = response.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
