# AI Travel Planner for Students

This project is a **simple AI-based travel planning system** that helps students design
personalized, budget-friendly itineraries. It does *not* do any online bookings or
live price checks – it only uses rule-based logic on top of small, local data.

> **Viva-friendly one-liner**  
> "This project collects student travel preferences and uses AI-based logic to
> generate a personalized, budget-friendly travel itinerary."

---

## 1. Project Goals

- Keep trips **budget-friendly** for students.
- Make plans **time-efficient** and realistic.
- Use **personal preferences** (nature, food, culture, adventure, etc.).
- Present the final itinerary in a **clean, easy-to-read** format.

No heavy machine learning or external datasets are required – just Python, JSON
data and simple rules.

---

## 2. Technology Stack

| Layer       | Technology                              |
|------------|-----------------------------------------|
| UI         | Streamlit (Python web framework)        |
| Backend    | Python                                  |
| AI Logic   | Rule-based + small generative text      |
| Data       | Local JSON file (`data/places_data.json`)|
| Database   | Not required (optional: SQLite)         |

---

## 3. Folder Structure

ai_travel_planner/
- `app.py` – Streamlit user interface
- `travel_logic.py` – core AI / rule-based logic
- `data/places_data.json` – sample places and student-budget costs
- `requirements.txt` – Python dependencies
- `README.md` – project documentation (this file)

This clean separation is easy to explain in viva.

---

## 4. How the System Works (Flow)

**High-level flow (good to say in viva):**

1. **User Input**  
   The student enters:
   - Destination city (e.g., Bangalore, Mysore, Goa)
   - Number of days
   - Total budget
   - Interests (nature, food, culture, adventure, shopping, history)
   - Travel type (solo / friends)

2. **AI Travel Planner Logic**  
   `travel_logic.py` implements rule-based AI:
   - Calculates approximate **budget per day**.
   - Filters places that match the selected **interests** and **travel type**.
   - Chooses student-friendly, low-cost options first.
   - Avoids repeating the same place on multiple days.

3. **Budget & Preference Matching**  
   - Cheaper places are selected first (greedy algorithm).
   - If budget is low, more free/low-cost options are used.
   - If preferences remove too many places, the system falls back to a
     balanced set so that the itinerary is never empty.

4. **Personalized Itinerary Generation**  
   - For each day (Day 1, Day 2, ...):
     - 2–4 places are selected.
     - An approximate **day cost** is estimated.
     - Student tips and local advice are attached.

5. **Travel Plan Display (Streamlit UI)**  
   - Day-wise itinerary is shown with expand/collapse sections.
   - Each place includes:
     - Name
     - Category (nature/food/culture/...)
     - Approximate cost
     - Why it is recommended
     - Student-specific tip
     - Optional **Google Maps** link
   - Overall estimated cost and budget warnings are displayed.

---

## 5. File-Level Explanation

### `app.py` (UI Layer)

- Built using **Streamlit**.
- Handles **user input form**:
  - Destination, days, budget, interests, travel type.
- Calls `generate_itinerary(...)` from `travel_logic.py`.
- Displays:
  - Trip summary (destination, days, estimated total cost).
  - Day-wise itinerary with collapsible sections.
  - Student-focused tips and optional map links.

### `travel_logic.py` (AI Logic Layer)

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

You can clearly say that this is **rule-based AI** and not heavy ML.

### `data/places_data.json` (Sample Data)

- Small, easy-to-read JSON file.
- Contains example cities like **Bangalore, Mysore, Goa**.
- For each place it stores:
  - Name
  - Categories (nature, food, culture, adventure, shopping, history)
  - Approximate student-budget cost
  - Time required (rough idea)
  - Student tips
  - Optional Google Maps link

You can modify or extend this file without changing the code.

---

## 6. How to Run the Project

1. Create and activate a Python virtual environment (optional but recommended).
2. Install dependencies from `requirements.txt`.
3. Run the Streamlit app:
   - `streamlit run app.py`
4. The app will open in your browser.

Then fill the form and click **"Generate Itinerary"** to see the plan.

---

## 7. What This Project *Does Not* Do

Very important to state clearly in viva:

- ❌ No ticket or hotel booking
- ❌ No payment gateway
- ❌ No live hotel or flight prices
- ❌ No heavy ML model training
- ❌ No external Kaggle dataset

It is a **safe, contained, educational project** that shows how to use
AI-style thinking (rules + simple generation) to solve a real problem for
students.

---

## 8. Example Viva Points

You can mention points like:

- "We used a rule-based AI approach instead of training a complex model."
- "The itinerary is generated day-wise with cost estimates and student tips."
- "All data is local and stored in a JSON file, so there is no privacy issue."
- "Streamlit provides a simple and interactive UI for entering preferences."

This should be more than enough to confidently present and defend the project.
