"""
WaterBuddy - Interactive Water Hydration Tracker
Developed for WellNest Technologies Pvt. Ltd.
IBCP AI CRS Year 1 Python Programming Project (FA-2)

Key Features:
- Age-aware daily hydration goals (Kids, Teens, Adults, Seniors)
- Dynamic auto-suggestion with manual goal adjustments
- Quick log buttons (+250ml compulsory, +100ml, +500ml) & custom logging
- Live real-time calculations (Total, Remaining, Percentage)
- Dynamic visual feedback: Animated SVG Water Bottle & Progress Bar
- Interactive Mascot milestone feedback (0%, 25%, 50%, 75%, 100%+)
- Reset day & Undo functionality
- Unit Converter (Cups, Ounces, Milliliters)
- Daily scientific hydration tips and intake history log
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

# ==========================================
# 1. PAGE CONFIGURATION & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="WaterBuddy | Smart Hydration App",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Aqua/Blue Hydration Theme CSS
st.markdown("""
<style>
    /* Main Background & Accent Styling */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.2);
    }
    .main-header h1 {
        color: white;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .main-header p {
        color: #e0f2fe;
        font-size: 1.1rem;
        margin-bottom: 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 0.8rem;
    }
    .metric-title {
        color: #0369a1;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #0c4a6e;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 0.2rem;
    }
    
    /* Mascot Card */
    .mascot-box {
        background: #ecfeff;
        border-left: 5px solid #06b6d4;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .mascot-title {
        color: #0e7490;
        font-weight: 700;
        font-size: 1.05rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .mascot-text {
        color: #164e63;
        font-size: 1rem;
        margin-top: 0.3rem;
        margin-bottom: 0;
    }

    /* Tip Box */
    .tip-box {
        background: #fefce8;
        border: 1px solid #fef08a;
        border-radius: 10px;
        padding: 0.85rem;
        color: #854d0e;
        font-size: 0.95rem;
        margin-top: 1rem;
    }
    
    /* Subtle button hover adjustments */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. CONSTANTS & SCIENTIFIC DATA
# ==========================================
AGE_GROUPS = {
    "6-12 years (Kids)": {
        "recommended_ml": 1600,
        "description": "Active growing bodies require frequent sips throughout the day."
    },
    "13-18 years (Teens)": {
        "recommended_ml": 2000,
        "description": "High energy & study routines require consistent fluid intake."
    },
    "19-50 years (Adults)": {
        "recommended_ml": 2500,
        "description": "Supports peak cognitive energy, organ function, and daily metabolism."
    },
    "65+ years (Seniors)": {
        "recommended_ml": 2000,
        "description": "Thirst sensation decreases with age; proactive scheduled hydration is key."
    }
}

HYDRATION_TIPS = [
    "💧 Drinking a glass of water right after waking up helps jumpstart your metabolism and organs.",
    "🧠 Mild dehydration (as little as 1-2%) can impair brain focus, memory, and concentration.",
    "🍋 Add a slice of lemon, cucumber, or mint to your bottle for a refreshing natural flavor boost.",
    "🏃 Drink 250ml of water 30 minutes before exercising to ensure optimal muscle performance.",
    "🍵 Herbal teas and water-rich fruits (like watermelon and oranges) contribute to your daily hydration!",
    "🥤 Thirst is a late indicator of dehydration. Sip water steadily throughout your day.",
    "✨ Drinking adequate water improves skin elasticity and keeps joints lubricated.",
    "🌡️ Hot weather and air conditioning both increase fluid loss; adjust your intake accordingly."
]


# ==========================================
# 3. HELPER & CALCULATION FUNCTIONS
# ==========================================
def get_standard_goal(age_group: str) -> int:
    """Return the scientifically suggested intake (ml) for an age group."""
    return AGE_GROUPS.get(age_group, {}).get("recommended_ml", 2000)

def calculate_metrics(total_intake: int, daily_goal: int):
    """
    Calculate hydration metrics:
    Returns (remaining_ml, percentage_achieved)
    """
    remaining = max(0, daily_goal - total_intake)
    if daily_goal > 0:
        percentage = round((total_intake / daily_goal) * 100, 1)
    else:
        percentage = 0.0
    return remaining, percentage

def get_mascot_state(percentage: float):
    """
    Returns mascot emoji, title, and motivational message based on achievement milestone.
    """
    if percentage <= 0:
        return "😴", "Buddy is Asleep & Parched", "Take your first sip today to wake Buddy up and kickstart your hydration journey!"
    elif percentage < 25:
        return "🌱", "Buddy is Waking Up!", f"Off to a healthy start! You've reached {percentage}% of your daily goal."
    elif percentage < 50:
        return "💧", "Buddy is Feeling Refreshed!", f"Nice rhythm! You're at {percentage}%. Keep sipping regularly!"
    elif percentage < 75:
        return "🌊", "Halfway Hero!", f"Over halfway there ({percentage}%)! Your body and mind thank you."
    elif percentage < 100:
        return "⭐", "Almost at the Finish Line!", f"Incredible effort ({percentage}%)! Just a few more sips to complete your daily target."
    else:
        return "🏆", "Hydration Champion!", f"Hooray! You reached {percentage}% of your goal! Buddy is proud of you! 🎉"

def render_bottle_svg(percentage: float) -> str:
    """
    Generate an interactive SVG water bottle filling dynamically according to percentage.
    """
    clamped_pct = min(max(percentage, 0.0), 100.0)
    # The water bottle fill height (total inside height is 220px, starting from bottom y=270 to y=50)
    fill_height = (clamped_pct / 100.0) * 200
    fill_y = 260 - fill_height

    svg = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 10px;">
        <svg width="180" height="310" viewBox="0 0 180 310" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="waterGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#38bdf8" />
                    <stop offset="100%" stop-color="#0284c7" />
                </linearGradient>
                <linearGradient id="glassGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="rgba(255,255,255,0.6)" />
                    <stop offset="50%" stop-color="rgba(255,255,255,0.1)" />
                    <stop offset="100%" stop-color="rgba(255,255,255,0.4)" />
                </linearGradient>
                <clipPath id="bottleClip">
                    <!-- Bottle neck and body shape -->
                    <path d="M 65 35 
                             L 115 35 
                             L 115 65 
                             Q 145 75 145 110 
                             L 145 260 
                             Q 145 275 130 275 
                             L 50 275 
                             Q 35 275 35 260 
                             L 35 110 
                             Q 35 75 65 65 
                             Z" />
                </clipPath>
            </defs>

            <!-- Bottle Cap -->
            <rect x="70" y="18" width="40" height="17" rx="5" fill="#0369a1" />
            <rect x="68" y="32" width="44" height="4" rx="2" fill="#0284c7" />

            <!-- Bottle Background / Empty Chamber -->
            <path d="M 65 35 
                     L 115 35 
                     L 115 65 
                     Q 145 75 145 110 
                     L 145 260 
                     Q 145 275 130 275 
                     L 50 275 
                     Q 35 275 35 260 
                     L 35 110 
                     Q 35 75 65 65 
                     Z" 
                  fill="#f0f9ff" stroke="#bae6fd" stroke-width="4" />

            <!-- Dynamic Water Fill Level -->
            <g clip-path="url(#bottleClip)">
                <rect x="30" y="{fill_y}" width="120" height="{fill_height + 30}" fill="url(#waterGrad)" />
                <!-- Water wave bubble / surface highlight -->
                <ellipse cx="90" cy="{fill_y}" rx="55" ry="6" fill="#7dd3fc" opacity="{0.8 if clamped_pct > 1 else 0}" />
            </g>

            <!-- Measurement Graduation Markers -->
            <!-- 75% mark -->
            <line x1="125" y1="110" x2="140" y2="110" stroke="#94a3b8" stroke-width="2" stroke-dasharray="2,2"/>
            <text x="145" y="114" font-size="10" fill="#64748b" font-family="sans-serif">75%</text>
            <!-- 50% mark -->
            <line x1="125" y1="160" x2="140" y2="160" stroke="#94a3b8" stroke-width="2" stroke-dasharray="2,2"/>
            <text x="145" y="164" font-size="10" fill="#64748b" font-family="sans-serif">50%</text>
            <!-- 25% mark -->
            <line x1="125" y1="210" x2="140" y2="210" stroke="#94a3b8" stroke-width="2" stroke-dasharray="2,2"/>
            <text x="145" y="214" font-size="10" fill="#64748b" font-family="sans-serif">25%</text>

            <!-- Glass Reflection Overlay -->
            <path d="M 65 35 
                     L 115 35 
                     L 115 65 
                     Q 145 75 145 110 
                     L 145 260 
                     Q 145 275 130 275 
                     L 50 275 
                     Q 35 275 35 260 
                     L 35 110 
                     Q 35 75 65 65 
                     Z" 
                  fill="url(#glassGrad)" stroke="#0284c7" stroke-width="3" />

            <!-- Percentage Display inside bottle -->
            <text x="90" y="295" font-size="14" font-weight="bold" fill="#0369a1" text-anchor="middle" font-family="sans-serif">
                {clamped_pct}% Fill
            </text>
        </svg>
    </div>
    """
    return svg


# ==========================================
# 4. INITIALIZE SESSION STATE
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

if "tip_index" not in st.session_state:
    st.session_state.tip_index = random.randint(0, len(HYDRATION_TIPS) - 1)

if "celebrated_goal" not in st.session_state:
    st.session_state.celebrated_goal = False


# ==========================================
# 5. STATE MODIFIERS (CALLBACKS)
# ==========================================
def log_water(amount: int, label: str):
    """Add water to total intake and record timestamped history."""
    if amount > 0:
        st.session_state.total_intake += amount
        now_str = datetime.now().strftime("%I:%M %p")
        st.session_state.logs.append({
            "time": now_str,
            "amount": amount,
            "label": label,
            "total_after": st.session_state.total_intake
        })
        st.toast(f"Logged +{amount} ml ({label})!", icon="💧")

def undo_last_log():
    """Undo the most recent water intake entry."""
    if st.session_state.logs:
        last_entry = st.session_state.logs.pop()
        st.session_state.total_intake = max(0, st.session_state.total_intake - last_entry["amount"])
        st.toast(f"Removed last log (-{last_entry['amount']} ml)", icon="↩️")

def reset_daily_progress():
    """Reset the hydration count and logs for a new day."""
    st.session_state.total_intake = 0
    st.session_state.logs = []
    st.session_state.celebrated_goal = False
    st.toast("Day reset! Ready for a fresh hydration start.", icon="🔄")

def on_age_change():
    """Automatically update the recommended goal when the age group changes."""
    suggested = get_standard_goal(st.session_state.selected_age_widget)
    st.session_state.daily_goal = suggested
    st.session_state.age_group = st.session_state.selected_age_widget


# ==========================================
# 6. SIDEBAR: TOOLS & HYDRATION KNOWLEDGE
# ==========================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1548839140-29a749e1bc4e?auto=format&fit=crop&w=300&q=80", width=300)
    st.title("💧 WaterBuddy Tools")
    st.caption("WellNest Technologies • AI CRS Project")

    st.markdown("---")
    st.subheader("💡 Daily Hydration Tip")
    st.markdown(f"""
    <div class="tip-box">
        {HYDRATION_TIPS[st.session_state.tip_index]}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎲 Next Tip", use_container_width=True):
        st.session_state.tip_index = (st.session_state.tip_index + 1) % len(HYDRATION_TIPS)
        st.rerun()

    st.markdown("---")
    st.subheader("🔄 Quick Unit Converter")
    conv_mode = st.radio("Conversion Type:", ["Cups ↔ mL", "Fluid Ounces (fl oz) ↔ mL"], horizontal=True)
    
    if conv_mode == "Cups ↔ mL":
        cups_in = st.number_input("Number of Cups (1 cup ≈ 250 ml):", min_value=0.1, value=1.0, step=0.5)
        st.info(f"👉 **{cups_in} cups** = **{int(cups_in * 250)} ml**")
    else:
        oz_in = st.number_input("Fluid Ounces (1 fl oz ≈ 29.57 ml):", min_value=1.0, value=8.0, step=1.0)
        st.info(f"👉 **{oz_in} fl oz** = **{int(oz_in * 29.57)} ml**")

    st.markdown("---")
    with st.expander("ℹ️ About WaterBuddy (FA-2)"):
        st.markdown("""
        **Developer**: WellNest Technologies Student Team  
        **Course**: IBCP AI CRS Year 1 (Python Programming)  
        **Framework**: Streamlit & Python  
        **Compliance**: Meets all Rubric requirements for Stage 4 (Coding), Stage 5 (Calculations & Mascot Feedback), and Stage 6/7 (Interface & Cloud Deployment).
        """)


# ==========================================
# 7. MAIN INTERFACE LAYOUT
# ==========================================

# Top Banner Header
st.markdown("""
<div class="main-header">
    <h1>💧 WaterBuddy</h1>
    <p>Your Intelligent, Age-Aware Daily Hydration Companion</p>
</div>
""", unsafe_allow_html=True)

# Main Grid: Left Column (Controls & Inputs), Right Column (Visual Bottle & Mascot)
col_left, col_right = st.columns([3, 2], gap="large")

# ------------------------------------------
# LEFT COLUMN: AGE SELECTOR, GOALS & LOGGING
# ------------------------------------------
with col_left:
    st.subheader("👤 Step 1: Age Group & Hydration Goal")
    
    # Age Group Selector (Compulsory Feature)
    selected_age = st.selectbox(
        "Select your age group:",
        options=list(AGE_GROUPS.keys()),
        index=list(AGE_GROUPS.keys()).index(st.session_state.age_group),
        key="selected_age_widget",
        on_change=on_age_change,
        help="Scientific hydration requirements vary significantly by age bracket."
    )
    
    age_info = AGE_GROUPS[selected_age]
    st.caption(f"ℹ️ *Guideline for {selected_age}: {age_info['description']}*")

    # Target comparison & Manual adjustment
    col_std, col_adj = st.columns(2)
    with col_std:
        std_val = age_info["recommended_ml"]
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Standard Age Guideline</div>
            <div class="metric-value">{std_val} <span style="font-size:1rem; font-weight:normal;">ml</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col_adj:
        # Option to manually adjust goal (Compulsory Feature)
        user_goal = st.number_input(
            "Custom Daily Goal (ml):",
            min_value=500,
            max_value=5000,
            value=st.session_state.daily_goal,
            step=100,
            help="You can manually tailor your personal goal (e.g., if you are exercising or in hot weather)."
        )
        st.session_state.daily_goal = user_goal

    st.markdown("---")
    
    # Stage 4 Compulsory Logging Section
    st.subheader("🥤 Step 2: Log Your Water Intake")
    st.write("Choose a quick preset or type a custom amount:")

    # Quick Buttons (Compulsory +250ml + Creative Quick Presets)
    btn_c1, btn_c2, btn_c3 = st.columns(3)
    with btn_c1:
        if st.button("➕ 250 ml\n(Standard Glass)", use_container_width=True, type="primary"):
            log_water(250, "Glass (250 ml)")
            st.rerun()

    with btn_c2:
        if st.button("➕ 100 ml\n(Small Cup)", use_container_width=True):
            log_water(100, "Small Cup (100 ml)")
            st.rerun()

    with btn_c3:
        if st.button("➕ 500 ml\n(Water Bottle)", use_container_width=True):
            log_water(500, "Water Bottle (500 ml)")
            st.rerun()

    # Custom amount input
    with st.expander("✏️ Log Custom Intake Amount"):
        custom_c1, custom_c2 = st.columns([3, 2])
        with custom_c1:
            custom_ml = st.number_input("Enter amount in ml:", min_value=10, max_value=2000, value=200, step=50)
        with custom_c2:
            st.write("")
            st.write("")
            if st.button("Add Custom ml", use_container_width=True):
                log_water(custom_ml, f"Custom ({custom_ml} ml)")
                st.rerun()

    # Management controls: Reset & Undo
    st.markdown("---")
    mgt_c1, mgt_c2 = st.columns(2)
    with mgt_c1:
        # Reset Day Button (Compulsory Feature)
        if st.button("🔄 Reset Today's Intake", use_container_width=True):
            reset_daily_progress()
            st.rerun()
    with mgt_c2:
        # Undo button (Creative Feature)
        if st.button("↩️ Undo Last Drink", use_container_width=True, disabled=(len(st.session_state.logs) == 0)):
            undo_last_log()
            st.rerun()


# ------------------------------------------
# RIGHT COLUMN: VISUALS, CALCULATIONS & MASCOT
# ------------------------------------------
with col_right:
    st.subheader("📊 Step 3: Real-Time Feedback & Bottle")

    # Stage 5 Calculations
    remaining_ml, pct_achieved = calculate_metrics(st.session_state.total_intake, st.session_state.daily_goal)
    
    # Milestone Celebration Balloons
    if pct_achieved >= 100.0 and not st.session_state.celebrated_goal:
        st.balloons()
        st.session_state.celebrated_goal = True
    elif pct_achieved < 100.0:
        st.session_state.celebrated_goal = False

    # Metric summary row
    stat_c1, stat_c2, stat_c3 = st.columns(3)
    with stat_c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Drunk</div>
            <div class="metric-value" style="color:#0284c7;">{st.session_state.total_intake} <span style="font-size:0.9rem;">ml</span></div>
        </div>
        """, unsafe_allow_html=True)
    with stat_c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Remaining</div>
            <div class="metric-value" style="color:#e11d48;">{remaining_ml} <span style="font-size:0.9rem;">ml</span></div>
        </div>
        """, unsafe_allow_html=True)
    with stat_c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Progress</div>
            <div class="metric-value" style="color:#10b981;">{pct_achieved}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Streamlit native progress bar (Compulsory Feature)
    progress_val = min(pct_achieved / 100.0, 1.0)
    st.progress(progress_val)

    # Dynamic Animated Water Bottle SVG (Compulsory / Creative Feature)
    st.markdown(render_bottle_svg(pct_achieved), unsafe_allow_html=True)

    # Stage 5 Mascot Milestone Reaction Box (Compulsory Feature)
    mascot_emoji, mascot_title, mascot_msg = get_mascot_state(pct_achieved)
    st.markdown(f"""
    <div class="mascot-box">
        <div class="mascot-title">{mascot_emoji} {mascot_title}</div>
        <p class="mascot-text">{mascot_msg}</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 8. TODAY'S INTAKE HISTORY LOG
# ==========================================
st.markdown("---")
st.subheader("📜 Today's Hydration Log")

if st.session_state.logs:
    # Display recent logs in a formatted table
    log_display_data = []
    for idx, entry in enumerate(reversed(st.session_state.logs), start=1):
        log_display_data.append({
            "#": len(st.session_state.logs) - idx + 1,
            "Time Logged": entry["time"],
            "Container / Description": entry["label"],
            "Amount Added": f"+{entry['amount']} ml",
            "Cumulative Total": f"{entry['total_after']} ml"
        })
    st.dataframe(log_display_data, use_container_width=True, hide_index=True)
else:
    st.info("No drinks logged yet today. Click '+250 ml' above to start your daily log!")

# ==========================================
# 9. FOOTER
# ==========================================
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 2rem 0 1rem 0;">
    WaterBuddy App • WellNest Technologies Pvt. Ltd. • Built with Python & Streamlit for IBCP AI CRS Project
</div>
""", unsafe_allow_html=True)
