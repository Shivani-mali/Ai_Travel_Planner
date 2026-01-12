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

