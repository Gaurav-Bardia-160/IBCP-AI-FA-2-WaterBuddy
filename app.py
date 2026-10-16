"""
WaterBuddy - Interactive Water Hydration Tracker
Faithfully designed and built according to the FA-1 Storyboard.

Storyboard Architecture:
1. User Avatars: Child, Teen, Adult, Senior (Interactive profiles)
2. Daily Recommended Water Targets (with standard suggestions & cups conversion)
3. App Data Logic: Age-based auto-goal with option to adjust
4. Python Logic Updates: Total intake (++), remaining needed (++), % progress
5. Turtle Mascot Milestone System:
   - Progress < 20%: Neutral resting turtle
   - Progress >= 20%: Avatar smiles 😊
   - Progress >= 75%: Avatar waves 👋
   - Total >= Goal: Celebration! 🎉
6. Bottle Visualization: Animated translucent bottle filling with water & dynamic messages
7. Log Activity: Circular +250 ml quick log & custom "Your entry" input
8. End-of-Day Summary & New Day reset confirmation modal
"""

import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Auto-launcher for running directly via 'python app.py'
if get_script_run_ctx() is None:
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())

import streamlit as st
import random
from datetime import datetime
import pandas as pd

# ==============================================================================
# 1. PAGE SETUP & FA-1 STORYBOARD PASTEL THEME
# ==============================================================================
st.set_page_config(
    page_title="WaterBuddy",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling matching the Soft Mint-Green & Aqua Palette of the Storyboard
st.html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Nunito:wght@600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Overall Background and Layout */
    .stApp {
        background: linear-gradient(180deg, #f0fdf4 0%, #ecfdf5 50%, #f0f9ff 100%);
    }

    .block-container {
        max-width: 1140px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Storyboard Top Title */
    .storyboard-title-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.8rem 1.5rem;
        background: linear-gradient(135deg, #d8f3dc 0%, #b7e4c7 100%);
        border: 2px solid #95d5b2;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(82, 183, 136, 0.15);
    }
    .storyboard-title {
        font-family: 'Nunito', sans-serif;
        font-size: 2.3rem;
        font-weight: 900;
        color: #1b4332;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        text-shadow: 1px 2px 0px rgba(255,255,255,0.8);
    }
    .storyboard-tag {
        font-size: 0.95rem;
        font-weight: 700;
        color: #2d6a4f;
        background: rgba(255, 255, 255, 0.8);
        padding: 6px 16px;
        border-radius: 30px;
        border: 1px solid #74c69d;
    }

    /* Panel Card Containers */
    .sb-card {
        background: #ffffff;
        border: 1.5px solid #d8f3dc;
        border-radius: 18px;
        padding: 1.25rem;
        box-shadow: 0 6px 20px rgba(45, 106, 79, 0.04);
        margin-bottom: 1.25rem;
        height: 100%;
    }
    .sb-card-header {
        font-family: 'Nunito', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        color: #1b4332;
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 2px solid #e8f5e9;
        padding-bottom: 0.5rem;
    }

    /* User Avatars Grid */
    .avatar-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        text-align: center;
    }
    .avatar-item {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 14px;
        padding: 10px 6px;
        transition: all 0.2s ease;
    }
    .avatar-item.active {
        background: #ecfdf5;
        border-color: #52b788;
        box-shadow: 0 4px 12px rgba(82, 183, 136, 0.2);
    }
    .avatar-icon {
        font-size: 2.2rem;
        display: block;
        margin-bottom: 4px;
    }
    .avatar-name {
        font-weight: 700;
        font-size: 0.9rem;
        color: #1e293b;
    }
    .avatar-target {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
    }

    /* Daily Targets List */
    .target-pill {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 8px 14px;
        margin-bottom: 8px;
        font-size: 0.88rem;
    }
    .target-role {
        font-weight: 700;
        color: #166534;
    }
    .target-cups {
        color: #0369a1;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Turtle Mascot Card */
    .mascot-display-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #86efac;
        border-radius: 18px;
        padding: 1.2rem;
        text-align: center;
        margin-top: 1rem;
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.08);
    }
    .mascot-title {
        font-family: 'Nunito', sans-serif;
        font-size: 1.1rem;
        font-weight: 800;
        color: #14532d;
        margin-top: 6px;
    }
    .mascot-desc {
        font-size: 0.9rem;
        color: #166534;
        margin-top: 4px;
        margin-bottom: 0;
        line-height: 1.4;
    }

    /* Circular +250ml Button Styling */
    .circular-log-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: linear-gradient(135deg, #52b788 0%, #2d6a4f 100%);
        color: white;
        border: 6px solid #b7e4c7;
        box-shadow: 0 10px 25px rgba(45, 106, 79, 0.25);
        cursor: pointer;
        margin: 10px auto;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .circular-log-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 14px 30px rgba(45, 106, 79, 0.35);
    }
    .circular-val {
        font-family: 'Nunito', sans-serif;
        font-size: 1.7rem;
        font-weight: 900;
        line-height: 1;
    }
    .circular-sub {
        font-size: 0.8rem;
        font-weight: 700;
        opacity: 0.9;
        margin-top: 4px;
    }

    /* End-of-Day Summary Card (Screen 9) */
    .summary-report-card {
        background: #ffffff;
        border: 2px solid #74c69d;
        border-radius: 18px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 8px 24px rgba(45, 106, 79, 0.08);
        position: relative;
    }
    .summary-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #e8f5e9;
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
    }
    .summary-title {
        font-family: 'Nunito', sans-serif;
        font-size: 1.2rem;
        font-weight: 900;
        color: #1b4332;
    }
    .summary-metric-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 1rem;
    }
    .summary-metric {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
    }
    .summary-metric-val {
        font-size: 1.3rem;
        font-weight: 800;
        color: #0f172a;
    }
    .summary-metric-lbl {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }
    .summary-badge-success {
        background: #dcfce7;
        color: #15803d;
        border: 1.5px solid #86efac;
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 700;
        font-size: 0.92rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Bottle Dynamic Motivational Caption */
    .bottle-caption {
        font-family: 'Nunito', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: #0369a1;
        text-align: center;
        margin-top: 8px;
    }
    .bottle-subcaption {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-align: center;
        margin-bottom: 6px;
    }

    /* Button Tweaks */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.15s ease;
    }
</style>
""")


# ==============================================================================
# 2. STORYBOARD DATA & USER PERSONAS
# ==============================================================================
# Exact 4 Avatars and Guidelines from Storyboard
AVATARS = {
    "Child": {
        "icon": "🧒",
        "recommended_ml": 1600,
        "cups": "6–7 cups",
        "desc": "Active growing bodies requiring regular hydration during school & play."
    },
    "Teen": {
        "icon": "👧",
        "recommended_ml": 2000,
        "cups": "8–10 cups",
        "desc": "High energy & study routines demanding consistent fluid balance."
    },
    "Adult": {
        "icon": "🧑",
        "recommended_ml": 2500,
        "cups": "8–10 cups",
        "desc": "Supports peak mental focus, daily metabolism, and vitality."
    },
    "Senior": {
        "icon": "👴",
        "recommended_ml": 2000,
        "cups": "4–10 cups",
        "desc": "Thirst cues decline with age; scheduled drinking is essential."
    }
}


# ==============================================================================
# 3. VECTOR GRAPHICS (TURTLE MASCOT & TRANSLUCENT BOTTLE)
# ==============================================================================

def render_turtle_mascot_svg(pct: float) -> str:
    """
    Renders the exact Turtle Mascot from the Storyboard with 3 distinct milestone states:
    - If progress < 20%: Resting / Neutral Turtle 🐢
    - If progress >= 20%: Avatar smiles 😊
    - If progress >= 75%: Avatar waves 👋
    - If total >= goal: Celebration with sparkles 🎉
    """
    # Determine state
    if pct >= 100.0:
        state = "celebration"
        state_title = "Celebration Milestone!"
        state_desc = "Awesome job! You reached 100% of your daily water goal!"
    elif pct >= 75.0:
        state = "waving"
        state_title = "Avatar Waves 👋"
        state_desc = f"You are at {pct}%! Turtle is happily waving you forward to the finish line!"
    elif pct >= 20.0:
        state = "smiling"
        state_title = "Avatar Smiles 😊"
        state_desc = f"Great start ({pct}%)! Turtle is smiling at your healthy habit."
    else:
        state = "resting"
        state_title = "Turtle is Resting 🐢"
        state_desc = "Take your first sip (reach 20%) to see Turtle smile!"

    # Arm / Flipper positioning based on state
    if state == "waving":
        # Right flipper raised high in waving gesture
        right_flipper = '<path d="M 125 70 Q 145 45 155 35 Q 162 42 152 60 Q 140 78 128 85 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'
    elif state == "celebration":
        # Both flippers raised in celebration
        right_flipper = '<path d="M 125 70 Q 145 45 155 35 Q 162 42 152 60 Q 140 78 128 85 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'
    else:
        # Normal relaxed flipper
        right_flipper = '<path d="M 125 85 Q 145 92 148 102 Q 140 108 125 98 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>'

    # Mouth and Eyes based on state
    if state in ["smiling", "waving"]:
        # Smiling eyes and curved happy mouth
        mouth = '<path d="M 130 65 Q 138 74 146 65" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
        eyes = '''
        <circle cx="132" cy="52" r="3.5" fill="#1b4332"/>
        <circle cx="146" cy="52" r="3.5" fill="#1b4332"/>
        <circle cx="133.5" cy="50.5" r="1.2" fill="#ffffff"/>
        <circle cx="147.5" cy="50.5" r="1.2" fill="#ffffff"/>
        <ellipse cx="128" cy="60" rx="3" ry="1.5" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="149" cy="60" rx="3" ry="1.5" fill="#fca5a5" opacity="0.6"/>
        '''
    elif state == "celebration":
        # Joyful open mouth & celebration stars
        mouth = '<path d="M 130 63 Q 138 78 146 63 Z" stroke="#1b4332" stroke-width="2" fill="#e11d48"/>'
        eyes = '''
        <path d="M 128 53 Q 133 48 136 53" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <path d="M 142 53 Q 147 48 150 53" stroke="#1b4332" stroke-width="2.5" fill="none" stroke-linecap="round"/>
        <ellipse cx="128" cy="60" rx="3.5" ry="2" fill="#fca5a5"/>
        <ellipse cx="150" cy="60" rx="3.5" ry="2" fill="#fca5a5"/>
        <!-- Celebration Sparkles / Stars -->
        <polygon points="160,20 163,27 170,28 165,33 166,40 160,36 154,40 155,33 150,28 157,27" fill="#f59e0b"/>
        <polygon points="40,25 42,30 47,31 43,35 44,40 40,37 36,40 37,35 33,31 38,30" fill="#38bdf8"/>
        <circle cx="145" cy="18" r="3" fill="#ec4899"/>
        <circle cx="55" cy="20" r="2.5" fill="#10b981"/>
        '''
    else:
        # Neutral resting face
        mouth = '<path d="M 132 65 Q 138 68 144 65" stroke="#1b4332" stroke-width="2" fill="none" stroke-linecap="round"/>'
        eyes = '''
        <circle cx="132" cy="53" r="3" fill="#1b4332"/>
        <circle cx="146" cy="53" r="3" fill="#1b4332"/>
        <circle cx="133" cy="52" r="1" fill="#ffffff"/>
        <circle cx="147" cy="52" r="1" fill="#ffffff"/>
        '''

    svg = f"""
    <div style="display:flex; justify-content:center; align-items:center; padding: 4px 0;">
        <svg width="190" height="135" viewBox="0 0 190 135" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Back Feet -->
            <ellipse cx="48" cy="100" rx="14" ry="9" fill="#52b788" stroke="#2d6a4f" stroke-width="2.5"/>
            <ellipse cx="108" cy="100" rx="14" ry="9" fill="#52b788" stroke="#2d6a4f" stroke-width="2.5"/>

            <!-- Tail -->
            <path d="M 28 85 Q 15 88 18 95 Q 26 95 32 89 Z" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>

            <!-- Turtle Shell Body -->
            <ellipse cx="78" cy="75" rx="52" ry="40" fill="#2d6a4f" stroke="#1b4332" stroke-width="3"/>
            <ellipse cx="78" cy="72" rx="46" ry="34" fill="#40916c"/>

            <!-- Shell Scutes / Hexagonal Patterns -->
            <polygon points="78,48 93,56 93,72 78,80 63,72 63,56" fill="#52b788" stroke="#2d6a4f" stroke-width="2"/>
            <polygon points="78,80 93,88 93,98 78,102 63,98 63,88" fill="#52b788" stroke="#2d6a4f" stroke-width="1.8"/>
            <polygon points="108,60 118,66 118,78 108,84 96,78 96,66" fill="#74c69d" stroke="#2d6a4f" stroke-width="1.8"/>
            <polygon points="48,60 60,66 60,78 48,84 38,78 38,66" fill="#74c69d" stroke="#2d6a4f" stroke-width="1.8"/>

            <!-- Front Left Leg -->
            <ellipse cx="70" cy="105" rx="14" ry="8" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>

            <!-- Front Right Flipper (Animated Gesture) -->
            {right_flipper}

            <!-- Head & Neck -->
            <path d="M 112 75 Q 120 65 128 62 L 132 82 Q 122 84 115 80 Z" fill="#74c69d"/>
            <ellipse cx="138" cy="58" rx="18" ry="17" fill="#74c69d" stroke="#2d6a4f" stroke-width="2.5"/>

            <!-- Eyes, Cheeks, and Mouth -->
            {eyes}
            {mouth}
        </svg>
    </div>
    """
    return svg, state_title, state_desc


def render_translucent_bottle_svg(pct: float) -> str:
    """
    Renders the exact 3D Translucent Blue Bottle from the Storyboard (Screens 1, 2, 3, 7).
    """
    clamped = min(max(pct, 0.0), 100.0)
    # Total inside fillable height is 165px (from y=215 to y=50)
    fill_h = (clamped / 100.0) * 165
    water_y = 215 - fill_h

    return (
        '<div style="display:flex; justify-content:center; align-items:center; padding: 6px 0;">'
        '<svg width="150" height="255" viewBox="0 0 150 255" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<linearGradient id="sbWaterGrad" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#38bdf8" />'
        '<stop offset="100%" stop-color="#0284c7" />'
        '</linearGradient>'
        '<linearGradient id="sbGlassGrad" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="white" stop-opacity="0.6"/>'
        '<stop offset="40%" stop-color="white" stop-opacity="0.1"/>'
        '<stop offset="100%" stop-color="white" stop-opacity="0.4"/>'
        '</linearGradient>'
        '<clipPath id="sbBottleClip">'
        '<path d="M 56 26 L 94 26 L 94 50 Q 120 58 120 85 L 120 215 Q 120 228 106 228 L 44 228 Q 30 228 30 215 L 30 85 Q 30 58 56 50 Z" />'
        '</clipPath>'
        '</defs>'
        # Cap
        '<rect x="58" y="12" width="34" height="15" rx="4" fill="#0284c7"/>'
        '<rect x="55" y="24" width="40" height="4" rx="2" fill="#38bdf8"/>'
        # Bottle Body Background
        '<path d="M 56 26 L 94 26 L 94 50 Q 120 58 120 85 L 120 215 Q 120 228 106 228 L 44 228 Q 30 228 30 215 L 30 85 Q 30 58 56 50 Z" fill="#f0f9ff" stroke="#bae6fd" stroke-width="2.5"/>'
        # Water Fill Level
        '<g clip-path="url(#sbBottleClip)">'
        f'<rect x="25" y="{water_y}" width="100" height="{fill_h + 30}" fill="url(#sbWaterGrad)"/>'
        f'<ellipse cx="75" cy="{water_y}" rx="45" ry="5" fill="#7dd3fc" opacity="{0.85 if clamped > 1 else 0}"/>'
        '</g>'
        # Graduation lines
        '<line x1="104" y1="91" x2="116" y2="91" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>'
        '<text x="120" y="94" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="700">75%</text>'
        '<line x1="104" y1="133" x2="116" y2="133" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>'
        '<text x="120" y="136" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="700">50%</text>'
        '<line x1="104" y1="174" x2="116" y2="174" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>'
        '<text x="120" y="177" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="700">25%</text>'
        # Glass Reflection
        '<path d="M 56 26 L 94 26 L 94 50 Q 120 58 120 85 L 120 215 Q 120 228 106 228 L 44 228 Q 30 228 30 215 L 30 85 Q 30 58 56 50 Z" fill="url(#sbGlassGrad)" stroke="#38bdf8" stroke-width="2" opacity="0.9"/>'
        '</svg>'
        '</div>'
    )


# ==============================================================================
# 4. SESSION STATE INITIALIZATION
# ==============================================================================
if "active_avatar" not in st.session_state:
    st.session_state.active_avatar = "Adult"

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = AVATARS["Adult"]["recommended_ml"]

if "total_intake" not in st.session_state:
    st.session_state.total_intake = 0

if "logs" not in st.session_state:
    st.session_state.logs = []

if "celebrated" not in st.session_state:
    st.session_state.celebrated = False

if "show_reset_confirm" not in st.session_state:
    st.session_state.show_reset_confirm = False


# ==============================================================================
# 5. CORE BUSINESS LOGIC (FA-1 APP DATA LOGIC)
# ==============================================================================
def log_water_amount(amount: int, label: str):
    """User logged water intake -> +amount -> Python logic updates"""
    if amount > 0:
        st.session_state.total_intake += amount
        st.session_state.logs.append({
            "Time": datetime.now().strftime("%I:%M %p"),
            "Entry": label,
            "Amount Added": f"+{amount} ml",
            "Total So Far": f"{st.session_state.total_intake} ml"
        })
        st.toast(f"Logged +{amount} ml ({label})!", icon="💧")

def undo_last_drink():
    """Removes the most recent logged intake entry."""
    if st.session_state.logs:
        last = st.session_state.logs.pop()
        amt = int(last["Amount Added"].replace("+", "").replace(" ml", "").strip())
        st.session_state.total_intake = max(0, st.session_state.total_intake - amt)
        st.toast(f"Undid -{amt} ml", icon="↩️")

def reset_daily_counters():
    """Storyboard Screen 8: Reset counters for New Day"""
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated = False
    st.session_state.show_reset_confirm = False
    st.toast("Counters reset for a fresh day!", icon="🔄")


# Calculate Metrics (Storyboard: Total ++ amount, Total ++ remaining, % progress)
remaining_needed = max(0, st.session_state.daily_goal - st.session_state.total_intake)
pct_progress = round((st.session_state.total_intake / st.session_state.daily_goal) * 100, 1) if st.session_state.daily_goal > 0 else 0.0

# Celebration balloon trigger
if pct_progress >= 100.0 and not st.session_state.celebrated:
    st.balloons()
    st.session_state.celebrated = True
elif pct_progress < 100.0:
    st.session_state.celebrated = False


# ==============================================================================
# 6. APP HEADER (STORYBOARD TITLE BAR)
# ==============================================================================
st.html("""
<div class="storyboard-title-bar">
    <div class="storyboard-title">
        💧 WaterBuddy
    </div>
    <div class="storyboard-tag">
        Smart Daily Hydration
    </div>
</div>
""")


# ==============================================================================
# 7. TOP ROW: USER AVATARS & WATER TARGETS (STORYBOARD PANELS 1, 2, 3)
# ==============================================================================
row1_left, row1_right = st.columns([6, 5], gap="large")

with row1_left:
    st.html("""
    <div class="sb-card">
        <div class="sb-card-header">
            <span>👤 User Avatars</span>
        </div>
        <p style="font-size:0.85rem; color:#64748b; margin-bottom:10px;">Select your avatar profile to auto-suggest daily target:</p>
    """)

    # 4 Avatar Selection Buttons matching Storyboard Panel 1
    av_col1, av_col2, av_col3, av_col4 = st.columns(4)
    avatars_list = list(AVATARS.keys())

    for idx, (col, av_name) in enumerate(zip([av_col1, av_col2, av_col3, av_col4], avatars_list)):
        with col:
            av_data = AVATARS[av_name]
            is_active = (st.session_state.active_avatar == av_name)
            btn_label = f"{av_data['icon']}\n{av_name}"
            
            if st.button(btn_label, use_container_width=True, type="primary" if is_active else "secondary", key=f"av_btn_{av_name}"):
                st.session_state.active_avatar = av_name
                st.session_state.daily_goal = av_data["recommended_ml"]
                st.rerun()

    # Active Profile Guideline & Option to Adjust
    active_info = AVATARS[st.session_state.active_avatar]
    st.html(f"""
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:10px 14px; margin-top:12px;">
            <div style="font-weight:700; color:#166534; font-size:0.9rem;">
                {active_info['icon']} Selected Profile: {st.session_state.active_avatar}
            </div>
            <div style="font-size:0.82rem; color:#475569; margin-top:3px;">
                {active_info['desc']} (Standard suggestion: <strong>{active_info['recommended_ml']} ml</strong> ≈ {active_info['cups']})
            </div>
        </div>
    </div>
    """)

with row1_right:
    st.html("""
    <div class="sb-card">
        <div class="sb-card-header">
            <span>🎯 Daily Recommended Water Target</span>
        </div>
        <div class="target-pill">
            <span class="target-role">Adults: 2000–2500 ml</span>
            <span class="target-cups">≈ 8–10 cups 🥛🥛</span>
        </div>
        <div class="target-pill">
            <span class="target-role">Teens: 2000–2500 ml</span>
            <span class="target-cups">≈ 8–10 cups 🥛🥛</span>
        </div>
        <div class="target-pill">
            <span class="target-role">Children: 1600–1800 ml</span>
            <span class="target-cups">≈ 6–8 cups 🥛🥛</span>
        </div>
        <div class="target-pill">
            <span class="target-role">Seniors: 1500–2000 ml</span>
            <span class="target-cups">≈ 6–8 cups 🥛🥛</span>
        </div>
    </div>
    """)


# ==============================================================================
# 8. MIDDLE ROW: LOGIC, BOTTLE VISUALS, & TURTLE MASCOT
# ==============================================================================
col_main_left, col_main_center, col_main_right = st.columns([3.8, 3.8, 4.4], gap="large")

# ------------------------------------------------------------------------------
# PANEL A: INTAKE CONTROLS & LOG ACTIVITY (SCREENS 5 & 6)
# ------------------------------------------------------------------------------
with col_main_left:
    st.html("""
    <div class="sb-card">
        <div class="sb-card-header">
            <span>🥤 Log Activity</span>
        </div>
        <p style="font-size:0.85rem; color:#64748b; text-align:center; margin-bottom:8px;">Tap quick log or enter custom amount:</p>
    """)

    # Storyboard Screen 5: Compulsory Circular +250ml Button
    if st.button("➕ 250 ml\n(Standard Glass)", use_container_width=True, type="primary"):
        log_water_amount(250, "Glass (250 ml)")
        st.rerun()

    # Secondary Quick Buttons (+100 ml, +500 ml)
    q1, q2 = st.columns(2)
    with q1:
        if st.button("➕ 100 ml (Cup)", use_container_width=True):
            log_water_amount(100, "Cup (100 ml)")
            st.rerun()
    with q2:
        if st.button("➕ 500 ml (Bottle)", use_container_width=True):
            log_water_amount(500, "Bottle (500 ml)")
            st.rerun()

    # Storyboard Screen 6: "Your entry" & "Add entry" Custom Log
    st.html('<div style="font-size:0.82rem; font-weight:700; color:#1b4332; margin-top:14px; margin-bottom:4px;">Custom Entry (ml):</div>')
    custom_c1, custom_c2 = st.columns([3, 2])
    with custom_c1:
        custom_input = st.number_input(
            "Your entry",
            min_value=20,
            max_value=2000,
            value=250,
            step=50,
            label_visibility="collapsed"
        )
    with custom_c2:
        if st.button("Add entry", use_container_width=True):
            log_water_amount(custom_input, f"Custom ({custom_input} ml)")
            st.rerun()

    # Option to Adjust Daily Target (Storyboard: "Option to adjust")
    st.html('<div style="font-size:0.82rem; font-weight:700; color:#1b4332; margin-top:14px; margin-bottom:4px;">Option to Adjust Daily Goal:</div>')
    adjusted_goal = st.number_input(
        "Adjust Goal",
        min_value=500,
        max_value=5000,
        value=st.session_state.daily_goal,
        step=100,
        label_visibility="collapsed"
    )
    if adjusted_goal != st.session_state.daily_goal:
        st.session_state.daily_goal = adjusted_goal

    # Undo Button
    if st.button("↩️ Undo Last Log", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
        undo_last_drink()
        st.rerun()

    st.html("</div>")


# ------------------------------------------------------------------------------
# PANEL B: TRANSLUCENT BLUE BOTTLE VISUAL (SCREENS 1, 2, 3, 7)
# ------------------------------------------------------------------------------
with col_main_center:
    st.html("""
    <div class="sb-card" style="text-align:center;">
        <div class="sb-card-header" style="justify-content:center;">
            <span>💧 Animated Bottle</span>
        </div>
    """)

    # Dynamic Translucent Blue Bottle
    st.html(render_translucent_bottle_svg(pct_progress))

    # Dynamic Motivational Message below bottle (Screens 1, 2, 3)
    if pct_progress >= 100.0:
        bottle_msg = "Goal achieved! Fantastic job!"
        bottle_sub = "100% of daily hydration reached"
    elif pct_progress >= 50.0:
        bottle_msg = "Halfway there!"
        bottle_sub = "Logged water keeping you energized"
    elif pct_progress >= 20.0:
        bottle_msg = "Great start!"
        bottle_sub = "Animated water rising steadily"
    else:
        bottle_msg = "Ready to start!"
        bottle_sub = "Take your first sip today"

    st.html(f"""
        <div class="bottle-caption">{bottle_msg}</div>
        <div class="bottle-subcaption">{bottle_sub}</div>
    </div>
    """)


# ------------------------------------------------------------------------------
# PANEL C: TURTLE MASCOT & DATA LOGIC (STORYBOARD MILESTONES)
# ------------------------------------------------------------------------------
with col_main_right:
    # 1. Python Data Logic Live Counters
    st.html(f"""
    <div class="sb-card">
        <div class="sb-card-header">
            <span>⚙️ Python Logic Updates</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-bottom:12px;">
            <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:8px 4px; text-align:center;">
                <div style="font-size:0.7rem; color:#166534; font-weight:700;">TOTAL ++</div>
                <div style="font-size:1.15rem; font-weight:800; color:#14532d;">{st.session_state.total_intake:,} <span style="font-size:0.75rem;">ml</span></div>
            </div>
            <div style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:8px 4px; text-align:center;">
                <div style="font-size:0.7rem; color:#0369a1; font-weight:700;">REMAINING</div>
                <div style="font-size:1.15rem; font-weight:800; color:#0284c7;">{remaining_needed:,} <span style="font-size:0.75rem;">ml</span></div>
            </div>
            <div style="background:#fefce8; border:1px solid #fef08a; border-radius:10px; padding:8px 4px; text-align:center;">
                <div style="font-size:0.7rem; color:#854d0e; font-weight:700;">PROGRESS</div>
                <div style="font-size:1.15rem; font-weight:800; color:#a16207;">{pct_progress}%</div>
            </div>
        </div>
    """)

    # Streamlit native progress bar
    st.progress(min(pct_progress / 100.0, 1.0))

    # 2. Turtle Mascot Milestone Display (Middle-Right of Storyboard)
    turtle_svg, t_title, t_desc = render_turtle_mascot_svg(pct_progress)
    st.html(f"""
        <div class="mascot-display-card">
            {turtle_svg}
            <div class="mascot-title">{t_title}</div>
            <div class="mascot-desc">{t_desc}</div>
        </div>
    </div>
    """)


# ==============================================================================
# 9. BOTTOM SECTION: END-OF-DAY SUMMARY & RESET (STORYBOARD SCREENS 8 & 9)
# ==============================================================================
st.markdown("---")
summary_left, summary_right = st.columns([6, 6], gap="large")

# ------------------------------------------------------------------------------
# SCREEN 9: END-OF-DAY SUMMARY REPORT
# ------------------------------------------------------------------------------
with summary_left:
    st.html(f"""
    <div class="summary-report-card">
        <div class="summary-header">
            <div>
                <div class="summary-title">📊 End-of-Day Summary</div>
                <div style="font-size:0.82rem; color:#64748b;">Daily Hydration Report</div>
            </div>
            <div style="font-size:2rem;">🐢</div>
        </div>
        <div class="summary-metric-row">
            <div class="summary-metric">
                <div class="summary-metric-lbl">Total Intake</div>
                <div class="summary-metric-val" style="color:#0284c7;">{st.session_state.total_intake:,} ml</div>
            </div>
            <div class="summary-metric">
                <div class="summary-metric-lbl">Daily Goal</div>
                <div class="summary-metric-val" style="color:#1b4332;">{st.session_state.daily_goal:,} ml</div>
            </div>
        </div>
        <div class="summary-badge-success">
            <strong>{pct_progress}% Achieved!</strong>
            <div style="font-size:0.84rem; font-weight:500; margin-top:2px;">
                {"🎉 Excellent job! You hit 100% of your target. Regular hydration is keeping you energized!" if pct_progress >= 100.0 else "Great progress! Keep regular sips to reach your full target."}
            </div>
        </div>
    </div>
    """)

    # Storyboard Screen 8 & 9: New Day / Reset Modal
    if not st.session_state.show_reset_confirm:
        if st.button("🔄 New Day / Reset Counters", use_container_width=True):
            st.session_state.show_reset_confirm = True
            st.rerun()
    else:
        st.warning("⚠️ **New Day Confirmation**: This will reset your counters for today. Are you sure?")
        r_c1, r_c2 = st.columns(2)
        with r_c1:
            if st.button("✅ [Yes] Reset Now", use_container_width=True, type="primary"):
                reset_daily_counters()
                st.rerun()
        with r_c2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_reset_confirm = False
                st.rerun()


# ------------------------------------------------------------------------------
# TIMELINE AUDIT LOG TABLE
# ------------------------------------------------------------------------------
with summary_right:
    st.html("""
    <div class="sb-card">
        <div class="sb-card-header">
            <span>📜 Today's Logged History</span>
        </div>
    """)

    if st.session_state.logs:
        df_history = pd.DataFrame(reversed(st.session_state.logs))
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    else:
        st.info("No drinks logged yet today. Click **+250 ml** to log your first drink!")

    st.html("</div>")
