from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from urllib.parse import quote_plus

import kagglehub
import pandas as pd

# Kaggle dataset id for attractions/places
KAGGLE_DATASET = "saketk511/travel-dataset-guide-to-indias-must-see-places"

# Local CSV (from another Kaggle dataset) that stores
# city-wise accommodation cost ranges.
TRAVEL_COST_CSV_PATH = Path(__file__).parent / "travel cost.csv"

# Where to write the final JSON (same file your app already uses)
OUTPUT_PATH = Path(__file__).parent / "data" / "places_data.json"


def download_kaggle_dataset() -> Path:
    """Download the Kaggle dataset using kagglehub and return its folder path."""
    path = kagglehub.dataset_download(KAGGLE_DATASET)
    return Path(path)


def find_csv_file(root: Path) -> Path:
    """Find the first CSV file under the downloaded dataset directory."""
    csv_files = list(root.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found under {root}")
    # If there are many, just take the first; adjust manually if needed.
    return csv_files[0]


def pick_first_existing_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Return the first column name from candidates that exists in df, else None."""
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _parse_cost_range(text: str) -> Optional[int]:
    """Parse a string like "500 - 3000" and return a *student-friendly* cost.

    We keep it simple: take the **lowest** number we can find, because
    students usually look for the cheapest reasonable accommodation.
    """

    if not isinstance(text, str):
        text = str(text)

    cleaned = text.replace(",", " ")
    digits = re.findall(r"\d+", cleaned)
    if not digits:
        return None

    values = [int(d) for d in digits]
    if not values:
        return None
    return min(values)


def load_travel_costs(path: Path = TRAVEL_COST_CSV_PATH) -> Dict[str, int]:
    """Load city-wise accommodation costs from the second Kaggle dataset.

    CSV columns are typically:
    - City
    - Accomadation_Type
    - Accomdation_Cost (range as text)

    We aggregate a *low-end* per-night accommodation cost per city.
    If the file is missing or malformed, we gracefully fall back to
    an empty dict and keep using only place-based costs.
    """

    if not path.exists():
        print(f"[INFO] Travel cost CSV not found at {path}; using place-based costs only.")
        return {}

    df = pd.read_csv(path)
    if "City" not in df.columns:
        print("[INFO] 'City' column missing in travel cost CSV; skipping accommodation data.")
        return {}

    # Column that stores textual cost ranges
    cost_col: Optional[str] = None
    for candidate in ["Accomdation_Cost", "Accomadation_Cost", "Accommodation_Cost", "Cost"]:
        if candidate in df.columns:
            cost_col = candidate
            break

    if cost_col is None:
        print("[INFO] No accommodation cost column found in travel cost CSV; skipping.")
        return {}

    costs_by_city: Dict[str, List[int]] = defaultdict(list)

    for _, row in df.iterrows():
        city_raw = row.get("City", "")
        city = str(city_raw).strip()
        if not city:
            continue

        cost_val = _parse_cost_range(str(row.get(cost_col, "")))
        if cost_val is None or cost_val <= 0:
            continue

        costs_by_city[city].append(cost_val)

    summary: Dict[str, int] = {}
    for city, values in costs_by_city.items():
        # Use the *minimum* low-end cost across all accommodation types
        # to keep it budget-friendly for students.
        summary[city] = int(min(values))

    print(f"[INFO] Loaded accommodation costs for {len(summary)} cities from '{path.name}'.")
    return summary


def infer_categories(raw: str) -> List[str]:
    """Map free‑text category/description into our small category set."""
    text = (raw or "").lower()

    cats: List[str] = []
    if any(w in text for w in ["beach", "lake", "river", "waterfall", "hill", "mountain", "park", "garden"]):
        cats.append("nature")
    if any(w in text for w in ["trek", "adventure", "paragliding", "rafting", "water sports"]):
        cats.append("adventure")
    if any(w in text for w in ["temple", "church", "mosque", "monastery", "gurudwara", "shrine"]):
        cats.extend(["culture", "history"])
    if any(w in text for w in ["fort", "palace", "museum", "monument", "heritage"]):
        if "history" not in cats:
            cats.append("history")
        if "culture" not in cats:
            cats.append("culture")
    if any(w in text for w in ["market", "bazaar", "shopping", "mall"]):
        cats.append("shopping")
    if any(w in text for w in ["food", "restaurant", "dhaba", "cafe", "street food"]):
        cats.append("food")
    if any(w in text for w in ["relax", "chill", "sunset", "sunrise"]):
        cats.append("relax")

    # Fallback if we couldn't infer anything
    if not cats:
        cats.append("culture")

    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for c in cats:
        if c not in seen:
            seen.add(c)
            unique.append(c)
    return unique


def infer_cost(row: pd.Series) -> int:
    """Infer approximate student cost in INR from possible price columns."""
    # Try a list of likely price/fee columns
    candidates = [
        "Ticket_Price",
        "Ticket Price",
        "Entry_Fee",
        "Entry Fee",
        "Entry_fee",
        "Entry_Fee_Rs",
        "Price",
        "Cost",
    ]
    for col in candidates:
        if col in row.index:
            value = row[col]
            if pd.isna(value):
                continue
            # If it's already numeric
            if isinstance(value, (int, float)):
                if value < 0:
                    continue
                return int(value)

            # If it's a string like "Free", "100-200", "₹150"
            s = str(value).strip().lower()
            if not s:
                continue
            if "free" in s:
                return 0
            # Extract digits from the text
            digits = "".join(ch if ch.isdigit() else " " for ch in s).split()
            if digits:
                try:
                    return int(digits[0])
                except ValueError:
                    pass

    # Fallback: a generic low student budget
    return 300


def infer_time_required_hours(row: pd.Series) -> float:
    """Infer approximate time required to visit the place, in hours."""
    candidates = [
        "Time_required_hours",
        "Time_Required",
        "Time Required",
        "Ideal_Visit_Duration",
        "Ideal Visit Duration",
        "Duration",
    ]
    for col in candidates:
        if col in row.index:
            value = row[col]
            if pd.isna(value):
                continue
            if isinstance(value, (int, float)):
                if value <= 0:
                    continue
                # If it looks like minutes, normalise roughly; else treat as hours
                if value > 0 and value <= 5:
                    return float(value)
                if value > 5 and value < 24:
                    return float(value)
                # >24 probably means minutes
                return float(value) / 60.0

            s = str(value).strip().lower()
            if not s:
                continue
            # Look for patterns like "2-3 hours", "3 hrs", "45 min"
            if "min" in s:
                digits = "".join(ch if ch.isdigit() else " " for ch in s).split()
                if digits:
                    try:
                        mins = float(digits[0])
                        return max(1.0, mins / 60.0)
                    except ValueError:
                        pass
            else:
                digits = "".join(ch if ch.isdigit() else " " for ch in s).split()
                if digits:
                    try:
                        hrs = float(digits[0])
                        return max(1.0, hrs)
                    except ValueError:
                        pass

    # Fallback: 3 hours per place
    return 3.0


def build_map_link(place_name: str, city_name: str) -> str:
    """Build a Google Maps search URL."""
    query = quote_plus(f"{place_name} {city_name}")
    return f"https://www.google.com/maps/search/?api=1&query={query}"


def infer_why(row: pd.Series, place_name: str, city_name: str) -> str:
    """Build a short 'why recommended' text."""
    for col in ["Description", "Short_Description", "Famous_For", "Famous For", "Highlights"]:
        if col in row.index and not pd.isna(row[col]):
            text = str(row[col]).strip()
            if text:
                return text
    return f"Popular place in {city_name} visited by many tourists and students."


def infer_student_tip(cost: int) -> str:
    """Simple, budget-aware student tip."""
    if cost == 0:
        return "Great free spot – perfect when your budget is tight."
    if cost <= 200:
        return "Low-cost place – you can easily fit this into a student budget."
    if cost <= 500:
        return "Plan this along with 1–2 free/low-cost spots to balance your budget."
    return "Consider sharing transport and food with friends to keep the overall day cost under control."


def build_city_level_meta(city_name: str, places: List[Dict[str, Any]], travel_cost_by_city: Dict[str, int]) -> Dict[str, Any]:
    """Compute default_focus, average_daily_cost, tips for a given city.

    We now mix **two Kaggle sources**:
    - Attractions dataset  -> per-place approx_cost
    - Travel-cost dataset  -> low-end accommodation cost per city
    """
    # Aggregate categories to form default_focus
    cat_counter = Counter()
    for p in places:
        for c in p.get("categories", []):
            cat_counter[c] += 1

    if cat_counter:
        top_cats = [c for c, _ in cat_counter.most_common(3)]
        default_focus = ", ".join(top_cats)
    else:
        default_focus = "top highlights"

    # Simple place-based estimate: median place cost × ~2 places/day
    place_based_daily = 0
    if places:
        costs = sorted(p.get("approx_cost", 0) for p in places if p.get("approx_cost", 0) is not None)
        if costs:
            mid = costs[len(costs) // 2]
            place_based_daily = max(0, mid * 2)

    # Accommodation-based estimate from the travel-cost dataset
    accom_cost = travel_cost_by_city.get(city_name)

    if accom_cost is not None:
        # Rough rule: daily budget ≈ accommodation + place-based spends
        avg_daily_cost = int(max(300, accom_cost + place_based_daily))
    else:
        # Fallback: if we don't know accommodation, use only places
        avg_daily_cost = int(max(300, place_based_daily or 1000))

    general_tips = [
        "Travel with friends to share room and cab costs.",
        "Prefer public transport or walking instead of point-to-point cabs.",
        "Carry a refillable water bottle and some snacks.",
        "Check for student discounts at museums and attractions.",
    ]
    local_tips = [
        "Try to group nearby places on the same day to save travel cost and time.",
        "Start your day a bit early to avoid crowds and heat wherever possible.",
    ]

    return {
        "city_name": city_name,
        "default_focus": default_focus,
        "average_daily_cost": avg_daily_cost,
        "general_tips": general_tips,
        "local_tips": local_tips,
        "places": places,
    }


def convert_dataframe_to_places_json(df: pd.DataFrame, travel_cost_by_city: Dict[str, int]) -> Dict[str, Any]:
    """Convert the Kaggle DataFrame into the existing places_data.json schema.

    `travel_cost_by_city` comes from the second Kaggle dataset and is
    used to enrich each city's average_daily_cost.
    """
    # Try to locate column names we need
    city_col = pick_first_existing_column(
        df,
        ["City", "city", "Nearest_City", "Nearest City", "Location"]
    ) or "City"
    name_col = pick_first_existing_column(
        df,
        ["Place_Name", "Place Name", "Attraction", "Attraction_Name", "Name"]
    ) or "Place_Name"
    category_col = pick_first_existing_column(
        df,
        ["Category", "Type", "Place_Type", "Place Type"]
    )
    desc_col = pick_first_existing_column(
        df,
        ["Description", "Short_Description", "Famous_For", "Famous For", "Highlights"]
    )

    # Ensure fallback columns exist in the frame (to avoid KeyError later)
    for col in [city_col, name_col]:
        if col not in df.columns:
            raise KeyError(f"Expected column '{col}' not found in dataset. "
                           f"Please adjust column mappings in the script.")

    # We'll build per-city data here
    city_places: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    for _, row in df.iterrows():
        city_name = str(row.get(city_col, "") or "").strip()
        if not city_name:
            city_name = "Unknown City"

        place_name = str(row.get(name_col, "") or "").strip()
        if not place_name:
            # Skip rows without a proper place name
            continue

        raw_cat = ""
        if category_col and category_col in row.index and not pd.isna(row[category_col]):
            raw_cat = str(row[category_col])
        elif desc_col and desc_col in row.index and not pd.isna(row[desc_col]):
            raw_cat = str(row[desc_col])

        categories = infer_categories(raw_cat)
        approx_cost = infer_cost(row)
        time_required_hours = infer_time_required_hours(row)
        why = infer_why(row, place_name, city_name)
        student_tip = infer_student_tip(approx_cost)
        map_link = build_map_link(place_name, city_name)

        place_obj: Dict[str, Any] = {
            "name": place_name,
            "categories": categories,
            "approx_cost": approx_cost,
            "time_required_hours": time_required_hours,
            "best_for": ["solo", "friends"],  # generic but safe for our app's filters
            "why": why,
            "student_tip": student_tip,
            "map_link": map_link,
        }

        city_places[city_name].append(place_obj)

    # Now build the top-level JSON structure, city by city
    result: Dict[str, Any] = {}
    for city_name, places in sorted(city_places.items(), key=lambda x: x[0].lower()):
        result[city_name] = build_city_level_meta(city_name, places, travel_cost_by_city)

    return result


def main() -> None:
    print("Downloading Kaggle dataset (or using cached copy)...")
    dataset_dir = download_kaggle_dataset()
    print(f"Dataset directory: {dataset_dir}")

    csv_path = find_csv_file(dataset_dir)
    print(f"Using CSV file: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from attractions dataset.")

    # Load city-wise accommodation costs from the second Kaggle dataset
    # (already downloaded and saved locally as 'travel cost.csv').
    travel_cost_by_city = load_travel_costs()

    places_json = convert_dataframe_to_places_json(df, travel_cost_by_city)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(places_json, f, ensure_ascii=False, indent=2)

    print(f"Written processed data to: {OUTPUT_PATH}")
    print("Now you can run the Streamlit app with the new data.")


if __name__ == "__main__":
    main()
