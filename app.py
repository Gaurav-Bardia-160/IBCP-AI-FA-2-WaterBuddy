"""
WaterBuddy - Clean Mobile Hydration App
100% Pure Python & Streamlit (No HTML, No CSS).

Built specifically in a clean, centered mobile-app layout matching
the phone wireframes and features from the FA-1 Storyboard:
- Centered phone container with tab navigation: Today, Log Drink, Summary, Profile
- 4 Avatars: Child, Teen, Adult, Senior
- Standard age goals with manual adjustments
- Live calculations: Total intake, remaining needed, % progress
- Real-time progress bar & milestone messages
- Turtle mascot milestone reactions (<20% resting, >=20% smile, >=75% wave, 100%+ celebration)
- One-touch +250ml quick logging & custom entries
- End-of-Day report & safe New Day reset confirmation
"""

import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Auto-launcher for running directly via 'python app.py'
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
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. STORYBOARD DATA CONSTANTS
# ==============================================================================
AVATARS = {
    "🧒 Child": {
        "full_name": "Child (6–12 yrs)",
        "goal": 1600,
        "cups": "≈ 6–7 cups (250 ml each)",
        "hint": "Growing bodies require regular hydration during school & playtime."
    },
    "👧 Teen": {
        "full_name": "Teen (13–18 yrs)",
        "goal": 2000,
        "cups": "≈ 8–10 cups (250 ml each)",
        "hint": "High study routines & activities demand constant fluid balance."
    },
    "🧑 Adult": {
        "full_name": "Adult (19–50 yrs)",
        "goal": 2500,
        "cups": "≈ 8–10 cups (250 ml each)",
        "hint": "Supports peak mental focus, daily energy, and metabolism."
    },
    "👴 Senior": {
        "full_name": "Senior (65+ yrs)",
        "goal": 2000,
        "cups": "≈ 4–10 cups (250 ml each)",
        "hint": "Thirst cues decline with age; scheduled drinking is essential."
    }
}

# ==============================================================================
# 3. INITIALIZE STATE
# ==============================================================================
default_avatar = "🧑 Adult"

if "avatar" not in st.session_state:
    st.session_state.avatar = default_avatar

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = AVATARS[default_avatar]["goal"]

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
    """Logs water intake and adds a timestamped record."""
    if amount > 0:
        st.session_state.total_intake += amount
        st.session_state.logs.append({
            "Time": datetime.now().strftime("%I:%M %p"),
            "Drink": label,
            "Amount": f"+{amount} ml",
            "Total": f"{st.session_state.total_intake} ml"
        })
        st.toast(f"Logged +{amount} ml ({label})!", icon="💧")

def undo_drink():
    """Removes the most recent logged intake."""
    if st.session_state.logs:
        last = st.session_state.logs.pop()
        amt = int(last["Amount"].replace("+", "").replace(" ml", "").strip())
        st.session_state.total_intake = max(0, st.session_state.total_intake - amt)
        st.toast(f"Undid -{amt} ml", icon="↩️")

def reset_all():
    """Resets daily counters for a fresh day."""
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated = False
    st.session_state.show_reset_confirm = False
    st.toast("Counters reset for a fresh day!", icon="🔄")


# Calculate live metrics
remaining = max(0, st.session_state.daily_goal - st.session_state.total_intake)
pct = round((st.session_state.total_intake / st.session_state.daily_goal) * 100, 1) if st.session_state.daily_goal > 0 else 0.0

if pct >= 100.0 and not st.session_state.celebrated:
    st.balloons()
    st.session_state.celebrated = True
elif pct < 100.0:
    st.session_state.celebrated = False


# ==============================================================================
# 5. MOBILE APP INTERFACE (PURE PYTHON)
# ==============================================================================

# Mobile App Header
st.title("💧 WaterBuddy")
st.caption(f"Profile: **{st.session_state.avatar}** • Target: **{st.session_state.daily_goal:,} ml**")

# Clean Mobile Navigation Tabs (Directly matching Storyboard mobile navigation)
tab_home, tab_log, tab_summary, tab_profile = st.tabs([
    "🏠 Today",
    "🥤 Log Drink",
    "📊 Summary",
    "⚙️ Profile"
])


# ------------------------------------------------------------------------------
# TAB 1: 🏠 TODAY (HOME SCREEN)
# ------------------------------------------------------------------------------
with tab_home:
    with st.container(border=True):
        st.subheader("💧 Today's Hydration")
        
        # 3 Clean Metrics (Storyboard: Total ++ amount, remaining needed, % progress)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Drunk", f"{st.session_state.total_intake:,} ml")
        col2.metric("Remaining", f"{remaining:,} ml")
        col3.metric("Progress", f"{pct}%")

        # Native Progress Bar
        progress_val = min(pct / 100.0, 1.0)
        st.progress(progress_val)

        # Dynamic Water Cups Visual (Pure Python)
        cups_drunk = st.session_state.total_intake // 250
        total_cups_needed = max(1, st.session_state.daily_goal // 250)
        filled_icons = "🥛 " * min(cups_drunk, 10)
        empty_icons = "🫙 " * max(0, min(total_cups_needed - cups_drunk, 10))
        st.write(f"**Intake Level:** {filled_icons}{empty_icons} ({cups_drunk}/{total_cups_needed} glasses)")

        # Motivational Feedback (Storyboard Screens 1, 2, 3)
        if pct >= 100.0:
            st.success("🏆 **Goal Achieved! Fantastic job!** (100% reached)")
        elif pct >= 75.0:
            st.success(f"⭐ **Almost at the finish line!** ({pct}% completed)")
        elif pct >= 50.0:
            st.info(f"🌊 **Halfway there!** ({pct}% completed - logged water keeping you energized)")
        elif pct >= 20.0:
            st.info(f"🌱 **Great start!** ({pct}% completed - keep sipping regularly)")
        else:
            st.write("💧 **Ready to start!** Take your first sip today to begin.")

    # Turtle Mascot Card (Storyboard Panel 6)
    with st.container(border=True):
        st.subheader("🐢 Turtle Mascot")
        if pct >= 100.0:
            st.markdown("### 🐢🎉✨ **Celebration!**")
            st.success("Awesome job! You reached 100% of your daily water goal! Turtle is celebrating with you!")
        elif pct >= 75.0:
            st.markdown("### 🐢👋 **Avatar Waves!**")
            st.info(f"You're at {pct}%! Turtle is happily waving hello and cheering you to the finish line!")
        elif pct >= 20.0:
            st.markdown("### 🐢😊 **Avatar Smiles!**")
            st.info(f"Great start ({pct}%)! Turtle is smiling at your healthy routine.")
        else:
            st.markdown("### 🐢😴 **Turtle is Resting**")
            st.write("Take your first sip (reach 20% progress) to wake Turtle up and see him smile!")

    # 1-Click Primary Quick Drink Button
    if st.button("➕ Quick Drink (+250 ml Glass)", use_container_width=True, type="primary"):
        log_water(250, "Glass (250 ml)")
        st.rerun()


# ------------------------------------------------------------------------------
# TAB 2: 🥤 LOG DRINK (LOG ACTIVITY SCREEN - SCREENS 5 & 6)
# ------------------------------------------------------------------------------
with tab_log:
    with st.container(border=True):
        st.subheader("🥤 Quick Presets")
        st.write("Select a preset to quickly add to your daily intake:")

        # Primary compulsory +250ml Glass button
        if st.button("➕ 250 ml (Standard Glass)", use_container_width=True, type="primary"):
            log_water(250, "Glass (250 ml)")
            st.rerun()

        # Companion preset buttons
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("➕ 100 ml (Small Cup)", use_container_width=True):
                log_water(100, "Cup (100 ml)")
                st.rerun()
        with btn_c2:
            if st.button("➕ 500 ml (Water Bottle)", use_container_width=True):
                log_water(500, "Bottle (500 ml)")
                st.rerun()

    with st.container(border=True):
        st.subheader("✏️ Custom Entry")
        st.write("Enter an exact amount of water in milliliters:")
        
        custom_c1, custom_c2 = st.columns([3, 2])
        with custom_c1:
            custom_ml = st.number_input(
                "Amount in ml",
                min_value=20,
                max_value=2000,
                value=250,
                step=50,
                label_visibility="collapsed"
            )
        with custom_c2:
            if st.button("Add Entry", use_container_width=True):
                log_water(custom_ml, f"Custom ({custom_ml} ml)")
                st.rerun()

    # Undo Button
    if st.button("↩️ Undo Last Logged Drink", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
        undo_drink()
        st.rerun()


# ------------------------------------------------------------------------------
# TAB 3: 📊 SUMMARY (END-OF-DAY SUMMARY - SCREENS 8 & 9)
# ------------------------------------------------------------------------------
with tab_summary:
    with st.container(border=True):
        st.subheader("📋 End-of-Day Summary")
        st.caption("Daily Hydration Report")

        sum_c1, sum_c2 = st.columns(2)
        sum_c1.metric("Total Intake", f"{st.session_state.total_intake:,} ml")
        sum_c2.metric("Daily Target", f"{st.session_state.daily_goal:,} ml")

        if pct >= 100.0:
            st.success(f"**{pct}% Achieved!** 🎉 Excellent job! You hit 100% of your target. Regular hydration is keeping you energized!")
        else:
            st.info(f"**{pct}% Achieved!** Keep sipping water consistently to reach your goal.")

        st.divider()

        # Storyboard Screen 8: New Day / Reset confirmation
        if not st.session_state.show_reset_confirm:
            if st.button("🔄 New Day / Reset Counters", use_container_width=True):
                st.session_state.show_reset_confirm = True
                st.rerun()
        else:
            st.warning("⚠️ **New Day Confirmation**: This will reset your counters for today. Are you sure?")
            conf1, conf2 = st.columns(2)
            with conf1:
                if st.button("✅ [Yes] Reset Now", use_container_width=True, type="primary"):
                    reset_all()
                    st.rerun()
            with conf2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.session_state.show_reset_confirm = False
                    st.rerun()

    # Timeline Log
    with st.expander("📜 Today's Logged History", expanded=True):
        if st.session_state.logs:
            df_history = pd.DataFrame(reversed(st.session_state.logs))
            st.dataframe(df_history, use_container_width=True, hide_index=True)
        else:
            st.info("No drinks logged yet today.")


# ------------------------------------------------------------------------------
# TAB 4: ⚙️ PROFILE (USER AVATARS & GUIDELINES)
# ------------------------------------------------------------------------------
with tab_profile:
    with st.container(border=True):
        st.subheader("👤 User Avatar & Age Group")
        
        avatar_keys = list(AVATARS.keys())
        selected_avatar = st.radio(
            "Select Avatar",
            options=avatar_keys,
            index=avatar_keys.index(st.session_state.avatar),
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if selected_avatar != st.session_state.avatar:
            st.session_state.avatar = selected_avatar
            st.session_state.daily_goal = AVATARS[selected_avatar]["goal"]
            st.rerun()

        info = AVATARS[st.session_state.avatar]
        st.info(f"**{info['full_name']}**: {info['hint']}")

    with st.container(border=True):
        st.subheader("🎯 Daily Target Adjustment")
        st.write("Standard suggested goal based on age with manual adjustment option:")
        
        adj_goal = st.number_input(
            "Target Goal (ml)",
            min_value=500,
            max_value=5000,
            value=st.session_state.daily_goal,
            step=100
        )
        if adj_goal != st.session_state.daily_goal:
            st.session_state.daily_goal = adj_goal
            st.rerun()

        st.caption(f"Standard guideline: **{info['goal']:,} ml** ({info['cups']})")
