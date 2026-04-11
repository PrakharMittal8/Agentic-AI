# app.py
import os
import time
import streamlit as st
from agent import run_agent  # your existing calculator agent

# ──────────────────────────────────────────────────────────────────────────────
# 1) PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Prakhar's Hacker Calculator Agent",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────────────────────────────────
# 2) THEME CSS (3 vibes): Cyberpunk, Hacker Terminal, Funky Agent
#    We inject CSS based on selection. Keep it small, local, and fast.
# ──────────────────────────────────────────────────────────────────────────────

def css_cyberpunk(accent="#8a5cff"):
    return f"""
    <style>
    :root {{
      --bg1: #070612;
      --bg2: #0e0b1f;
      --panel: rgba(15,12,35,0.6);
      --ink: #e6e8ff;
      --ink-dim: #aab0ff;
      --accent: {accent};
      --glow: 0 0 24px var(--accent), 0 0 48px rgba(138,92,255,0.5);
      --radius: 16px;
    }}
    html, body, [data-testid="stAppViewContainer"] {{
      background:
        radial-gradient(1200px 600px at 15% -10%, rgba(138,92,255,0.25), transparent 60%),
        radial-gradient(900px 450px at 90% 0%, rgba(0,220,255,0.18), transparent 60%),
        linear-gradient(180deg, var(--bg1), var(--bg2));
      color: var(--ink);
    }}
    h1, h2, h3, h4, h5, h6, p, label, span {{
      color: var(--ink);
    }}
    /* Typewriter title */
    .typewrap {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
      font-weight: 700;
      font-size: 1.8rem;
      letter-spacing: .02em;
      display: inline-block;
      border-right: 2px solid var(--ink);
      white-space: nowrap;
      overflow: hidden;
      width: 0;
      animation: typing 2.8s steps(30, end) forwards, blink .9s step-end infinite;
      text-shadow: 0 0 8px rgba(138,92,255,0.6);
    }}
    @keyframes typing {{ from {{ width: 0 }} to {{ width: 100% }} }}
    @keyframes blink {{ 50% {{ border-color: transparent }} }}
    /* Card base */
    .card {{
      background: var(--panel);
      backdrop-filter: blur(10px) saturate(140%);
      border: 1px solid rgba(138,92,255,0.25);
      border-radius: var(--radius);
      box-shadow: var(--glow);
      padding: 18px 18px;
    }}
    /* Buttons */
    .stButton > button {{
      background: linear-gradient(135deg, var(--accent), #00e7ff);
      color: #070612;
      border: none;
      border-radius: 12px;
      height: 44px;
      box-shadow: 0 6px 20px rgba(138,92,255,0.35);
      transition: transform .05s ease, filter .2s ease;
      font-weight: 700;
    }}
    .stButton > button:hover {{ filter: brightness(1.05) saturate(1.15); }}
    .stButton > button:active {{ transform: translateY(1px); }}
    /* Input field */
    .stTextInput > div > div > input {{
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(138,92,255,0.35);
      color: var(--ink);
      border-radius: 12px;
    }}
    /* History item */
    .history {{
      background: rgba(255,255,255,0.04);
      border: 1px dashed rgba(138,92,255,0.35);
      border-radius: 12px;
      padding: 10px 12px;
      margin-bottom: 10px;
      color: var(--ink);
    }}
    .label {{
      font-size: .8rem;
      color: var(--ink-dim);
      letter-spacing: .08em;
      text-transform: uppercase;
    }}
    .metric {{
      font-family: ui-monospace, Menlo, Consolas, monospace;
      color: #a4ffe9;
    }}
    </style>
    """

def css_hacker_terminal():
    return """
    <style>
    :root {
      --bg: #030303;
      --ink: #d6ffd6;
      --dim: #88c988;
      --accent: #00ff66;
      --scan: rgba(0,255,100,0.06);
    }
    html, body, [data-testid="stAppViewContainer"] {
      background:
        linear-gradient(180deg, #020202, #060606 40%, #020202),
        repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(0,255,102,0.02) 4px);
      color: var(--ink);
    }
    .typewrap {
      font-family: "SFMono-Regular", Menlo, Consolas, monospace;
      color: var(--accent);
      text-shadow: 0 0 8px rgba(0,255,102,0.6);
      border-right: 2px solid var(--accent);
      white-space: nowrap; overflow: hidden; width: 0;
      animation: typing 2.4s steps(30,end) forwards, blink .9s step-end infinite;
      font-weight: 700; font-size: 1.6rem;
    }
    @keyframes typing { from {width:0} to {width:100%} }
    @keyframes blink { 50% { border-color: transparent } }
    .card {
      background: rgba(0,0,0,0.55);
      border: 1px solid rgba(0,255,102,0.25);
      border-radius: 14px;
      padding: 16px 16px;
      box-shadow: inset 0 0 0 1px rgba(0,255,102,0.08);
    }
    .stButton > button {
      background: linear-gradient(180deg, #00c957, #00ff66);
      color: #031b0e; border: none; border-radius: 10px; height: 42px;
      box-shadow: 0 0 24px rgba(0,255,102,0.25);
      font-weight: 800;
    }
    .stTextInput > div > div > input {
      background: rgba(0,0,0,0.7); border: 1px solid rgba(0,255,102,0.3);
      color: var(--ink); border-radius: 10px;
    }
    .history {
      background: rgba(0,255,102,0.05);
      border: 1px dashed rgba(0,255,102,0.35);
      border-radius: 10px; padding: 10px 12px; margin-bottom: 10px;
    }
    .label { font-size: .8rem; color: var(--dim); letter-spacing: .08em; text-transform: uppercase; }
    .metric { color: #adfffe; font-family: Menlo, Consolas, monospace; }
    </style>
    """

def css_funky_agent():
    return """
    <style>
    :root{
      --ink: #0c1222; --ink-dim:#3a3f52; --radius: 18px;
    }
    html, body, [data-testid="stAppViewContainer"]{
      background:
        radial-gradient(1400px 600px at 10% -10%, #ffd6f9 0%, transparent 55%),
        radial-gradient(1000px 450px at 100% 0%, #c5ffe8 0%, transparent 55%),
        linear-gradient(180deg, #f7fbff, #ffffff 40%);
      color: var(--ink);
    }
    .typewrap{
      font-weight: 900; font-size: 1.9rem; letter-spacing: .02em;
      background: linear-gradient(90deg, #7b5cff, #1dd3b0, #ff7ac6);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      border-right: 2px solid #7b5cff;
      white-space: nowrap; overflow: hidden; width: 0;
      animation: typing 2.2s steps(30,end) forwards, blink .9s step-end infinite;
    }
    @keyframes typing { from {width:0} to {width:100%} }
    @keyframes blink { 50% { border-color: transparent } }
    .card{
      background: rgba(255,255,255,0.75);
      backdrop-filter: blur(10px) saturate(150%);
      border: 1px solid rgba(123,92,255,0.18);
      border-radius: var(--radius);
      box-shadow: 0 12px 30px rgba(14,22,45,0.12);
      padding: 18px 18px;
    }
    .stButton > button{
      background: linear-gradient(90deg, #7b5cff, #1dd3b0);
      color: white; border: none; border-radius: 14px; height: 46px; font-weight: 800;
      box-shadow: 0 10px 24px rgba(27, 180, 155, 0.35);
    }
    .stButton > button:hover{ filter: brightness(1.06); }
    .stTextInput > div > div > input{
      background: rgba(255,255,255,0.85); border: 1px solid rgba(123,92,255,0.25);
      color: #0c1222; border-radius: 12px;
    }
    .history{
      background: rgba(255,255,255,0.65);
      border: 1px dashed rgba(123,92,255,0.25);
      border-radius: 12px; padding: 10px 12px; margin-bottom: 10px;
    }
    .label{ color: var(--ink-dim); text-transform: uppercase; font-size: .8rem; letter-spacing: .08em; }
    .metric{ color: #7b5cff; font-weight: 700; }
    </style>
    """

# Theme selector (top-right via empty container hack)
theme_col = st.empty()
with theme_col.container():
    tcol1, tcol2, tcol3 = st.columns([1,1,1])
    theme = tcol1.selectbox("Theme", ["Cyberpunk", "Hacker Terminal", "Funky Agent"], index=0)
    if theme == "Cyberpunk":
        accent = tcol2.color_picker("Accent", value="#8a5cff")
        st.markdown(css_cyberpunk(accent), unsafe_allow_html=True)
    elif theme == "Hacker Terminal":
        st.markdown(css_hacker_terminal(), unsafe_allow_html=True)
    else:
        st.markdown(css_funky_agent(), unsafe_allow_html=True)
    density = tcol3.selectbox("Density", ["Comfortable", "Compact"], index=0)

# ──────────────────────────────────────────────────────────────────────────────
# 3) HEADER (typing effect + subtitle)
# ──────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="typewrap">Prakhar\'s Calc Agent v1.0  •  Math + LLM</div>', unsafe_allow_html=True)
st.caption("Deterministic tool‑calling • Safe AST compute • Built for speed")

# ──────────────────────────────────────────────────────────────────────────────
# 4) SESSION STATE (history)
# ──────────────────────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []  # [{q, a, latency_ms, ts}]

# ──────────────────────────────────────────────────────────────────────────────
# 5) LAYOUT: Input card (left) + Tips (right)
# ──────────────────────────────────────────────────────────────────────────────
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="label">Query</div>', unsafe_allow_html=True)

    # Text input with a persistent key so buttons can set it
    user_input = st.text_input(
        label="",
        key="query",
        placeholder="Try: sqrt(144) + 3^3  |  (12.5 + 7.5)^2 / 4  |  log(8) / log(2)",
        label_visibility="collapsed",
    )

    

    # Action buttons
    b1, b2 = st.columns([3, 1])
    run_clicked = b1.button("Run Agent 🚀", use_container_width=True)
    clear_clicked = b2.button("Reset ↺", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Actions
    if clear_clicked:
        st.session_state.history = []
        st.toast("History cleared.", icon="🧹")

    if run_clicked:
        q = (st.session_state.query or "").strip()
        if not q:
            st.warning("Enter a question first.")
        else:
            start = time.time()
            with st.spinner("Computing with tool…"):
                try:
                    answer = run_agent(q)
                    latency_ms = int((time.time() - start) * 1000)
                    st.session_state.history.insert(0, {
                        "q": q,
                        "a": answer,
                        "latency_ms": latency_ms,
                        "ts": time.strftime("%H:%M:%S"),
                    })
                    st.toast("Done ✅", icon="✅")
                except Exception as e:
                    st.error(f"Agent error: {e}")

    # Latest result
    if st.session_state.history:
        latest = st.session_state.history[0]
        st.markdown("#### Result")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(latest["a"])
        mcol1, mcol2, mcol3 = st.columns(3)
        mcol1.markdown(f'<span class="label">Latency</span><br><span class="metric">{latest["latency_ms"]} ms</span>', unsafe_allow_html=True)
        mcol2.markdown(f'<span class="label">Time</span><br><span class="metric">{latest["ts"]}</span>', unsafe_allow_html=True)
        mcol3.markdown(f'<span class="label">Mode</span><br><span class="metric">{theme}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # History list
    if st.session_state.history:
        st.markdown("#### History")
        max_items = 8 if density == "Comfortable" else 12
        for i, item in enumerate(st.session_state.history[:max_items], start=1):
            st.markdown(
                f'<div class="history"><b>Q{i}:</b> {item["q"]}<br/><b>A{i}:</b> {item["a"]}'
                f'<br/><span class="label">Latency:</span> {item["latency_ms"]} ms &nbsp; '
                f'<span class="label">At:</span> {item["ts"]}</div>',
                unsafe_allow_html=True
            )

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### Tips")
    # Your two lines, hacker‑vibe, polished
    st.markdown(
        "- **Ask me any mathematical expression** — from simple arithmetic to deep‑nested functions. "
        "My compute engine evaluates it with deterministic precision.\n"
        "- **If it’s not math**, the language model takes over and responds briefly, keeping the tool pipeline clean."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Prakhar’s AI Calculator • Neon‑secure AST compute • Built with Streamlit")