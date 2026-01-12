🌍 AI-Based Student Travel Planner for Indian Cities

A rule-based AI travel planning web application built with **Python** and **Streamlit**, designed to help students plan **affordable** and **realistic** trips across Indian cities.
The system generates **day-wise, budget-aware itineraries** by combining student preferences with curated local attractions, keeping the logic simple and fully explainable.

---

🏫 EDUNET FOUNDATION PROJECT

This project has been developed as part of the **EDUNET FOUNDATION** academic program.
It is submitted for **learning, evaluation, and demonstration** purposes, focusing on the practical application of **AI concepts** to a real-world student problem.

---

📌 Problem Statement

Students often want to travel but face multiple challenges such as:

- Limited budgets
- Travel apps focused on luxury and bookings
- Unrealistic trip durations
- Manual and time-consuming research
- Poor budget estimation leading to overspending

As a result, students struggle to plan efficient, economical, and interest-based trips.

---

💡 Proposed Solution

The **AI-Based Student Travel Planner** acts as a smart planning assistant that:

- Accepts basic travel inputs (city, days, budget, interests, travel type)
- Generates a **day-wise travel itinerary**
- Automatically limits trip days based on available attractions
- Recalculates budgets for realistic planning
- Works completely **offline** using local data (no external APIs or booking systems)

The focus is on **clarity, transparency, and explainable rule-based AI**, not heavy ML models.

---

✨ Key Features

- ✅ Rule-based AI system (no machine learning required)
- ✅ Auto-adjusts trip days based on attraction availability
- ✅ Budget-aware **daily** and **total** cost estimation
- ✅ Personalized itineraries based on interests and travel type (solo / friends)
- ✅ Never shows an "empty" trip – falls back to reasonable defaults
- ✅ Clean, modern, and student-friendly **Streamlit UI**
- ✅ Works fully offline using local **JSON** data

---

🧠 How the System Works

1. Student enters destination city, number of days, total budget, interests, and travel type.
2. The system loads attraction data from `data/places_data.json`.
3. Places are filtered based on interests and travel type.
4. The system estimates how many sightseeing days the city can realistically support.
5. Planned days are auto-limited if needed (e.g., city has attractions only for 2 days).
6. A **cost-effective, day-wise itinerary** is generated using a simple greedy strategy.
7. A clear trip summary and **budget suggestion** is displayed.

---

⚙️ Technology Stack

- **Frontend / UI:** Streamlit
- **Backend:** Python
- **AI Logic:** Rule-based decision system (no ML training)
- **Data Storage:** Local JSON (`data/places_data.json`)
- **Source Data:** Kaggle CSVs (Indian tourist attractions & travel cost data), preprocessed offline
- **Deployment:** Streamlit (local or cloud)

---

🏗️ Project Structure

Repository root: `Ai_Travel_Planner/`

- `app.py` – Streamlit UI (main entrypoint)
- `travel_logic.py` – rule-based AI / itinerary generation logic
- `build_places_from_kaggle.py` – script to build `places_data.json` from Kaggle CSVs
- `Top Indian Places to Visit.csv` – raw attractions data (from Kaggle)
- `travel cost.csv` – raw travel cost data (from Kaggle)
- `data/places_data.json` – processed, student-friendly places and costs
- `requirements.txt` – Python dependencies
- `README.md` – project documentation (this file)

This separation is simple to understand and easy to explain during viva.

---

## 4. How the System Works

### Step 1 – User Input
The student enters:
- Destination city (e.g., Bangalore, Mysore, Goa)
- Number of days
- Total budget
- Interests (nature, food, culture, adventure, shopping, history)
- Travel type (solo / friends)

### Step 2 – AI Travel Planner Logic
`travel_logic.py` implements **rule‑based AI**:
- Calculates approximate **budget per day**.
- Filters places that match the selected **interests** and **travel type**.
- Prefers student‑friendly, low‑cost options.
- Avoids repeating the same place on multiple days.

### Step 3 – Budget & Preference Matching
- Cheaper places are selected first (simple greedy strategy).
- If budget is low, more free / low‑cost options are chosen.
- If preferences are too strict and remove most places, the system falls back
  to a balanced set so the itinerary is never empty.

### Step 4 – Personalized Itinerary Generation
For each day (Day 1, Day 2, …):
- 2–4 places are selected.
- An approximate **day cost** is estimated.
- Student tips and local advice are attached.

### Step 5 – Display in Streamlit UI
- Day‑wise itinerary with expand/collapse sections.
- Each place shows:
  - Name
  - Category (nature/food/culture/...)
  - Approximate cost
  - Why it is recommended
  - Student‑specific tip
  - Optional **Google Maps** link
- Overall estimated cost and budget warnings are displayed.

---

## 5. File‑Level Overview

### `app.py` – UI Layer

- Built using **Streamlit**.
- Handles the **user input form**:
  - Destination, days, budget, interests, travel type.
- Calls `generate_itinerary(...)` from `travel_logic.py`.
- Displays:
  - Trip summary (destination, days, estimated total cost).
  - Day‑wise itinerary with collapsible sections.
  - Student‑focused tips and optional map links.

### `travel_logic.py` – AI Logic Layer

Implements simple, explainable AI logic:

- Loads data from `data/places_data.json`.
- Filters places based on:
  - Selected interests
  - Travel type (solo / friends)
- Computes a **daily budget** from the total budget and number of days.
- Uses a simple **greedy algorithm**:
  - Sorts places by approximate cost.
  - Picks cheaper places first until the daily budget is roughly filled.
  - Tries not to repeat the same place on multiple days.
- Returns a structured Python dictionary (destination, days, costs, tips).

You can clearly say that this is **rule‑based AI**, not heavy machine learning.

### `data/places_data.json` – Sample Data

- Small, easy‑to‑read JSON file.
- Contains example cities like **Bangalore, Mysore, Goa**.
- For each place it stores:
  - Name
  - Categories (nature, food, culture, adventure, shopping, history)
  - Approximate student‑budget cost
  - Time required (rough estimate)
  - Student tips
  - Optional Google Maps link

You can modify or extend this file without changing the core code.

---

## 6. Running the Project Locally

### Prerequisites
- Python 3.10+ (project tested with Python 3.12)
- (Optional but recommended) Virtual environment

---

## 7. What This Project *Does Not* Do

Good to mention clearly (especially in viva):

- ❌ No ticket or hotel booking
- ❌ No payment gateway
- ❌ No live hotel or flight prices
- ❌ No heavy ML model training
- ❌ No external real‑time APIs

It is a **safe, contained, educational project** that shows how to use
AI‑style thinking (rules + simple generation) to solve a real problem for
students.


Use the **live demo link** plus a short explanation of the flow to give a strong, clear project presentation.
