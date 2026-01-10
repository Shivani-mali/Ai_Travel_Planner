## AI Travel Planner for Students

An AI‑style travel planning system that helps students create **personalized, budget‑friendly itineraries** using simple, explainable rules on top of small local data. No bookings, no payments, no live price scraping – just clean logic you can easily explain in a viva.

> "This project collects student travel preferences and uses rule‑based AI logic to generate a personalized, budget‑friendly travel itinerary."

---

## 🚀 Live Demo

Try the deployed app here (no setup needed):

**https://aitravelplanner-qnghyfqvasrgccsupj5qus.streamlit.app/**

---

## 1. Project Goals

- Keep trips **budget‑friendly** for students.
- Make plans **time‑efficient** and realistic.
- Use **personal preferences** (nature, food, culture, adventure, etc.).
- Present the final itinerary in a **clean, easy‑to‑read** format.

No heavy machine learning or external online APIs are required – just Python, JSON
data and simple rule‑based logic.

---

## 2. Technology Stack

| Layer       | Technology                               |
|------------|-------------------------------------------|
| UI         | Streamlit (Python web framework)          |
| Backend    | Python                                    |
| AI Logic   | Rule‑based heuristic + light text output  |
| Data       | Local JSON file (`data/places_data.json`) |
| Database   | Not required (optional: SQLite)           |

---

## 3. Project Structure

`ai_travel_planner/`
- `app.py` – Streamlit user interface
- `travel_logic.py` – core AI / rule‑based logic
- `data/places_data.json` – sample places and student‑budget costs
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

### Setup

From the project root (`ai_travel_planner/`):

1. Create and activate a virtual environment (you can adapt names/paths):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

4. Open the URL shown in the terminal (usually `http://localhost:8501`).

Then fill the form and click **"Generate Itinerary"** to see the plan.

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

---

## 8. Viva / Presentation Points

You can confidently say:

- "We used a rule‑based AI approach instead of training a complex model."
- "The itinerary is generated day‑wise with cost estimates and student tips."
- "All data is local and stored in a JSON file, so there is no privacy issue."
- "Streamlit provides a simple and interactive UI for entering preferences."

Use the **live demo link** plus a short explanation of the flow to give a strong, clear project presentation.
