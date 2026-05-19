import streamlit as st
from fewshot import FewShotPosts
from post_generator import generate_post

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&display=swap');

    /* ─── Root & Page ─────────────────────────────── */
    :root {
        --crimson:      #C41E3A;
        --crimson-dim:  #8B0000;
        --crimson-glow: rgba(196, 30, 58, 0.25);
        --obsidian:     #0A0A0A;
        --charcoal:     #111111;
        --surface:      #181818;
        --surface-2:    #202020;
        --border:       rgba(196, 30, 58, 0.18);
        --border-hover: rgba(196, 30, 58, 0.55);
        --text-primary: #F0EBE3;
        --text-muted:   #7A7068;
        --text-accent:  #C41E3A;
    }

    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background-color: var(--obsidian) !important;
        font-family: 'Montserrat', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent !important; }

    /* ─── Hide default Streamlit chrome ───────────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ─── Main container ──────────────────────────── */
    .main .block-container {
        max-width: 860px;
        padding: 3rem 2.5rem 4rem;
        margin: 0 auto;
    }

    /* ─── Hero header ─────────────────────────────── */
    .hero-wrap {
        text-align: center;
        padding: 3.5rem 0 2.8rem;
        position: relative;
    }
    .hero-wrap::before {
        content: '';
        position: absolute;
        top: 0; left: 50%;
        transform: translateX(-50%);
        width: 1px;
        height: 48px;
        background: linear-gradient(to bottom, transparent, var(--crimson));
    }
    .hero-eyebrow {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        color: var(--crimson);
        margin-bottom: 1rem;
    }
    .hero-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(2.4rem, 5vw, 3.8rem);
        font-weight: 300;
        font-style: italic;
        color: var(--text-primary);
        line-height: 1.15;
        letter-spacing: -0.01em;
        margin: 0 0 0.6rem;
    }
    .hero-title span {
        color: var(--crimson);
        font-style: normal;
        font-weight: 600;
    }
    .hero-sub {
        font-size: 0.78rem;
        font-weight: 300;
        letter-spacing: 0.15em;
        color: var(--text-muted);
        text-transform: uppercase;
    }
    .hero-divider {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2rem auto 0;
        max-width: 260px;
    }
    .hero-divider::before,
    .hero-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }
    .hero-divider-dot {
        width: 5px; height: 5px;
        border-radius: 50%;
        background: var(--crimson);
        box-shadow: 0 0 10px var(--crimson);
    }

    /* ─── Card / Panel ────────────────────────────── */
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 2px;
        padding: 2.2rem 2.4rem;
        margin-bottom: 1.4rem;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: linear-gradient(to bottom, var(--crimson), transparent);
    }
    .card-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--crimson);
        margin-bottom: 1.4rem;
    }

    /* ─── Selectbox labels ────────────────────────── */
    [data-testid="stSelectbox"] label,
    .stSelectbox label {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.63rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.24em !important;
        text-transform: uppercase !important;
        color: var(--text-muted) !important;
        margin-bottom: 0.5rem !important;
    }

    /* ─── Selectbox control ───────────────────────── */
    [data-testid="stSelectbox"] > div > div,
    .stSelectbox > div > div {
        background-color: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        color: var(--text-primary) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 300 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    [data-testid="stSelectbox"] > div > div:hover {
        border-color: var(--border-hover) !important;
        box-shadow: 0 0 0 2px var(--crimson-glow) !important;
    }
    [data-testid="stSelectbox"] > div > div:focus-within {
        border-color: var(--crimson) !important;
        box-shadow: 0 0 0 3px var(--crimson-glow) !important;
    }

    /* Dropdown arrow & text colour */
    [data-testid="stSelectbox"] svg { fill: var(--crimson) !important; }
    [data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: var(--text-primary) !important;
    }

    /* ─── Dropdown popover ────────────────────────── */
    [data-baseweb="popover"] ul,
    [role="listbox"] {
        background: var(--surface-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
    }
    [role="option"] {
        background: transparent !important;
        color: var(--text-primary) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 300 !important;
        transition: background 0.15s !important;
    }
    [role="option"]:hover,
    [aria-selected="true"] {
        background: rgba(196, 30, 58, 0.12) !important;
        color: var(--crimson) !important;
    }

    /* ─── Generate Button ─────────────────────────── */
    [data-testid="stButton"] > button {
        width: 100%;
        background: transparent !important;
        border: 1px solid var(--crimson) !important;
        border-radius: 2px !important;
        color: var(--crimson) !important;
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.35em !important;
        text-transform: uppercase !important;
        padding: 1rem 2.5rem !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.3s ease !important;
        margin-top: 0.5rem;
    }
    [data-testid="stButton"] > button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(196,30,58,0.08), transparent);
        transition: left 0.5s ease;
    }
    [data-testid="stButton"] > button:hover {
        background: rgba(196, 30, 58, 0.08) !important;
        box-shadow: 0 0 24px var(--crimson-glow), inset 0 0 24px rgba(196,30,58,0.04) !important;
        color: #E83A56 !important;
        border-color: #E83A56 !important;
    }
    [data-testid="stButton"] > button:hover::before { left: 100%; }
    [data-testid="stButton"] > button:active {
        transform: scale(0.985) !important;
        box-shadow: 0 0 8px var(--crimson-glow) !important;
    }

    /* ─── Output area ─────────────────────────────── */
    .output-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 2px;
        padding: 2rem 2.4rem;
        margin-top: 1.6rem;
        position: relative;
        animation: fadeSlideUp 0.5s cubic-bezier(0.22,1,0.36,1) both;
    }
    .output-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(to right, var(--crimson), transparent);
    }
    .output-label {
        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--crimson);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .output-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: var(--border);
    }

    /* ─── Streamlit's own write / markdown ───────── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stText"] {
        font-family: 'Montserrat', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 300 !important;
        color: var(--text-primary) !important;
        line-height: 1.85 !important;
    }

    /* ─── Column gaps ─────────────────────────────── */
    [data-testid="stHorizontalBlock"] {
        gap: 1.2rem !important;
    }

    /* ─── Scrollbar ───────────────────────────────── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: var(--obsidian); }
    ::-webkit-scrollbar-thumb { background: var(--crimson-dim); border-radius: 2px; }

    /* ─── Animations ──────────────────────────────── */
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ─── Spinner ─────────────────────────────────── */
    [data-testid="stSpinner"] { color: var(--crimson) !important; }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="LinkedIn Post Generator · Pradeep's - AI Studio",
        page_icon="✦",
        layout="centered",
    )

    inject_custom_css()

    # ── Hero ──────────────────────────────────────────
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-eyebrow">Pradeep's - AI Studio</div>
        <h1 class="hero-title">LinkedIn <span>Post</span> Generator</h1>
        <p class="hero-sub">Craft · Refine · Publish</p>
        <div class="hero-divider"><div class="hero-divider-dot"></div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls card ──────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">✦ &nbsp;Configure your post</div>', unsafe_allow_html=True)

    fs = FewShotPosts()
    tags = fs.get_tags()

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_tag = st.selectbox("Topic", options=tags)
    with col2:
        selected_length = st.selectbox("Length", options=length_options)
    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Generate button ────────────────────────────────
    col_btn, _ = st.columns([1, 2])
    with col_btn:
        generate_clicked = st.button("✦  Generate Post")

    # ── Output ─────────────────────────────────────────
    if generate_clicked:
        with st.spinner("Composing…"):
            post = generate_post(selected_length, selected_language, selected_tag)

        st.markdown('<div class="output-card"><div class="output-label">Generated post</div>', unsafe_allow_html=True)
        st.write(post)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()