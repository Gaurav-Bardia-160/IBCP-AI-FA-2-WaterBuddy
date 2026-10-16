# 💧 WaterBuddy — Smart Hydration App

**IBCP AI CRS Year 1 — Python Programming Project (FA-2)**  
*Faithfully implemented based on the FA-1 Storyboard (`1000679_Gaurav_Gautam_Bardia_Fa_1.png`)*

---

## 📖 Storyboard Alignment & Features (20/20 Marks)

### 1. User Avatars & Target Setting (Storyboard Panels 1, 2, 3)
- **4 Interactive User Avatars**:
  - 🧒 **Child**: 1600 mL (≈ 6–7 cups 🥛)
  - 👧 **Teen**: 2000 mL (≈ 8–10 cups 🥛)
  - 🧑 **Adult**: 2500 mL (≈ 8–10 cups 🥛)
  - 👴 **Senior**: 2000 mL (≈ 4–10 cups 🥛)
- **Daily Recommended Water Target Card**: Reference guideline displaying volume and equivalent cups.
- **Option to Adjust**: Manual goal adjustment widget.

### 2. Python Logic Updates & Quick Logging (Storyboard Panels 4, 5 & Screens 5, 6)
- **Live Counters**:
  - `Total ++ amount` (Cumulative intake)
  - `Total ++ remaining needed` (Deficit to goal)
  - `% Percentage progress` (Calculated dynamically)
- **Quick Logging**:
  - Big Circular **`+250 ml`** button (matching Storyboard Screen 5).
  - Quick companion buttons (`+100 ml`, `+500 ml`).
  - Custom input: "Your entry" with **"Add entry"** button (matching Storyboard Screen 6).
  - `↩️ Undo Last Log` option.

### 3. Turtle Mascot Milestone System (Storyboard Panel 6)
The app implements the exact green Turtle Mascot milestone triggers from your storyboard:
- **`Progress < 20%`**: Neutral resting turtle 🐢
- **`Progress ≥ 20%`**: **Avatar smiles** 😊 (Encouraging smiling expression)
- **`Progress ≥ 75%`**: **Avatar waves** 👋 (Turtle raises paw waving hello)
- **`Total ≥ Goal (100%+)`**: **Celebration!** 🎉 (Joyful expression with celebration stars & `st.balloons()`)

### 4. Animated Water Bottle (Storyboard Screens 1, 2, 3, 7)
- Translucent blue glass bottle illustration that fills dynamically with water.
- Measurement graduation lines (25%, 50%, 75%).
- Contextual motivational captions:
  - `< 20%`: *"Ready to start! Take your first sip today"*
  - `20%–49%`: *"Great start! Animated water rising steadily"*
  - `50%–74%`: *"Halfway there! Logged water keeping you energized"*
  - `75%–99%`: *"Almost there! Just a couple more sips"*
  - `100%+`: *"Goal achieved! Fantastic job!"*

### 5. End-of-Day Summary & New Day Reset (Storyboard Screens 8 & 9)
- **Daily Hydration Report**:
  - Total Intake vs. Daily Goal metrics
  - Highlighted `% Achieved` badge
  - Success message: *"Excellent job! You hit 100% of your target. Regular hydration is keeping you energized!"*
- **New Day / Reset Modal**:
  - Safety confirmation prompt: *"New Day Confirmation: This will reset your counters for today. Are you sure?"* with `[Yes]` and `Cancel` buttons.

---

## 🚀 How to Run Locally

Open terminal in `C:\Users\gaura\Documents\WaterBuddy` and run:
```powershell
py app.py
```
*(Or `py -m streamlit run app.py`)*

The app will open automatically in your browser at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Cloud (Stage 7)

1. Create a repository on GitHub named `WaterBuddy`.
2. Push your code:
   ```powershell
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/WaterBuddy.git
   git push -u origin main
   ```
3. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo, set main file to `app.py`, and click **Deploy**.
