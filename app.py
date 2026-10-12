"""
WaterBuddy - Modern Hydration Companion
A sleek, intelligent water tracking web application.
"""

import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

# If run directly via 'python app.py' (or the VS Code Run button), automatically launch via Streamlit
if get_script_run_ctx() is None:
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())

import streamlit as st
import random
from datetime import datetime
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="WaterBuddy",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. POLISHED MODERN CSS DESIGN SYSTEM
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Remove extra top padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
        max-width: 1100px;
    }

    /* Glass Card Styling */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(240, 249, 255, 0.85));
        border: 1px solid rgba(224, 242, 254, 0.9);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(14, 165, 233, 0.08);
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    /* Header Styling */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.8rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #f1f5f9;
    }
    .brand-title {
        font-size: 1.9rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .brand-subtitle {
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 0.2rem;
        font-weight: 500;
    }

    /* Stat Badges */
    .stat-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: #f0f9ff;
        color: #0369a1;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #bae6fd;
    }

    /* Primary Progress Hero Display */
    .progress-hero {
        text-align: center;
        padding: 1rem 0;
    }
    .hero-number {
        font-size: 3.2rem;
        font-weight: 800;
        color: #0369a1;
        line-height: 1;
        letter-spacing: -1px;
    }
    .hero-target {
        font-size: 1.2rem;
        font-weight: 600;
        color: #94a3b8;
    }

    /* Metric Micro-Cards */
    .metric-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 1rem;
    }
    .metric-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 12px;
        text-align: center;
    }
    .metric-box-title {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-box-val {
        color: #0f172a;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 2px;
    }

    /* Mascot Friendly Card */
    .mascot-container {
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(135deg, #f0fdfa, #f0f9ff);
        border: 1px solid #ccfbf1;
        border-radius: 16px;
        padding: 14px 18px;
        margin-top: 1rem;
    }
    .mascot-icon {
        font-size: 2.2rem;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.06));
    }
    .mascot-heading {
        font-weight: 700;
        color: #0f766e;
        font-size: 0.98rem;
        margin: 0;
    }
    .mascot-desc {
        color: #334155;
        font-size: 0.88rem;
        margin-top: 3px;
        margin-bottom: 0;
        line-height: 1.35;
    }

    /* Quick Tip Pill */
    .tip-card {
        background: #fffbeb;
        border: 1px solid #fef3c7;
        border-radius: 14px;
        padding: 12px 16px;
        color: #92400e;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1.2rem;
    }

    /* Streamlit Widget Polishing */
    div[data-testid="stMetricValue"] {
        font-weight: 700 !important;
    }
    div.stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        border: 1px solid #cbd5e1;
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: #0284c7;
        color: #0284c7;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.12);
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7, #2563eb) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
    }
    div.stButton > button[kind="primary"]:hover {
        opacity: 0.92;
        transform: translateY(-1px);
    }

    /* Section Subheadings */
    .section-label {
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #0284c7;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. SCIENTIFIC DATA & CONSTANTS
# ==========================================
AGE_GROUPS = {
    "Kids (6–12 yrs)": {"goal": 1600, "hint": "Growing bodies require regular hydration through school & play."},
    "Teens (13–18 yrs)": {"goal": 2000, "hint": "High energy & study routines demand consistent fluid balance."},
    "Adults (19–50 yrs)": {"goal": 2500, "hint": "Maintains peak mental focus, metabolism, and vitality."},
    "Seniors (65+ yrs)": {"goal": 2000, "hint": "Thirst cues decline with age; scheduled drinking is essential."}
}

HYDRATION_TIPS = [
    "Drinking a tall glass of water right upon waking activates your organs and kickstarts metabolism.",
    "Mild dehydration (as little as 1–2%) can significantly reduce memory, energy, and concentration.",
    "Infuse your bottle with cucumber, fresh mint, or a slice of citrus for natural taste.",
    "Thirst is a delayed signal of dehydration; take small sips consistently throughout the day.",
    "Sip 250 ml of water 30 minutes before workouts to protect muscles and joints.",
    "Herbal teas and high-water fruits like watermelon contribute directly to daily hydration."
]


# ==========================================
# 4. CORE CALCULATION & MASCOT FUNCTIONS
# ==========================================
def get_standard_goal(age_group: str) -> int:
    return AGE_GROUPS.get(age_group, {}).get("goal", 2500)

def calculate_metrics(total_intake: int, daily_goal: int):
    remaining = max(0, daily_goal - total_intake)
    pct = round((total_intake / daily_goal) * 100, 1) if daily_goal > 0 else 0.0
    return remaining, pct

def get_mascot_state(percentage: float):
    if percentage <= 0:
        return "😴", "Buddy is Asleep", "Take your first sip of the day to wake Buddy up and begin!"
    elif percentage < 25:
        return "🌱", "Fresh Start", f"Great first step! You have reached {percentage}% of your daily goal."
    elif percentage < 50:
        return "💧", "In the Flow", f"You're at {percentage}%. Keep up this steady hydration pace!"
    elif percentage < 75:
        return "🌊", "Halfway Hero", f"Past the halfway mark ({percentage}%)! Energy levels are soaring."
    elif percentage < 100:
        return "⭐", "Almost There", f"{percentage}% completed! Just a couple more glasses to victory."
    else:
        return "🏆", "Hydration Champion!", f"Awesome! You hit {percentage}% of your goal! Buddy is cheering for you! 🎉"

def render_sleek_bottle(percentage: float) -> str:
    clamped = min(max(percentage, 0.0), 100.0)
    fill_h = (clamped / 100.0) * 170
    water_y = 225 - fill_h

    return (
        '<div style="display:flex; justify-content:center; align-items:center; padding: 8px 0;">'
        '<svg width="150" height="260" viewBox="0 0 150 260" fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<defs>'
        '<linearGradient id="liquidGrad" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0%" stop-color="#38bdf8" />'
        '<stop offset="100%" stop-color="#0284c7" />'
        '</linearGradient>'
        '<linearGradient id="glassReflection" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="white" stop-opacity="0.55"/>'
        '<stop offset="35%" stop-color="white" stop-opacity="0.1"/>'
        '<stop offset="100%" stop-color="white" stop-opacity="0.35"/>'
        '</linearGradient>'
        '<clipPath id="innerBottleClip">'
        '<path d="M 55 30 L 95 30 L 95 55 Q 120 62 120 90 L 120 220 Q 120 234 106 234 L 44 234 Q 30 234 30 220 L 30 90 Q 30 62 55 55 Z" />'
        '</clipPath>'
        '</defs>'
        '<rect x="58" y="16" width="34" height="14" rx="4" fill="#0369a1"/>'
        '<rect x="54" y="28" width="42" height="4" rx="2" fill="#0ea5e9"/>'
        '<path d="M 55 30 L 95 30 L 95 55 Q 120 62 120 90 L 120 220 Q 120 234 106 234 L 44 234 Q 30 234 30 220 L 30 90 Q 30 62 55 55 Z" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2.5"/>'
        '<g clip-path="url(#innerBottleClip)">'
        f'<rect x="25" y="{water_y}" width="100" height="{fill_h + 30}" fill="url(#liquidGrad)"/>'
        f'<ellipse cx="75" cy="{water_y}" rx="45" ry="5" fill="#7dd3fc" opacity="{0.85 if clamped > 1 else 0}"/>'
        '</g>'
        '<line x1="105" y1="95" x2="116" y2="95" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>'
        '<text x="122" y="98" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="600">75%</text>'
        '<line x1="105" y1="140" x2="116" y2="140" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>'
        '<text x="122" y="143" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="600">50%</text>'
        '<line x1="105" y1="185" x2="116" y2="185" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="2 2"/>'
        '<text x="122" y="188" fill="#64748b" font-size="9" font-family="sans-serif" font-weight="600">25%</text>'
        '<path d="M 55 30 L 95 30 L 95 55 Q 120 62 120 90 L 120 220 Q 120 234 106 234 L 44 234 Q 30 234 30 220 L 30 90 Q 30 62 55 55 Z" fill="url(#glassReflection)" stroke="#38bdf8" stroke-width="2" opacity="0.9"/>'
        '</svg>'
        '</div>'
    )


# ==========================================
# 5. STATE INITIALIZATION
# ==========================================
default_age = list(AGE_GROUPS.keys())[2]  # Adults default
if "age_group" not in st.session_state:
    st.session_state.age_group = default_age

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = get_standard_goal(default_age)

if "total_intake" not in st.session_state:
    st.session_state.total_intake = 0

if "logs" not in st.session_state:
    st.session_state.logs = []

if "tip_idx" not in st.session_state:
    st.session_state.tip_idx = random.randint(0, len(HYDRATION_TIPS) - 1)

if "celebrated" not in st.session_state:
    st.session_state.celebrated = False


# ==========================================
# 6. ACTION CALLBACKS
# ==========================================
def log_intake(ml: int, label: str):
    if ml > 0:
        st.session_state.total_intake += ml
        time_now = datetime.now().strftime("%I:%M %p")
        st.session_state.logs.append({
            "Time": time_now,
            "Item": label,
            "Amount": f"+{ml} ml",
            "Total": f"{st.session_state.total_intake} ml"
        })

def undo_drink():
    if st.session_state.logs:
        last = st.session_state.logs.pop()
        # Parse amount number
        amt = int(last["Amount"].replace("+", "").replace(" ml", "").strip())
        st.session_state.total_intake = max(0, st.session_state.total_intake - amt)

def reset_all():
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated = False

def on_age_select():
    new_age = st.session_state.age_selector_key
    st.session_state.age_group = new_age
    st.session_state.daily_goal = get_standard_goal(new_age)


# ==========================================
# 7. SIDEBAR: CLEAN & MINIMAL TOOLS
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Preferences & Tools")

    # Age Group Selector
    st.html('<div class="section-label">Profile</div>')
    st.selectbox(
        "Age Category",
        options=list(AGE_GROUPS.keys()),
        index=list(AGE_GROUPS.keys()).index(st.session_state.age_group),
        key="age_selector_key",
        on_change=on_age_select,
        label_visibility="collapsed"
    )
    st.caption(f"💡 {AGE_GROUPS[st.session_state.age_group]['hint']}")

    # Manual Goal Customization
    st.html('<div class="section-label" style="margin-top:1rem;">Daily Goal (ml)</div>')
    custom_target = st.number_input(
        "Goal in ml",
        min_value=500,
        max_value=5000,
        value=st.session_state.daily_goal,
        step=100,
        label_visibility="collapsed"
    )
    st.session_state.daily_goal = custom_target

    st.markdown("---")

    # Clean Unit Converter
    st.html('<div class="section-label">Unit Converter</div>')
    conv_tab = st.radio("Convert", ["Cups ↔ mL", "fl oz ↔ mL"], horizontal=True, label_visibility="collapsed")
    if conv_tab == "Cups ↔ mL":
        cups = st.number_input("Cups (1 cup = 250 ml)", min_value=0.5, value=1.0, step=0.5)
        st.caption(f"👉 **{cups} cups = {int(cups * 250)} ml**")
    else:
        floz = st.number_input("Fluid Ounces", min_value=1.0, value=8.0, step=1.0)
        st.caption(f"👉 **{floz} fl oz = {int(floz * 29.57)} ml**")

    st.markdown("---")
    if st.button("🎲 Shuffle Tip", use_container_width=True):
        st.session_state.tip_idx = (st.session_state.tip_idx + 1) % len(HYDRATION_TIPS)
        st.rerun()


# ==========================================
# 8. MAIN VIEW
# ==========================================

# Top Clean Header
st.html("""
<div class="app-header">
    <div>
        <h1 class="brand-title">💧 WaterBuddy</h1>
        <div class="brand-subtitle">Smart daily hydration tracker & habit coach</div>
    </div>
    <div>
        <span class="stat-pill">✨ Daily Goal</span>
    </div>
</div>
""")

# Daily Tip Banner
st.html(f"""
<div class="tip-card">
    <span style="font-size:1.2rem;">💡</span>
    <span>{HYDRATION_TIPS[st.session_state.tip_idx]}</span>
</div>
""")

# Metrics calculation
remaining_ml, percentage = calculate_metrics(st.session_state.total_intake, st.session_state.daily_goal)

# Milestone Balloon Celebration
if percentage >= 100.0 and not st.session_state.celebrated:
    st.balloons()
    st.session_state.celebrated = True
elif percentage < 100.0:
    st.session_state.celebrated = False

# Two-column clean responsive layout
col_left, col_right = st.columns([7, 5], gap="large")

# ------------------------------------------
# LEFT COLUMN: INTERACTION & LOGGING
# ------------------------------------------
with col_left:
    st.html('<div class="section-label">Quick Intake Log</div>')
    
    # 3 Pill buttons
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🥛 +250 ml\n(Glass)", use_container_width=True, type="primary"):
            log_intake(250, "Glass (250 ml)")
            st.rerun()
    with b2:
        if st.button("☕ +100 ml\n(Cup)", use_container_width=True):
            log_intake(100, "Cup (100 ml)")
            st.rerun()
    with b3:
        if st.button("🍶 +500 ml\n(Bottle)", use_container_width=True):
            log_intake(500, "Bottle (500 ml)")
            st.rerun()

    # Custom ml log
    with st.expander("✏️ Custom Amount"):
        c_in1, c_in2 = st.columns([3, 2])
        with c_in1:
            custom_amt = st.number_input("Amount (ml)", min_value=20, max_value=2000, value=200, step=50, label_visibility="collapsed")
        with c_in2:
            if st.button("Add Intake", use_container_width=True):
                log_intake(custom_amt, f"Custom ({custom_amt} ml)")
                st.rerun()

    # History & Manage Buttons
    st.html('<div class="section-label" style="margin-top:1.5rem;">Today\'s Timeline</div>')
    
    if st.session_state.logs:
        df_logs = pd.DataFrame(reversed(st.session_state.logs))
        st.dataframe(df_logs, use_container_width=True, hide_index=True)
    else:
        st.info("No drinks recorded today yet. Tap **+250 ml** to log your first drink!")

    # Undo and Reset controls
    btn_undo_col, btn_reset_col = st.columns(2)
    with btn_undo_col:
        if st.button("↩️ Undo Last", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
            undo_drink()
            st.rerun()
    with btn_reset_col:
        if st.button("🔄 Reset Day", use_container_width=True):
            reset_all()
            st.rerun()


# ------------------------------------------
# RIGHT COLUMN: VISUAL DASHBOARD & MASCOT
# ------------------------------------------
with col_right:
    with st.container(border=True):
        st.html(f"""
        <div class="progress-hero">
            <div class="hero-number">{st.session_state.total_intake:,} <span style="font-size:1.4rem; font-weight:600; color:#64748b;">ml</span></div>
            <div class="hero-target">of {st.session_state.daily_goal:,} ml target ({percentage}%)</div>
        </div>
        """)

        # Sleek progress bar
        st.progress(min(percentage / 100.0, 1.0))

        # Metric micro-boxes
        st.html(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-box-title">Remaining</div>
                <div class="metric-box-val" style="color:#0284c7;">{remaining_ml:,} ml</div>
            </div>
            <div class="metric-box">
                <div class="metric-box-title">Status</div>
                <div class="metric-box-val" style="color:#10b981;">{"Completed! 🎉" if percentage >= 100 else f"{percentage}%"}</div>
            </div>
        </div>
        """)

        # Dynamic Water Bottle Illustration
        st.html(render_sleek_bottle(percentage))

        # Mascot Milestone Feedback
        mascot_icon, mascot_title, mascot_msg = get_mascot_state(percentage)
        st.html(f"""
        <div class="mascot-container">
            <div class="mascot-icon">{mascot_icon}</div>
            <div>
                <div class="mascot-heading">{mascot_title}</div>
                <p class="mascot-desc">{mascot_msg}</p>
            </div>
        </div>
        """)
