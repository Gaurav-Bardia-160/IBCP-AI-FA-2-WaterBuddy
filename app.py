"""
WaterBuddy - Interactive Water Hydration Tracker
Faithfully designed and built according to the FA-1 Storyboard.

Features:
- Balanced 2-column layout (Visual Core on Left, Control Dashboard on Right)
- 4 Avatars: Child, Teen, Adult, Senior with standard recommendations
- Translucent animated water bottle that visually fills with real-time level
- Turtle mascot with exact storyboard milestone states (<20% resting, >=20% smiling, >=75% waving, 100%+ celebration)
- Compulsory +250ml quick log, +100ml, +500ml, and custom entry
- Python logic counters: Total intake, remaining needed, percentage achieved
- End-of-day summary card & New Day reset confirmation
"""

import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Auto-launcher when run directly via 'python app.py'
if get_script_run_ctx() is None:
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())

import streamlit as st
from datetime import datetime
import pandas as pd

# ==============================================================================
# 1. PAGE SETUP & CLEAN MINT-THEME STYLING
# ==============================================================================
st.set_page_config(
    page_title="WaterBuddy",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Polished pastel mint styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Nunito:wght@700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Overall Background */
    .stApp {
        background: linear-gradient(180deg, #f0fdf4 0%, #f7fee7 50%, #f0f9ff 100%);
    }

    .block-container {
        max-width: 1000px;
        padding-top: 1.2rem;
        padding-bottom: 2.5rem;
    }

    /* Clean Brand Banner */
    .brand-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(135deg, #d8f3dc 0%, #b7e4c7 100%);
        border: 1.5px solid #74c69d;
        border-radius: 16px;
        padding: 0.9rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 15px rgba(82, 183, 136, 0.12);
    }
    .brand-title {
        font-family: 'Nunito', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        color: #1b4332;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .brand-tag {
        font-size: 0.85rem;
        font-weight: 700;
        color: #2d6a4f;
        background: rgba(255, 255, 255, 0.85);
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid #95d5b2;
    }

    /* Aligned Metric Micro-Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-bottom: 12px;
    }
    .metric-box {
        background: #ffffff;
        border: 1.5px solid #d8f3dc;
        border-radius: 12px;
        padding: 10px 8px;
        text-align: center;
    }
    .metric-lbl {
        font-size: 0.72rem;
        font-weight: 800;
        color: #15803d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 1.35rem;
        font-weight: 800;
        color: #1b4332;
        margin-top: 2px;
        line-height: 1.1;
    }

    /* Turtle Mascot Card */
    .mascot-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1.5px solid #86efac;
        border-radius: 14px;
        padding: 12px;
        text-align: center;
        margin-top: 10px;
    }
    .mascot-title {
        font-family: 'Nunito', sans-serif;
        font-size: 1.05rem;
        font-weight: 800;
        color: #14532d;
        margin-top: 4px;
    }
    .mascot-desc {
        font-size: 0.85rem;
        color: #166534;
        margin-top: 2px;
        margin-bottom: 0;
        line-height: 1.35;
    }

    /* Bottle Motivational Messages */
    .bottle-caption {
        font-family: 'Nunito', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        color: #0369a1;
        text-align: center;
        margin-top: 6px;
    }
    .bottle-sub {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 600;
        text-align: center;
        margin-bottom: 4px;
    }

    /* Target Guideline Pill */
    .guideline-banner {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 8px 12px;
        margin-top: 8px;
        font-size: 0.85rem;
        color: #166534;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Streamlit Container Enhancements */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #d8f3dc !important;
        border-radius: 16px !important;
        background: #ffffff !important;
        box-shadow: 0 4px 16px rgba(45, 106, 79, 0.04) !important;
    }

    /* Button Polish */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%) !important;
        border: none !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. STORYBOARD DATA CONSTANTS
# ==============================================================================
AVATARS = {
    "Child (6–12 yrs)": {
        "icon": "🧒",
        "name": "Child",
        "recommended_ml": 1600,
        "cups": "≈ 6–7 cups 🥛",
        "hint": "Growing bodies require regular sips during school & playtime."
    },
    "Teen (13–18 yrs)": {
        "icon": "👧",
        "name": "Teen",
        "recommended_ml": 2000,
        "cups": "≈ 8–10 cups 🥛",
        "hint": "High study routines & activities demand constant hydration."
    },
    "Adult (19–50 yrs)": {
        "icon": "🧑",
        "name": "Adult",
        "recommended_ml": 2500,
        "cups": "≈ 8–10 cups 🥛",
        "hint": "Supports peak cognitive energy, organ health, and metabolism."
    },
    "Senior (65+ yrs)": {
        "icon": "👴",
        "name": "Senior",
        "recommended_ml": 2000,
        "cups": "≈ 4–10 cups 🥛",
        "hint": "Thirst sensation decreases with age; scheduled drinking is key."
    }
}


# ==============================================================================
# 3. VECTOR GRAPHICS (TURTLE & BOTTLE)
# ==============================================================================

def render_turtle_mascot(pct: float):
    """Generates the Turtle Mascot SVG matching Storyboard Panel 6."""
    if pct >= 100.0:
        state_title = "Celebration! 🎉"
        state_desc = "Awesome job! You reached 100% of your daily water goal!"
        flipper = '<path d="M 125 70 Q 145 45 155 35 Q 162 42 152 60 Q 140 78 128 85 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'
        mouth = '<path d="M 130 63 Q 138 78 146 63 Z" stroke="#1b4332" stroke-width="2" fill="#e11d48"/>'
        face = '''
        <path d="M 128 53 Q 133 48 136 53" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <path d="M 142 53 Q 147 48 150 53" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="128" cy="60" rx="3.5" ry="2" fill="#fca5a5"/>
        <ellipse cx="150" cy="60" rx="3.5" ry="2" fill="#fca5a5"/>
        <polygon points="160,18 163,25 170,26 165,31 166,38 160,34 154,38 155,31 150,26 157,25" fill="#f59e0b"/>
        <circle cx="145" cy="16" r="3" fill="#ec4899"/>
        <circle cx="55" cy="18" r="2.5" fill="#10b981"/>
        '''
    elif pct >= 75.0:
        state_title = "Avatar Waves 👋"
        state_desc = f"You are at {pct}%! Turtle is happily waving you to the finish line!"
        flipper = '<path d="M 125 70 Q 145 45 155 35 Q 162 42 152 60 Q 140 78 128 85 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'
        mouth = '<path d="M 130 65 Q 138 74 146 65" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        face = '''
        <circle cx="132" cy="52" r="3.5" fill="#1b4332"/>
        <circle cx="146" cy="52" r="3.5" fill="#1b4332"/>
        <circle cx="133.5" cy="50.5" r="1.2" fill="#ffffff"/>
        <circle cx="147.5" cy="50.5" r="1.2" fill="#ffffff"/>
        <ellipse cx="128" cy="60" rx="3" ry="1.5" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="149" cy="60" rx="3" ry="1.5" fill="#fca5a5" opacity="0.6"/>
        '''
    elif pct >= 20.0:
        state_title = "Avatar Smiles 😊"
        state_desc = f"Great start ({pct}%)! Turtle is smiling at your healthy routine."
        flipper = '<path d="M 125 85 Q 145 92 148 102 Q 140 108 125 98 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'
        mouth = '<path d="M 130 65 Q 138 74 146 65" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        face = '''
        <circle cx="132" cy="52" r="3.5" fill="#1b4332"/>
        <circle cx="146" cy="52" r="3.5" fill="#1b4332"/>
        <circle cx="133.5" cy="50.5" r="1.2" fill="#ffffff"/>
        <circle cx="147.5" cy="50.5" r="1.2" fill="#ffffff"/>
        <ellipse cx="128" cy="60" rx="3" ry="1.5" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="149" cy="60" rx="3" ry="1.5" fill="#fca5a5" opacity="0.6"/>
        '''
    else:
        state_title = "Turtle is Resting 🐢"
        state_desc = "Take your first sip (reach 20%) to wake Turtle up and see him smile!"
        flipper = '<path d="M 125 85 Q 145 92 148 102 Q 140 108 125 98 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'
        mouth = '<path d="M 132 65 Q 138 68 144 65" stroke="#1b4332" stroke-width="2" fill="none" stroke-linecap="round"/>'
        face = '''
        <circle cx="132" cy="53" r="3" fill="#1b4332"/>
        <circle cx="146" cy="53" r="3" fill="#1b4332"/>
        <circle cx="133" cy="52" r="1" fill="#ffffff"/>
        <circle cx="147" cy="52" r="1" fill="#ffffff"/>
        '''

    svg = f"""
    <div style="display:flex; justify-content:center; align-items:center;">
        <svg width="180" height="120" viewBox="0 0 190 135" fill="none" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="48" cy="100" rx="14" ry="9" fill="#52b788" stroke="#2d6a4f" stroke-width="2.5"/>
            <ellipse cx="108" cy="100" rx="14" ry="9" fill="#52b788" stroke="#2d6a4f" stroke-width="2.5"/>
            <path d="M 28 85 Q 15 88 18 95 Q 26 95 32 89 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>
            <ellipse cx="78" cy="75" rx="52" ry="40" fill="#2d6a4f" stroke="#1b4332" stroke-width="3"/>
            <ellipse cx="78" cy="72" rx="46" ry="34" fill="#40916c"/>
            <polygon points="78,48 93,56 93,72 78,80 63,72 63,56" fill="#52b788" stroke="#2d6a4f" stroke-width="2"/>
            <polygon points="78,80 93,88 93,98 78,102 63,98 63,88" fill="#52b788" stroke="#2d6a4f" stroke-width="1.8"/>
            <polygon points="108,60 118,66 118,78 108,84 96,78 96,66" fill="#74c69d" stroke="#2d6a4f" stroke-width="1.8"/>
            <polygon points="48,60 60,66 60,78 48,84 38,78 38,66" fill="#74c69d" stroke="#2d6a4f" stroke-width="1.8"/>
            <ellipse cx="70" cy="105" rx="14" ry="8" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>
            {flipper}
            <path d="M 112 75 Q 120 65 128 62 L 132 82 Q 122 84 115 80 Z" fill="#74c69d"/>
            <ellipse cx="138" cy="58" rx="18" ry="17" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>
            {face}
            {mouth}
        </svg>
    </div>
    """
    return svg, state_title, state_desc


def render_translucent_bottle(pct: float) -> str:
    """Generates the Translucent Water Bottle SVG matching Storyboard Screens 1, 2, 3."""
    clamped = min(max(pct, 0.0), 100.0)
    fill_h = (clamped / 100.0) * 165
    water_y = 215 - fill_h

    return f"""
    <div style="display:flex; justify-content:center; align-items:center; padding: 4px 0;">
        <svg width="140" height="250" viewBox="0 0 150 255" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="wbGrad" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#38bdf8" />
                    <stop offset="100%" stop-color="#0284c7" />
                </linearGradient>
                <linearGradient id="wbGlass" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stop-color="white" stop-opacity="0.6"/>
                    <stop offset="40%" stop-color="white" stop-opacity="0.1"/>
                    <stop offset="100%" stop-color="white" stop-opacity="0.4"/>
                </linearGradient>
                <clipPath id="wbClip">
                    <path d="M 56 26 L 94 26 L 94 50 Q 120 58 120 85 L 120 215 Q 120 228 106 228 L 44 228 Q 30 228 30 215 L 30 85 Q 30 58 56 50 Z" />
                </clipPath>
            </defs>
            <rect x="58" y="12" width="34" height="15" rx="4" fill="#0284c7"/>
            <rect x="55" y="24" width="40" height="4" rx="2" fill="#38bdf8"/>
            <path d="M 56 26 L 94 26 L 94 50 Q 120 58 120 85 L 120 215 Q 120 228 106 228 L 44 228 Q 30 228 30 215 L 30 85 Q 30 58 56 50 Z" fill="#f0f9ff" stroke="#bae6fd" stroke-width="2.5"/>
            <g clip-path="url(#wbClip)">
                <rect x="25" y="{water_y}" width="100" height="{fill_h + 30}" fill="url(#wbGrad)"/>
                <ellipse cx="75" cy="{water_y}" rx="45" ry="5" fill="#7dd3fc" opacity="{0.85 if clamped > 1 else 0}"/>
            </g>
            <line x1="104" y1="91" x2="116" y2="91" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <text x="120" y="94" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="700">75%</text>
            <line x1="104" y1="133" x2="116" y2="133" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <text x="120" y="136" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="700">50%</text>
            <line x1="104" y1="174" x2="116" y2="174" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <text x="120" y="177" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="700">25%</text>
            <path d="M 56 26 L 94 26 L 94 50 Q 120 58 120 85 L 120 215 Q 120 228 106 228 L 44 228 Q 30 228 30 215 L 30 85 Q 30 58 56 50 Z" fill="url(#wbGlass)" stroke="#38bdf8" stroke-width="2" opacity="0.9"/>
        </svg>
    </div>
    """


# ==============================================================================
# 4. INITIALIZE SESSION STATE
# ==============================================================================
default_avatar_key = list(AVATARS.keys())[2]  # Adult default

if "active_avatar_key" not in st.session_state:
    st.session_state.active_avatar_key = default_avatar_key

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = AVATARS[default_avatar_key]["recommended_ml"]

if "total_intake" not in st.session_state:
    st.session_state.total_intake = 0

if "logs" not in st.session_state:
    st.session_state.logs = []

if "celebrated" not in st.session_state:
    st.session_state.celebrated = False

if "show_reset_confirm" not in st.session_state:
    st.session_state.show_reset_confirm = False


# ==============================================================================
# 5. BUSINESS LOGIC & CALLBACKS
# ==============================================================================
def log_water(amount: int, label: str):
    if amount > 0:
        st.session_state.total_intake += amount
        st.session_state.logs.append({
            "Time": datetime.now().strftime("%I:%M %p"),
            "Entry": label,
            "Amount": f"+{amount} ml",
            "Total": f"{st.session_state.total_intake} ml"
        })
        st.toast(f"Logged +{amount} ml ({label})!", icon="💧")

def undo_drink():
    if st.session_state.logs:
        last = st.session_state.logs.pop()
        amt = int(last["Amount"].replace("+", "").replace(" ml", "").strip())
        st.session_state.total_intake = max(0, st.session_state.total_intake - amt)
        st.toast(f"Undid -{amt} ml", icon="↩️")

def reset_counters():
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated = False
    st.session_state.show_reset_confirm = False
    st.toast("Counters reset for a fresh day!", icon="🔄")

def on_avatar_changed():
    selected = st.session_state.avatar_radio
    st.session_state.active_avatar_key = selected
    st.session_state.daily_goal = AVATARS[selected]["recommended_ml"]


# Computations
remaining_needed = max(0, st.session_state.daily_goal - st.session_state.total_intake)
pct_progress = round((st.session_state.total_intake / st.session_state.daily_goal) * 100, 1) if st.session_state.daily_goal > 0 else 0.0

if pct_progress >= 100.0 and not st.session_state.celebrated:
    st.balloons()
    st.session_state.celebrated = True
elif pct_progress < 100.0:
    st.session_state.celebrated = False


# ==============================================================================
# 6. HEADER
# ==============================================================================
st.markdown("""
<div class="brand-banner">
    <div class="brand-title">💧 WaterBuddy</div>
    <div class="brand-tag">Daily Hydration Companion</div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# 7. TOP PANEL: AVATAR PROFILE & TARGET GOAL (CLEAN & ALIGNED)
# ==============================================================================
with st.container(border=True):
    col_av, col_target = st.columns([6, 4], gap="medium")
    
    with col_av:
        st.markdown("**👤 Select Your Avatar Profile:**")
        st.radio(
            "Avatar",
            options=list(AVATARS.keys()),
            index=list(AVATARS.keys()).index(st.session_state.active_avatar_key),
            horizontal=True,
            key="avatar_radio",
            on_change=on_avatar_changed,
            label_visibility="collapsed"
        )
        active_av = AVATARS[st.session_state.active_avatar_key]
        st.caption(f"💡 *{active_av['name']}: {active_av['hint']}*")

    with col_target:
        st.markdown("**🎯 Daily Water Target:**")
        adj_col1, adj_col2 = st.columns([3, 2])
        with adj_col1:
            st.session_state.daily_goal = st.number_input(
                "Daily Target (ml)",
                min_value=500,
                max_value=5000,
                value=st.session_state.daily_goal,
                step=100,
                label_visibility="collapsed"
            )
        with adj_col2:
            st.markdown(f"<div style='margin-top:6px; font-weight:700; color:#0369a1;'>{active_av['cups']}</div>", unsafe_allow_html=True)


# ==============================================================================
# 8. BALANCED TWO-COLUMN DASHBOARD (INTUITIVE & ALIGNED)
# ==============================================================================
col_left, col_right = st.columns([5, 5], gap="large")

# ------------------------------------------------------------------------------
# LEFT COLUMN: THE VISUAL CORE (BOTTLE + TURTLE MASCOT)
# ------------------------------------------------------------------------------
with col_left:
    with st.container(border=True):
        st.markdown("<div style='text-align:center; font-weight:800; color:#1b4332; font-size:1.1rem; margin-bottom:4px;'>💧 Animated Water Bottle</div>", unsafe_allow_html=True)
        
        # Self-contained Translucent Bottle SVG
        st.markdown(render_translucent_bottle(pct_progress), unsafe_allow_html=True)

        # Contextual Motivational Caption (Screens 1, 2, 3)
        if pct_progress >= 100.0:
            b_msg, b_sub = "Goal achieved! Fantastic job!", "100% of daily hydration reached"
        elif pct_progress >= 50.0:
            b_msg, b_sub = "Halfway there!", "Logged water keeping you energized"
        elif pct_progress >= 20.0:
            b_msg, b_sub = "Great start!", "Animated water rising steadily"
        else:
            b_msg, b_sub = "Ready to start!", "Take your first sip today"

        st.markdown(f"""
        <div class="bottle-caption">{b_msg}</div>
        <div class="bottle-sub">{b_sub}</div>
        """, unsafe_allow_html=True)

        # Mascot Card (Storyboard Panel 6)
        t_svg, t_title, t_desc = render_turtle_mascot(pct_progress)
        st.markdown(f"""
        <div class="mascot-box">
            {t_svg}
            <div class="mascot-title">{t_title}</div>
            <p class="mascot-desc">{t_desc}</p>
        </div>
        """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# RIGHT COLUMN: ACTION & LOGGING (CLEAR & EFFORTLESS)
# ------------------------------------------------------------------------------
with col_right:
    # 1. LIVE METRICS & PROGRESS
    with st.container(border=True):
        st.markdown("<div style='font-weight:800; color:#1b4332; margin-bottom:8px;'>📊 Hydration Progress</div>", unsafe_allow_html=True)
        
        # Metric Boxes
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-box">
                <div class="metric-lbl">Total Drunk</div>
                <div class="metric-val" style="color:#0284c7;">{st.session_state.total_intake:,} <span style="font-size:0.75rem;">ml</span></div>
            </div>
            <div class="metric-box">
                <div class="metric-lbl">Remaining</div>
                <div class="metric-val" style="color:#16a34a;">{remaining_needed:,} <span style="font-size:0.75rem;">ml</span></div>
            </div>
            <div class="metric-box">
                <div class="metric-lbl">Progress</div>
                <div class="metric-val" style="color:#d97706;">{pct_progress}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(min(pct_progress / 100.0, 1.0))

    # 2. LOG WATER INTAKE
    with st.container(border=True):
        st.markdown("<div style='font-weight:800; color:#1b4332; margin-bottom:8px;'>🥤 Quick Log Water</div>", unsafe_allow_html=True)

        # Big primary +250ml Glass button (Storyboard Screen 5)
        if st.button("➕ 250 ml (Standard Glass)", use_container_width=True, type="primary"):
            log_water(250, "Glass (250 ml)")
            st.rerun()

        # Secondary presets
        p1, p2 = st.columns(2)
        with p1:
            if st.button("➕ 100 ml (Cup)", use_container_width=True):
                log_water(100, "Cup (100 ml)")
                st.rerun()
        with p2:
            if st.button("➕ 500 ml (Bottle)", use_container_width=True):
                log_water(500, "Bottle (500 ml)")
                st.rerun()

        # Custom entry (Storyboard Screen 6)
        st.markdown("<div style='font-size:0.82rem; font-weight:700; color:#475569; margin-top:8px;'>Custom Amount:</div>", unsafe_allow_html=True)
        cin1, cin2 = st.columns([3, 2])
        with cin1:
            custom_ml = st.number_input("Amount (ml)", min_value=20, max_value=2000, value=250, step=50, label_visibility="collapsed")
        with cin2:
            if st.button("Add entry", use_container_width=True):
                log_water(custom_ml, f"Custom ({custom_ml} ml)")
                st.rerun()

    # 3. END-OF-DAY SUMMARY & RESET (STORYBOARD SCREENS 8 & 9)
    with st.container(border=True):
        st.markdown("<div style='font-weight:800; color:#1b4332; margin-bottom:6px;'>📋 End-of-Day Summary</div>", unsafe_allow_html=True)
        
        status_txt = "🎉 Excellent job! You hit 100% of your target. Regular hydration is keeping you energized!" if pct_progress >= 100.0 else "Good progress! Keep regular sips to reach your full daily target."
        
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:10px; font-size:0.88rem; margin-bottom:10px;">
            <strong>Intake:</strong> {st.session_state.total_intake:,} ml of {st.session_state.daily_goal:,} ml (<strong>{pct_progress}%</strong>)<br>
            <span style="color:#15803d; font-size:0.82rem;">{status_txt}</span>
        </div>
        """, unsafe_allow_html=True)

        # Undo & New Day Buttons
        b_undo, b_reset = st.columns(2)
        with b_undo:
            if st.button("↩️ Undo Last", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
                undo_drink()
                st.rerun()
        with b_reset:
            if not st.session_state.show_reset_confirm:
                if st.button("🔄 New Day / Reset", use_container_width=True):
                    st.session_state.show_reset_confirm = True
                    st.rerun()

        # Storyboard Screen 8 Confirmation
        if st.session_state.show_reset_confirm:
            st.warning("⚠️ **New Day**: Reset all counters for today?")
            conf1, conf2 = st.columns(2)
            with conf1:
                if st.button("✅ [Yes] Reset", use_container_width=True, type="primary"):
                    reset_counters()
                    st.rerun()
            with conf2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_reset_confirm = False
                    st.rerun()


# ==============================================================================
# 9. TODAY'S ACTIVITY LOG TABLE (COLLAPSIBLE / CLEAN)
# ==============================================================================
with st.expander("📜 View Today's Intake History Log", expanded=False):
    if st.session_state.logs:
        df_history = pd.DataFrame(reversed(st.session_state.logs))
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    else:
        st.info("No drinks logged yet today.")
