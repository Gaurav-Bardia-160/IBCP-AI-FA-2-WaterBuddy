import os
import streamlit as st
import random
from datetime import datetime
from PIL import Image, ImageDraw

# ==========================================
# AUTO-SETUP APP THEME (Pure Python)
# ==========================================
def ensure_theme():
    """Creates Streamlit's native config.toml with dark blue/indigo theme."""
    os.makedirs(".streamlit", exist_ok=True)
    config_path = os.path.join(".streamlit", "config.toml")
    theme_config = (
        '[theme]\n'
        'base = "dark"\n'
        'primaryColor = "#3B82F6"\n'
        'backgroundColor = "#080C14"\n'
        'secondaryBackgroundColor = "#162238"\n'
        'textColor = "#F8FAFC"\n'
    )
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(theme_config)

ensure_theme()

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="WaterBuddy",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# DATA & CONSTANTS
# ==========================================
AGE_GOALS = {
    "Kids (6-12 years)": 1600,
    "Teens (13-18 years)": 2200,
    "Adults (19-50 years)": 2500,
    "Seniors (65+ years)": 2000
}

HYDRATION_TIPS = [
    "Drink a glass of water first thing in the morning to kickstart your metabolism.",
    "Keep your water bottle within arm's reach so you sip throughout the day.",
    "Eat water-rich foods like watermelon, cucumbers, and oranges.",
    "Drink a glass of water 30 minutes before every meal to aid digestion.",
    "Feeling tired or unfocused? Have a cup of water before reaching for caffeine.",
    "Take a quick hydration break every time you finish a study or work task.",
    "Infuse your water with lemon, cucumber, or mint for a refreshing natural flavor."
]

# ==========================================
# SESSION STATE INITIALIZATION (Stage 4)
# ==========================================
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "age_group" not in st.session_state:
    st.session_state.age_group = "Adults (19-50 years)"

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = AGE_GOALS[st.session_state.age_group]

if "cup_capacity" not in st.session_state:
    st.session_state.cup_capacity = 250

if "bottle_capacity" not in st.session_state:
    st.session_state.bottle_capacity = 500

if "intake" not in st.session_state:
    st.session_state.intake = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "current_tip" not in st.session_state:
    st.session_state.current_tip = random.choice(HYDRATION_TIPS)

if "celebrated" not in st.session_state:
    st.session_state.celebrated = False

# ==========================================
# PURE PYTHON FUNCTIONS & LOGIC (Stage 4 & 5)
# ==========================================
def log_water(amount, label="Drink"):
    """Logs water intake, records timestamp, and triggers 100% celebration."""
    if amount > 0:
        old_intake = st.session_state.intake
        st.session_state.intake += amount
        
        current_time = datetime.now().strftime("%I:%M %p")
        st.session_state.history.insert(0, f"{current_time} — Added **{amount} ml** ({label})")
        
        if old_intake < st.session_state.daily_goal and st.session_state.intake >= st.session_state.daily_goal:
            if not st.session_state.celebrated:
                st.balloons()
                st.session_state.celebrated = True

def reset_tracker():
    """Resets daily progress to start fresh."""
    st.session_state.intake = 0
    st.session_state.history = []
    st.session_state.celebrated = False
    st.session_state.current_tip = random.choice(HYDRATION_TIPS)

def get_milestone_feedback(percentage, age_group, name):
    """Returns age-aware feedback messages at hydration milestones."""
    is_kid = "Kids" in age_group
    
    if percentage == 0:
        return "Ready to Hydrate", f"Tap a drink button to start your day, {name}!" if is_kid else f"Log your first cup or bottle of water to start your day, {name}."
    elif percentage < 25:
        return "Off to a Great Start", f"Great job starting your water goal, {name}!" if is_kid else f"Good start, {name}. Early hydration sets the tone for your day."
    elif percentage < 50:
        return "25% Milestone Reached", "You are swimming right along! Keep sipping!" if is_kid else "Nice momentum. You have completed a quarter of your daily target."
    elif percentage < 75:
        return "50% Milestone: Halfway There", f"Awesome job, {name}! You passed the halfway mark!" if is_kid else f"Great progress, {name}. You reached 50% of your daily goal."
    elif percentage < 100:
        return "75% Milestone: Almost Done", "Just a little more water left to reach your goal!" if is_kid else "Fantastic effort. You are in the home stretch for today."
    else:
        return "100% Goal Achieved", f"Congratulations {name}! You completed today's goal!" if is_kid else f"Congratulations, {name}. You achieved 100% of your daily hydration goal."

def draw_hydration_rings(personal_pct, recommended_pct):
    """Uses Pure Python (PIL ImageDraw) to draw concentric Green & Yellow rings with completion checkmark."""
    size = 320
    center = size // 2
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer Ring: Personal Goal (Vibrant Green)
    r_outer = 140
    width_outer = 28
    bbox_outer = [center - r_outer, center - r_outer, center + r_outer, center + r_outer]
    draw.arc(bbox_outer, start=0, end=360, fill=(34, 197, 94, 55), width=width_outer)
    if personal_pct > 0:
        angle_outer = min(personal_pct, 100) / 100.0 * 360.0
        draw.arc(bbox_outer, start=-90, end=-90 + angle_outer, fill=(34, 197, 94, 255), width=width_outer)

    # Inner Ring: Recommended Age Goal (Vibrant Yellow)
    r_inner = 98
    width_inner = 28
    bbox_inner = [center - r_inner, center - r_inner, center + r_inner, center + r_inner]
    draw.arc(bbox_inner, start=0, end=360, fill=(250, 204, 21, 55), width=width_inner)
    if recommended_pct > 0:
        angle_inner = min(recommended_pct, 100) / 100.0 * 360.0
        draw.arc(bbox_inner, start=-90, end=-90 + angle_inner, fill=(250, 204, 21, 255), width=width_inner)

    # Draw Tick / Checkmark inside the circle when goal is completed (100%+)
    if personal_pct >= 100:
        tick_points = [
            (center - 28, center + 2),
            (center - 8, center + 24),
            (center + 32, center - 22)
        ]
        draw.line(tick_points, fill=(255, 255, 255, 255), width=10, joint="curve")
        for pt in tick_points:
            draw.ellipse([pt[0] - 5, pt[1] - 5, pt[0] + 5, pt[1] + 5], fill=(255, 255, 255, 255))

    return img


# ==========================================
# SCREEN 1: HOME / ONBOARDING SETUP SCREEN
# ==========================================
if not st.session_state.setup_complete:
    st.write("")
    _, center_col, _ = st.columns([0.6, 2.2, 0.6])
    
    with center_col:
        with st.container(border=True):
            st.header(":blue[Welcome to WaterBuddy!]")
            st.caption("Set up your profile and drinkware capacities to begin.")
            
            name_input = st.text_input(
                "What is your name?",
                value=st.session_state.user_name,
                placeholder="Enter your name (Required)"
            )
            
            selected_age = st.selectbox(
                "Select Your Age Group:",
                options=list(AGE_GOALS.keys()),
                index=list(AGE_GOALS.keys()).index(st.session_state.age_group)
            )
            
            suggested_target = AGE_GOALS[selected_age]
            if selected_age != st.session_state.age_group:
                st.session_state.age_group = selected_age
                st.session_state.daily_goal = suggested_target
            
            st.info(f"**Recommended Target for {selected_age}:** {suggested_target} ml")
            
            goal_input = st.number_input(
                "Your Personal Daily Water Target (ml):",
                min_value=500,
                max_value=6000,
                value=st.session_state.daily_goal,
                step=100
            )
            
            st.subheader(":violet[Your Drinkware Capacities]")
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                cup_input = st.number_input(
                    "1 Cup / Glass Capacity (ml):",
                    min_value=50,
                    max_value=1000,
                    value=st.session_state.cup_capacity,
                    step=25
                )
            with d_col2:
                bottle_input = st.number_input(
                    "1 Water Bottle Capacity (ml):",
                    min_value=100,
                    max_value=3000,
                    value=st.session_state.bottle_capacity,
                    step=50
                )
            
            st.write("")
            if st.button("Proceed to Dashboard", type="primary", use_container_width=True):
                if not name_input.strip():
                    st.error("Please enter your name before proceeding.")
                else:
                    st.session_state.user_name = name_input.strip()
                    st.session_state.age_group = selected_age
                    st.session_state.daily_goal = goal_input
                    st.session_state.cup_capacity = cup_input
                    st.session_state.bottle_capacity = bottle_input
                    st.session_state.setup_complete = True
                    st.rerun()


# ==========================================
# SCREEN 2: MAIN HYDRATION DASHBOARD
# ==========================================
else:
    # --- TOP BAR: GREETING (LEFT) & USER PROFILE MENU (TOP RIGHT) ---
    top_left, top_right = st.columns([3.2, 1], vertical_alignment="center")
    
    with top_left:
        st.header(f":blue[{st.session_state.user_name}'s] WaterBuddy")
        st.markdown(
            f":blue-background[**{st.session_state.age_group}**] &nbsp; "
            f":violet-background[**Cup: {st.session_state.cup_capacity} ml**] &nbsp; "
            f":orange-background[**Bottle: {st.session_state.bottle_capacity} ml**]"
        )
        
    with top_right:
        with st.popover(f"Profile: {st.session_state.user_name}", use_container_width=True):
            st.subheader("Edit Your Profile")
            
            new_name = st.text_input("Name:", value=st.session_state.user_name)
            
            new_age = st.selectbox(
                "Age Group:",
                options=list(AGE_GOALS.keys()),
                index=list(AGE_GOALS.keys()).index(st.session_state.age_group)
            )
            
            if new_age != st.session_state.age_group:
                st.session_state.age_group = new_age
                st.session_state.daily_goal = AGE_GOALS[new_age]
                st.rerun()
                
            st.caption(f"Recommended Age Target: **{AGE_GOALS[st.session_state.age_group]} ml**")
            
            new_goal = st.number_input(
                "Personal Daily Target (ml):",
                min_value=500,
                max_value=6000,
                value=st.session_state.daily_goal,
                step=100
            )
            
            new_cup = st.number_input(
                "1 Cup / Glass Capacity (ml):",
                min_value=50,
                max_value=1000,
                value=st.session_state.cup_capacity,
                step=25
            )
            
            new_bottle = st.number_input(
                "1 Bottle Capacity (ml):",
                min_value=100,
                max_value=3000,
                value=st.session_state.bottle_capacity,
                step=50
            )
            
            if st.button("Save Changes", type="primary", use_container_width=True):
                if not new_name.strip():
                    st.error("Name cannot be empty.")
                else:
                    st.session_state.user_name = new_name.strip()
                    st.session_state.daily_goal = new_goal
                    st.session_state.cup_capacity = new_cup
                    st.session_state.bottle_capacity = new_bottle
                    st.toast("Profile settings updated!")
                    st.rerun()
                
            if st.button("Back to Setup Screen", use_container_width=True):
                st.session_state.setup_complete = False
                st.rerun()

    st.divider()

    # --- LIVE CALCULATIONS (Stage 5) ---
    total_intake = st.session_state.intake
    goal = st.session_state.daily_goal
    standard_target = AGE_GOALS[st.session_state.age_group]
    cup_cap = st.session_state.cup_capacity
    bottle_cap = st.session_state.bottle_capacity
    
    remaining = max(0, goal - total_intake)
    percentage = round((total_intake / goal) * 100, 1) if goal > 0 else 0.0
    std_pct = round((total_intake / standard_target) * 100, 1) if standard_target > 0 else 0.0

    # ==========================================
    # 3-COLUMN DASHBOARD LAYOUT
    # ==========================================
    left_col, mid_col, right_col = st.columns([1.45, 1.15, 1.25], gap="medium")

    # ------------------------------------------
    # LEFT COLUMN: 4 METRIC BOXES + READY TO HYDRATE BELOW THEM
    # ------------------------------------------
    with left_col:
        m_c1, m_c2 = st.columns(2, gap="small")
        
        with m_c1:
            st.info(
                f"**Total Intake**\n"
                f"### {total_intake} ml\n"
                f"{round(total_intake / cup_cap, 1)} of your cups"
            )
            rem_text = "Goal Reached!" if remaining == 0 else f"{round(remaining / cup_cap, 1)} cups left"
            st.warning(
                f"**Remaining Needed**\n"
                f"### {remaining} ml\n"
                f"{rem_text}"
            )

        with m_c2:
            diff = goal - standard_target
            diff_text = "Matches age target" if diff == 0 else f"{diff:+d} ml vs age"
            st.success(
                f"**Daily Goal**\n"
                f"### {goal} ml\n"
                f"{diff_text}"
            )
            ach_text = "100%+ Complete" if percentage >= 100 else f"{round(100 - percentage, 1)}% remaining"
            st.error(
                f"**Goal Achieved**\n"
                f"### {percentage}%\n"
                f"{ach_text}"
            )

        # Placed directly below the 4 metric boxes
        headline, message = get_milestone_feedback(percentage, st.session_state.age_group, st.session_state.user_name)
        with st.container(border=True):
            st.subheader(f":green[{headline}]")
            if percentage >= 100:
                st.success(message)
            else:
                st.info(message)
                
            st.divider()
            t_col1, t_col2 = st.columns([2.2, 1], vertical_alignment="center")
            with t_col1:
                st.markdown("**:violet[Daily Hydration Tip]**")
            with t_col2:
                if st.button("New Tip", use_container_width=True):
                    st.session_state.current_tip = random.choice(HYDRATION_TIPS)
                    st.rerun()
            st.warning(st.session_state.current_tip)

    # ------------------------------------------
    # MIDDLE COLUMN: TODAY'S INTAKE REPORT + CONVERTER
    # ------------------------------------------
    with mid_col:
        with st.container(border=True):
            st.subheader(":violet[Today's Intake Report]")
            if st.session_state.history:
                for entry in st.session_state.history[:5]:
                    st.info(entry)
            else:
                st.info("No water logged yet today. Use the buttons to start.")
                
            if st.button("Reset Day & Start Fresh", use_container_width=True):
                reset_tracker()
                st.toast("Daily progress reset.")
                st.rerun()

        with st.container(border=True):
            st.subheader(":orange[Cups to ml Converter]")
            st.caption(f"Based on your saved cup capacity ({cup_cap} ml):")
            
            num_cups = st.number_input("Number of Cups:", min_value=0.5, max_value=20.0, value=2.0, step=0.5)
            converted_ml = int(num_cups * cup_cap)
            
            st.warning(f"**{num_cups} cup(s)** = **{converted_ml} ml**")
            
            if st.button(f"Log {converted_ml} ml Now", type="primary", use_container_width=True):
                log_water(converted_ml, f"{num_cups} Cups")
                st.rerun()

    # ------------------------------------------
    # RIGHT COLUMN: HYDRATION RINGS + LOG WATER INTAKE BELOW IT
    # ------------------------------------------
    with right_col:
        with st.container(border=True):
            st.subheader(":green[Your Progress]")
            ring_image = draw_hydration_rings(percentage, std_pct)
            _, ring_col, _ = st.columns([0.2, 2, 0.2])
            with ring_col:
                st.image(ring_image, use_container_width=True)
            st.success(f"**Outer Green (Personal):** {percentage}% ({total_intake}/{goal} ml)")
            st.warning(f"**Inner Yellow (Age Goal):** {std_pct}% ({total_intake}/{standard_target} ml)")

        # Placed directly below Hydration Rings
        with st.container(border=True):
            st.subheader(":blue[Log Water Intake]")
            st.caption("Select your cup, bottle, or enter a custom amount:")
            
            b1, b2 = st.columns(2)
            with b1:
                if st.button(f"+1 Cup ({cup_cap} ml)", use_container_width=True):
                    log_water(cup_cap, "1 Cup")
                    st.rerun()
            with b2:
                if st.button(f"+1 Bottle ({bottle_cap} ml)", use_container_width=True):
                    log_water(bottle_cap, "1 Bottle")
                    st.rerun()
                    
            c1, c2 = st.columns([1.8, 1], vertical_alignment="bottom")
            with c1:
                custom_ml = st.number_input("Custom amount (ml):", min_value=10, max_value=3000, value=300, step=50)
            with c2:
                if st.button("Add Custom", type="primary", use_container_width=True):
                    log_water(custom_ml, "Custom")
                    st.rerun()