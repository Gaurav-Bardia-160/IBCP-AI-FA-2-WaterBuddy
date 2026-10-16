"""
WaterBuddy - Modern Mobile Hydration Companion
Built 100% in Pure Python using Streamlit & Altair.
Zero HTML, Zero CSS.

Features from FA-1 Storyboard & FA-2 Rubric:
- Clean mobile-first centered interface (layout='centered')
- Native modern Segmented Control for 4 Avatars (Child, Teen, Adult, Senior)
- Auto-suggested daily targets with optional adjustment
- Interactive Altair vector hydration ring gauge (Pure Python)
- Live metrics: Total intake, remaining needed, % progress, and progress bar
- Milestone feedback with exact Turtle Mascot reactions (<20%, >=20%, >=75%, 100%+)
- One-touch compulsory +250ml quick logging, companion presets, and custom entry
- End-of-Day summary report and safe New Day reset confirmation
- Detailed intake history table
"""

import sys
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Auto-launch via Streamlit if run directly with python app.py
if get_script_run_ctx() is None:
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())

import streamlit as st
import altair as alt
import pandas as pd
from datetime import datetime

# ==============================================================================
# 1. PAGE SETUP (CLEAN MOBILE CENTERED LAYOUT)
# ==============================================================================
st.set_page_config(
    page_title="WaterBuddy",
    page_icon="💧",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. STORYBOARD DATA & PRESETS
# ==============================================================================
AVATAR_PROFILES = {
    "🧒 Child": {
        "title": "Child (6–12 yrs)",
        "goal": 1600,
        "cups": "≈ 6–7 cups (250 ml each)",
        "guideline": "Active growing bodies require steady hydration for play and school."
    },
    "👧 Teen": {
        "title": "Teen (13–18 yrs)",
        "goal": 2000,
        "cups": "≈ 8–10 cups (250 ml each)",
        "guideline": "High-energy study routines demand consistent fluid balance."
    },
    "🧑 Adult": {
        "title": "Adult (19–50 yrs)",
        "goal": 2500,
        "cups": "≈ 8–10 cups (250 ml each)",
        "guideline": "Maintains peak mental energy, organ health, and metabolism."
    },
    "👴 Senior": {
        "title": "Senior (65+ yrs)",
        "goal": 2000,
        "cups": "≈ 4–10 cups (250 ml each)",
        "guideline": "Thirst cues decline with age; scheduled drinking is essential."
    }
}

# ==============================================================================
# 3. INITIALIZE SESSION STATE
# ==============================================================================
default_avatar = "🧑 Adult"

if "selected_avatar" not in st.session_state:
    st.session_state.selected_avatar = default_avatar

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = AVATAR_PROFILES[default_avatar]["goal"]

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
    """Logs water intake and records timestamped entry."""
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
    """Removes the most recent logged intake."""
    if st.session_state.logs:
        last = st.session_state.logs.pop()
        amt = int(last["Amount Added"].replace("+", "").replace(" ml", "").strip())
        st.session_state.total_intake = max(0, st.session_state.total_intake - amt)
        st.toast(f"Removed last entry (-{amt} ml)", icon="↩️")

def reset_all_counters():
    """Resets daily progress for a new day."""
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated = False
    st.session_state.show_reset_confirm = False
    st.toast("Counters reset for a fresh day!", icon="🔄")


# Live metric computations
remaining_needed = max(0, st.session_state.daily_goal - st.session_state.total_intake)
pct_progress = round((st.session_state.total_intake / st.session_state.daily_goal) * 100, 1) if st.session_state.daily_goal > 0 else 0.0

# 100% Celebration balloons
if pct_progress >= 100.0 and not st.session_state.celebrated:
    st.balloons()
    st.session_state.celebrated = True
elif pct_progress < 100.0:
    st.session_state.celebrated = False


# ==============================================================================
# 5. PURE PYTHON VECTOR GAUGE (ALTAIR DONUT RING)
# ==============================================================================
def create_hydration_gauge(pct: float, current_ml: int, target_ml: int):
    """
    Builds a vector hydration ring chart using Altair (100% Pure Python).
    Displays the filled ring with center percentage and intake metrics.
    """
    clamped_pct = min(max(pct, 0.0), 100.0)
    remaining_pct = max(0.0, 100.0 - clamped_pct)

    gauge_df = pd.DataFrame({
        "Category": ["Hydrated", "Remaining"],
        "Value": [clamped_pct if clamped_pct > 0 else 0.001, remaining_pct]
    })

    # Base arc ring
    base_ring = alt.Chart(gauge_df).mark_arc(
        innerRadius=66,
        outerRadius=90,
        cornerRadius=6
    ).encode(
        theta=alt.Theta("Value:Q", sort=None),
        color=alt.Color(
            "Category:N",
            scale=alt.Scale(
                domain=["Hydrated", "Remaining"],
                range=["#0284c7", "#e2e8f0"]
            ),
            legend=None
        ),
        tooltip=[alt.Tooltip("Category:N"), alt.Tooltip("Value:Q", format=".1f", title="Percent")]
    ).properties(width=220, height=220)

    # Center text for percentage
    text_pct = alt.Chart(pd.DataFrame({"text": [f"{clamped_pct:.0f}%"]})).mark_text(
        fontSize=28,
        fontWeight="bold",
        color="#0284c7",
        dy=-8
    ).encode(text="text:N")

    # Center text for sublabel
    text_sub = alt.Chart(pd.DataFrame({"text": [f"{current_ml} / {target_ml} ml"]})).mark_text(
        fontSize=11,
        fontWeight="bold",
        color="#64748b",
        dy=16
    ).encode(text="text:N")

    return (base_ring + text_pct + text_sub).configure_view(strokeWidth=0)


# ==============================================================================
# 6. APP HEADER & PROFILE BAR
# ==============================================================================
st.title("💧 WaterBuddy")
st.caption("Smart Daily Hydration Tracker • Pure Python Edition")

# Avatar Profile Selector (Native Streamlit Segmented Control)
with st.container(border=True):
    st.write("**👤 User Profile:**")
    avatar_list = list(AVATAR_PROFILES.keys())
    
    selected_av = st.segmented_control(
        "Profile",
        options=avatar_list,
        default=st.session_state.selected_avatar,
        label_visibility="collapsed"
    )
    
    if selected_av and selected_av != st.session_state.selected_avatar:
        st.session_state.selected_avatar = selected_av
        st.session_state.daily_goal = AVATAR_PROFILES[selected_av]["goal"]
        st.rerun()

    profile_info = AVATAR_PROFILES[st.session_state.selected_avatar]
    st.info(f"💡 **{profile_info['title']}**: {profile_info['guideline']} (Standard target: **{profile_info['goal']:,} ml** • {profile_info['cups']})")


# ==============================================================================
# 7. HERO DASHBOARD CARD (VISUAL GAUGE & LIVE METRICS)
# ==============================================================================
with st.container(border=True):
    st.subheader("📊 Today's Progress")

    # Centered Vector Donut Gauge (Pure Python Altair)
    col_chart_left, col_chart_mid, col_chart_right = st.columns([1, 2, 1])
    with col_chart_mid:
        gauge_chart = create_hydration_gauge(
            pct_progress,
            st.session_state.total_intake,
            st.session_state.daily_goal
        )
        st.altair_chart(gauge_chart, use_container_width=True)

    # 3 Aligned Metrics Cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Intake", f"{st.session_state.total_intake:,} ml")
    m2.metric("Remaining", f"{remaining_needed:,} ml")
    m3.metric("Goal Target", f"{st.session_state.daily_goal:,} ml")

    # Linear progress bar
    st.progress(min(pct_progress / 100.0, 1.0))

    # Motivational Milestone Status (Storyboard Screens 1, 2, 3)
    if pct_progress >= 100.0:
        st.success("🏆 **Goal Achieved! Fantastic job!** You reached 100% of your daily hydration!")
    elif pct_progress >= 75.0:
        st.success(f"⭐ **Almost at the finish line!** ({pct_progress}% completed — just a few more sips!)")
    elif pct_progress >= 50.0:
        st.info(f"🌊 **Halfway there!** ({pct_progress}% completed — regular water is keeping you focused!)")
    elif pct_progress >= 20.0:
        st.info(f"🌱 **Great start!** ({pct_progress}% completed — keep up this healthy rhythm!)")
    else:
        st.write("💧 **Ready to start!** Take your first sip today to begin tracking.")


# ==============================================================================
# 8. TURTLE MASCOT CARD (STORYBOARD PANEL 6)
# ==============================================================================
with st.container(border=True):
    st.subheader("🐢 Turtle Mascot")
    
    if pct_progress >= 100.0:
        st.markdown("### 🐢🎉✨ **Celebration Milestone!**")
        st.success("Awesome job! You reached 100% of your daily water goal! Turtle is celebrating with you! 🎉")
    elif pct_progress >= 75.0:
        st.markdown("### 🐢👋 **Avatar Waves!**")
        st.info(f"You're at {pct_progress}%! Turtle is happily waving hello and cheering you to the finish line!")
    elif pct_progress >= 20.0:
        st.markdown("### 🐢😊 **Avatar Smiles!**")
        st.info(f"Great start ({pct_progress}%)! Turtle is smiling at your healthy hydration habit.")
    else:
        st.markdown("### 🐢😴 **Turtle is Resting**")
        st.write("Take your first sip (reach 20% progress) to wake Turtle up and see him smile!")


# ==============================================================================
# 9. QUICK LOG INTAKE (STORYBOARD SCREENS 5 & 6)
# ==============================================================================
with st.container(border=True):
    st.subheader("🥤 Quick Water Log")
    st.write("Tap a preset button or enter a custom amount:")

    # 3 Quick preset buttons (Compulsory +250ml highlighted as Primary)
    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        if st.button("➕ 250 ml\n(Glass)", use_container_width=True, type="primary"):
            log_water(250, "Standard Glass (250 ml)")
            st.rerun()
    with btn2:
        if st.button("➕ 100 ml\n(Cup)", use_container_width=True):
            log_water(100, "Small Cup (100 ml)")
            st.rerun()
    with btn3:
        if st.button("➕ 500 ml\n(Bottle)", use_container_width=True):
            log_water(500, "Water Bottle (500 ml)")
            st.rerun()

    # Custom Entry (Storyboard Screen 6)
    with st.expander("✏️ Log Custom Intake Amount"):
        c_in1, c_in2 = st.columns([3, 2])
        with c_in1:
            custom_ml = st.number_input(
                "Amount in ml",
                min_value=20,
                max_value=2000,
                value=250,
                step=50,
                label_visibility="collapsed"
            )
        with c_in2:
            if st.button("Add Entry", use_container_width=True):
                log_water(custom_ml, f"Custom ({custom_ml} ml)")
                st.rerun()

    # Manual Goal Adjustment Option (Storyboard Panel 4)
    with st.expander("🎯 Adjust Daily Target Goal"):
        adj_val = st.number_input(
            "Daily Target (ml)",
            min_value=500,
            max_value=5000,
            value=st.session_state.daily_goal,
            step=100
        )
        if adj_val != st.session_state.daily_goal:
            st.session_state.daily_goal = adj_val
            st.rerun()

    # Undo action button
    if st.button("↩️ Undo Last Logged Drink", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
        undo_last_drink()
        st.rerun()


# ==============================================================================
# 10. END-OF-DAY SUMMARY & NEW DAY RESET (STORYBOARD SCREENS 8 & 9)
# ==============================================================================
with st.container(border=True):
    st.subheader("📋 End-of-Day Summary")
    st.caption("Daily Hydration Report")

    s1, s2 = st.columns(2)
    s1.metric("Total Intake", f"{st.session_state.total_intake:,} ml")
    s2.metric("Daily Goal", f"{st.session_state.daily_goal:,} ml")

    if pct_progress >= 100.0:
        st.success(f"**{pct_progress}% Achieved!** 🎉 Excellent job! You hit 100% of your target. Regular hydration is keeping you energized!")
    else:
        st.info(f"**{pct_progress}% Achieved!** Keep sipping water consistently to reach your goal.")

    st.divider()

    # Storyboard Screen 8: Reset / New Day Confirmation Modal
    if not st.session_state.show_reset_confirm:
        if st.button("🔄 New Day / Reset Counters", use_container_width=True):
            st.session_state.show_reset_confirm = True
            st.rerun()
    else:
        st.warning("⚠️ **New Day Confirmation**: This will reset your counters for today. Are you sure?")
        conf1, conf2 = st.columns(2)
        with conf1:
            if st.button("✅ [Yes] Reset Now", use_container_width=True, type="primary"):
                reset_all_counters()
                st.rerun()
        with conf2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_reset_confirm = False
                st.rerun()


# ==============================================================================
# 11. TIMELINE INTAKE AUDIT LOG
# ==============================================================================
with st.expander("📜 Today's Logged History", expanded=False):
    if st.session_state.logs:
        df_history = pd.DataFrame(reversed(st.session_state.logs))
        st.dataframe(df_history, use_container_width=True, hide_index=True)
    else:
        st.info("No drinks logged yet today. Click **+250 ml** to log your first drink!")
