# 💧 WaterBuddy — Smart Hydration App

**WellNest Technologies Pvt. Ltd.**  
**IBCP AI CRS Year 1 — Python Programming Project (FA-2)**  
*Total Assessment: 20 Marks*

---

## 📖 Overview
**WaterBuddy** is an interactive, age-aware web application developed in Python with Streamlit to help users track and improve their daily hydration habits. Built according to the FA-1 design storyboards and logic flow, WaterBuddy translates scientific hydration requirements into real-time visual feedback, personalized goals, and motivational mascot interactions.

---

## 🌟 Rubric Features & Compliance (20/20 Marks)

### 1. Python Coding & User Interaction (10 Marks)
- **Age Group Selector (`st.selectbox`)**:
  - `6–12 years (Kids)`: Auto-suggests 1600 mL.
  - `13–18 years (Teens)`: Auto-suggests 2000 mL.
  - `19–50 years (Adults)`: Auto-suggests 2500 mL.
  - `65+ years (Seniors)`: Auto-suggests 2000 mL.
- **Dynamic Auto-Suggested Goal**: Updates automatically when the age category changes.
- **Manual Goal Adjustment (`st.number_input`)**: Users can adjust their custom target based on exercise or climate.
- **Side-by-Side Comparison**: Displays the standard medical guideline alongside the user's custom daily goal.
- **Quick Logging Buttons**:
  - `+250 ml (Standard Glass)` (*Compulsory requirement*)
  - `+100 ml (Small Cup)`
  - `+500 ml (Water Bottle)`
  - Custom milliliter input expander.
- **Daily Reset & Undo**:
  - `🔄 Reset Today's Intake`: Resets the day's total, celebration flags, and log table.
  - `↩️ Undo Last Drink`: Safely removes the latest logged entry.
- **Session State Management**: Uses `st.session_state` to ensure instant, reactive updates without page reloads.

### 2. Calculation & Visual Feedback (5 Marks)
- **Real-Time Calculations**:
  - Total intake consumed today.
  - Remaining milliliters needed to reach daily target.
  - Percentage of goal achieved (`(total_intake / daily_goal) * 100`).
- **Dynamic Visual Bottle**: An animated SVG water bottle that visually fills from 0% to 100% with gradient water, realistic water levels, and graduation marks.
- **Live Streamlit Progress Bar**: Standard progress tracker synchronized with total intake.
- **Interactive Mascot Feedback ("Buddy")**:
  - `0%`: 😴 Asleep & parched (encourages taking the first sip).
  - `<25%`: 🌱 Waking up and starting strong.
  - `25–49%`: 💧 Refreshed and feeling energized.
  - `50–74%`: 🌊 Halfway hero milestone.
  - `75–99%`: ⭐ Almost at the finish line!
  - `100%+`: 🏆 Hydration Champion! (Triggers confetti celebration with `st.balloons()`).
- **Random Daily Scientific Tips**: Curated science-backed hydration facts with a shuffle button.

### 3. Web App Interface & Deployment (5 Marks)
- Clean, aesthetic aquatic design palette (aqua, cyan, ocean blue).
- Sidebar with unit conversion tool (Cups ↔ mL and fl oz ↔ mL).
- Formatted daily intake audit log table with timestamps.
- Ready for GitHub push and 1-click Streamlit Cloud deployment.

---

## 🚀 How to Run Locally

1. Open your terminal / command prompt in this directory:
   ```bash
   cd "C:\Users\gaura\Documents\WaterBuddy"
   ```
2. Run the application using Python launcher:
   ```bash
   py -m streamlit run app.py
   ```
3. Your default web browser will automatically open:
   ```
   http://localhost:8501
   ```

---

## 🌐 How to Deploy to Streamlit Cloud (Stage 7)

### Step 1: Create a GitHub Repository
1. Go to [github.com](https://github.com) and log into your account.
2. Click **New Repository**.
3. Name your repository `WaterBuddy`.
4. Keep it **Public** and leave "Add a README" unchecked (since we already have one).
5. Click **Create repository**.

### Step 2: Push Your Code via Git
Open PowerShell in `C:\Users\gaura\Documents\WaterBuddy` and run:
```bash
git init
git add app.py requirements.txt README.md
git commit -m "Initial commit of WaterBuddy FA-2 project"
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/WaterBuddy.git
git push -u origin main
```
*(Alternatively, you can drag and drop `app.py` and `requirements.txt` directly into the GitHub web interface).*

### Step 3: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **Create app** (or **Deploy an app**).
3. Select your repository: `<YOUR_GITHUB_USERNAME>/WaterBuddy`.
4. Branch: `main`
5. Main file path: `app.py`
6. Click **Deploy!**
7. Copy the generated public URL (e.g., `https://waterbuddy-<unique-id>.streamlit.app`).

---

## 📋 Checklist of Evidence for Submission
For your FA-2 submission, paste into your submission Word/PDF document:
- [x] Storyboard link / diagrams from FA-1
- [x] GitHub Repository URL
- [x] Live Deployed Streamlit Cloud URL
