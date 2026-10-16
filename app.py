"""
WaterBuddy - Interactive Water Hydration Tracker
Built 100% with pure Streamlit widgets and components (no HTML/CSS).
Faithfully implements all features from the FA-1 Storyboard and FA-2 Rubric:
- 4 Avatars: Child, Teen, Adult, Senior
- Auto-suggested daily targets with manual adjustment option
- Real-time calculations: Total intake, remaining needed, % progress
- Streamlit progress bar with dynamic motivational milestones
- Turtle Mascot milestone reactions (<20% resting, >=20% smile, >=75% wave, 100%+ celebration)
- Compulsory +250ml log button, companion presets, and custom entry
- End-of-Day summary & New Day reset confirmation
"""

import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Auto-launch via Streamlit if executed directly with python app.py
if get_script_run_ctx() is None:
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())

import streamlit as st
from datetime import datetime
import pandas as pd

# ==============================================================================
# 1. PAGE SETUP
# ==============================================================================
st.set_page_config(
    page_title="WaterBuddy",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. STORYBOARD DATA & PRESETS
# ==============================================================================
AVATARS = {
    "🧒 Child (6–12 yrs)": {
        "name": "Child",
        "recommended_ml": 1600,
        "cups": "≈ 6–7 cups (250 ml each)",
        "hint": "Growing children need steady hydration during school, play, and sports."
    },
    "👧 Teen (13–18 yrs)": {
        "name": "Teen",
        "recommended_ml": 2000,
        "cups": "≈ 8–10 cups (250 ml each)",
        "hint": "High energy levels and study routines demand consistent fluid intake."
    },
    "🧑 Adult (19–50 yrs)": {
        "name": "Adult",
        "recommended_ml": 2500,
        "cups": "≈ 8–10 cups (250 ml each)",
        "hint": "Maintains peak cognitive focus, organ vitality, and physical energy."
    },
    "👴 Senior (65+ yrs)": {
        "name": "Senior",
        "recommended_ml": 2000,
        "cups": "≈ 4–10 cups (250 ml each)",
        "hint": "Thirst cues decline with age; scheduled drinking is essential."
    }
}

# ==============================================================================
# 3. SESSION STATE INITIALIZATION
# ==============================================================================
default_avatar_key = list(AVATARS.keys())[2]  # Adult default

if "avatar_choice" not in st.session_state:
    st.session_state.avatar_choice = default_avatar_key

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
# 4. ACTION CALLBACKS
# ==============================================================================
def log_water(amount: int, label: str):
    """Logs water intake and adds timestamped history."""
    if amount > 0:
        st.session_state.total_intake += amount
        st.session_state.logs.append({
            "Time": datetime.now().strftime("%I:%M %p"),
            "Container": label,
            "Amount Added": f"+{amount} ml",
            "Total Accumulated": f"{st.session_state.total_intake} ml"
        })
        st.toast(f"Logged +{amount} ml ({label})!", icon="💧")

def undo_last_drink():
    """Removes the most recent intake entry."""
    if st.session_state.logs:
        last = st.session_state.logs.pop()
        amt = int(last["Amount Added"].replace("+", "").replace(" ml", "").strip())
        st.session_state.total_intake = max(0, st.session_state.total_intake - amt)
        st.toast(f"Removed last log (-{amt} ml)", icon="↩️")

def reset_counters():
    """Resets daily progress for a new day."""
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated = False
    st.session_state.show_reset_confirm = False
    st.toast("Counters reset for a fresh day!", icon="🔄")

def on_avatar_change():
    """Updates the recommended goal when avatar profile changes."""
    selected = st.session_state.avatar_radio_input
    st.session_state.avatar_choice = selected
    st.session_state.daily_goal = AVATARS[selected]["recommended_ml"]


# Core calculations
remaining_needed = max(0, st.session_state.daily_goal - st.session_state.total_intake)
pct_progress = round((st.session_state.total_intake / st.session_state.daily_goal) * 100, 1) if st.session_state.daily_goal > 0 else 0.0

# Celebration balloons trigger at 100%
if pct_progress >= 100.0 and not st.session_state.celebrated:
    st.balloons()
    st.session_state.celebrated = True
elif pct_progress < 100.0:
    st.session_state.celebrated = False


# ==============================================================================
# 5. APP HEADER
# ==============================================================================
st.title("💧 WaterBuddy")
st.caption("Smart Daily Hydration Tracker • 100% Pure Streamlit")

# ==============================================================================
# 6. TOP SECTION: USER AVATAR & DAILY TARGET (STORYBOARD PANELS 1, 2, 3)
# ==============================================================================
with st.container(border=True):
    st.subheader("👤 User Profile & Daily Target")
    
    col_av, col_goal = st.columns([6, 4], gap="medium")
    
    with col_av:
        st.write("**Select Your Avatar:**")
        selected_av = st.radio(
            "Select Avatar",
            options=list(AVATARS.keys()),
            index=list(AVATARS.keys()).index(st.session_state.avatar_choice),
            horizontal=True,
            key="avatar_radio_input",
            on_change=on_avatar_change,
            label_visibility="collapsed"
        )
        active_info = AVATARS[selected_av]
        st.info(f"💡 **{active_info['name']} Target**: {active_info['hint']}")

    with col_goal:
        st.write("**Daily Water Target (ml):**")
        st.session_state.daily_goal = st.number_input(
            "Custom Goal in ml",
            min_value=500,
            max_value=5000,
            value=st.session_state.daily_goal,
            step=100,
            label_visibility="collapsed",
            help="You can manually adjust your daily target if needed."
        )
        st.caption(f"Standard guideline: **{active_info['recommended_ml']} ml** ({active_info['cups']})")


# ==============================================================================
# 7. MAIN SECTION: 2 BALANCED COLUMNS
# ==============================================================================
col_left, col_right = st.columns([5, 5], gap="large")

# ------------------------------------------------------------------------------
# LEFT COLUMN: HYDRATION PROGRESS & TURTLE MASCOT
# ------------------------------------------------------------------------------
with col_left:
    # 1. LIVE HYDRATION PROGRESS
    with st.container(border=True):
        st.subheader("📊 Live Hydration Progress")
        
        # 3 Aligned Metrics (Storyboard: Total ++ amount, remaining needed, % progress)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Drunk", f"{st.session_state.total_intake} ml")
        m2.metric("Remaining", f"{remaining_needed} ml")
        m3.metric("Progress", f"{pct_progress}%")
        
        # Streamlit Native Progress Bar (Compulsory Feature)
        progress_val = min(pct_progress / 100.0, 1.0)
        st.progress(progress_val)
        
        # Motivational Milestone Feedback below progress bar (Storyboard Screens 1, 2, 3)
        if pct_progress >= 100.0:
            st.success("🏆 **Goal Achieved! Fantastic job!** (100% of daily target reached)")
        elif pct_progress >= 75.0:
            st.success(f"⭐ **Almost at the finish line!** ({pct_progress}% completed)")
        elif pct_progress >= 50.0:
            st.info(f"🌊 **Halfway there!** ({pct_progress}% completed - keep up the great pace!)")
        elif pct_progress >= 20.0:
            st.info(f"🌱 **Great start!** ({pct_progress}% completed - water level rising steadily)")
        else:
            st.write("💧 **Ready to start!** Take your first sip today to begin tracking.")

    # 2. TURTLE MASCOT MILESTONE SYSTEM (STORYBOARD PANEL 6)
    with st.container(border=True):
        st.subheader("🐢 Turtle Mascot")
        
        if pct_progress >= 100.0:
            st.markdown("### 🐢🎉✨ **Celebration!**")
            st.success("Awesome job! You reached 100% of your daily water goal! Turtle is celebrating with you!")
        elif pct_progress >= 75.0:
            st.markdown("### 🐢👋 **Avatar Waves!**")
            st.info(f"You're at {pct_progress}%! Turtle is happily waving hello and cheering you to the finish line!")
        elif pct_progress >= 20.0:
            st.markdown("### 🐢😊 **Avatar Smiles!**")
            st.info(f"Great start ({pct_progress}%)! Turtle is smiling at your healthy routine.")
        else:
            st.markdown("### 🐢😴 **Turtle is Resting**")
            st.write("Take your first sip (reach 20% progress) to wake Turtle up and see him smile!")


# ------------------------------------------------------------------------------
# RIGHT COLUMN: LOGGING & SUMMARY
# ------------------------------------------------------------------------------
with col_right:
    # 1. LOG WATER INTAKE (STORYBOARD SCREENS 5 & 6)
    with st.container(border=True):
        st.subheader("🥤 Log Water Intake")
        
        # Compulsory +250ml Glass Button (Screen 5)
        if st.button("➕ 250 ml (Standard Glass)", use_container_width=True, type="primary"):
            log_water(250, "Glass (250 ml)")
            st.rerun()
            
        # Companion presets
        p1, p2 = st.columns(2)
        with p1:
            if st.button("➕ 100 ml (Cup)", use_container_width=True):
                log_water(100, "Cup (100 ml)")
                st.rerun()
        with p2:
            if st.button("➕ 500 ml (Bottle)", use_container_width=True):
                log_water(500, "Bottle (500 ml)")
                st.rerun()
                
        # Custom Entry (Screen 6)
        st.write("**Log Custom Amount:**")
        cin1, cin2 = st.columns([3, 2])
        with cin1:
            custom_ml = st.number_input(
                "Amount in ml",
                min_value=20,
                max_value=2000,
                value=250,
                step=50,
                label_visibility="collapsed"
            )
        with cin2:
            if st.button("Add entry", use_container_width=True):
                log_water(custom_ml, f"Custom ({custom_ml} ml)")
                st.rerun()

    # 2. END-OF-DAY SUMMARY & RESET (STORYBOARD SCREENS 8 & 9)
    with st.container(border=True):
        st.subheader("📋 End-of-Day Summary")
        
        summary_col1, summary_col2 = st.columns(2)
        summary_col1.metric("Total Intake", f"{st.session_state.total_intake} ml")
        summary_col2.metric("Target Goal", f"{st.session_state.daily_goal} ml")
        
        if pct_progress >= 100.0:
            st.success(f"**{pct_progress}% Achieved!** Excellent job! Regular hydration is keeping you energized.")
        else:
            st.info(f"**{pct_progress}% Achieved!** Regular sips throughout the day will help you reach 100%.")

        # Action Buttons
        b_undo, b_reset = st.columns(2)
        with b_undo:
            if st.button("↩️ Undo Last", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
                undo_last_drink()
                st.rerun()
        with b_reset:
            if not st.session_state.show_reset_confirm:
                if st.button("🔄 New Day / Reset", use_container_width=True):
                    st.session_state.show_reset_confirm = True
                    st.rerun()

        # Storyboard Screen 8 Confirmation
        if st.session_state.show_reset_confirm:
            st.warning("⚠️ **New Day Confirmation**: This will reset your counters for today. Are you sure?")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ [Yes] Reset Now", use_container_width=True, type="primary"):
                    reset_counters()
                    st.rerun()
            with c2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_reset_confirm = False
                    st.rerun()


# ==============================================================================
# 8. TODAY'S INTAKE HISTORY LOG
# ==============================================================================
with st.expander("📜 Today's Intake History Log", expanded=False):
    if st.session_state.logs:
        df_history = pd.DataFrame(reversed(st.session_state.logs))
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    else:
        st.info("No drinks logged yet today. Click **+250 ml** to log your first drink!")
