import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from urllib.parse import quote_plus


DATA_PATH = Path(__file__).parent / "data" / "places_data.json"


def load_places_data(path: Optional[Path] = None) -> Dict[str, Any]:
    """Load sample city and places data from JSON.

    Data is intentionally small and human-readable so that it can be
    explained easily during viva and modified by students.
    """
    data_path = path or DATA_PATH
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _filter_places(city_data: Dict[str, Any], interests: List[str], travel_type: str) -> List[Dict[str, Any]]:
    """Filter places using simple rule-based logic.

    Rules:
    - Prefer places that match at least one selected interest.
    - Prefer places that are marked as suitable for the chosen travel type.
    - If filtering removes everything, gracefully fall back to all places
      so that the user still gets a complete plan.
    """
    places = list(city_data.get("places", []))

    # Interest-based filtering
    if interests:
        interested = [
            p
            for p in places
            if any(i in p.get("categories", []) for i in interests)
        ]
        if interested:
            places = interested

    # Travel-type filtering (solo / friends)
    if travel_type:
        suitable = [
            p
            for p in places
            if not p.get("best_for") or travel_type in p.get("best_for", [])
        ]
        if suitable:
            places = suitable

    return places


def _build_day_plan(
    day_number: int,
    available_places: List[Dict[str, Any]],
    daily_budget: Optional[float],
    used_place_names: Set[str],
    city_data: Dict[str, Any],
    interests: List[str],
    city_name: str,
) -> Dict[str, Any]:
    """Create a simple day plan using greedy, budget-aware selection.

    This is **AI-style logic without ML training**:
    - Try to choose cheaper places first.
    - Try not to repeat the same place on multiple days.
    - Respect (approximately) the daily budget.
    """
    # Prefer unused places and sort by approximate cost (cheapest first)
    candidates = [p for p in available_places if p.get("name") not in used_place_names]

    # IMPORTANT change:
    # If there are no unused places left, we *do not* repeat the
    # same attractions again. Instead, we will keep the day light
    # with no new places, so that the itinerary reflects the
    # limited data for this city (good viva point).
    candidates.sort(key=lambda p: p.get("approx_cost", 0))

    selected: List[Dict[str, Any]] = []
    spent = 0.0

    for place in candidates:
        cost = float(place.get("approx_cost", 0) or 0)
        # Allow a small 20% flexibility over the daily budget
        if daily_budget is not None and spent + cost > daily_budget * 1.2:
            continue
        selected.append(place)
        used_place_names.add(place.get("name", ""))
        spent += cost
        # Keep days small and realistic (2–4 activities)
        if len(selected) >= 3:
            break

    focus = ", ".join(interests) if interests else city_data.get("default_focus", "top highlights")
    city_label = city_data.get("city_name") or city_name or "the city"

    if selected:
        description = (
            f"Day {day_number}: Focus on {focus.lower()} in and around {city_label}. "
            "The plan mixes student-friendly and budget-conscious options."
        )
    else:
        # No specific paid attractions planned for this day – leave it
        # open for rest, local markets, street food and self‑exploration.
        description = (
            f"Day {day_number}: Easy, flexible day in {city_label}. Use this day "
            "for rest, local walks, markets and your own favourite spots."
        )

    day_places = []
    for p in selected:
        raw_link = p.get("map_link", "") or ""
        if raw_link.startswith("http"):
            map_link = raw_link
        else:
            # Fallback: build a stable Google Maps search URL using place name + city
            query = quote_plus(f"{p.get('name', '')} {city_label}")
            map_link = f"https://www.google.com/maps/search/?api=1&query={query}"

        day_places.append(
            {
                "name": p.get("name"),
                "categories": p.get("categories", []),
                "approx_cost": p.get("approx_cost", 0),
                "why": p.get("why", "Popular and student-friendly place."),
                "tip": p.get("student_tip", ""),
                "map_link": map_link,
            }
        )

    return {
        "day": day_number,
        "focus": focus.title() if focus else "Highlights",
        "description": description,
        "places": day_places,
        "estimated_cost": spent,
        "extra_tips": city_data.get("local_tips", []),
    }


def generate_itinerary(
    destination: str,
    num_days: int,
    total_budget: Optional[int],
    interests: List[str],
    travel_type: str,
    places_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Main rule-based "AI" travel planner.

    This function is perfect to explain in viva:
    - It collects user preferences (destination, days, budget, interests).
    - It calculates an approximate *budget per day*.
    - It matches nearby places with the user's interests.
    - It generates a clear, day-wise plan with tips for students.

    No heavy ML or training is required – only Python conditions, loops
    and simple scoring logic.
    """
    # Number of days the user requested in the UI.
    if num_days <= 0:
        num_days = 1
    requested_days = num_days

    if places_data is None:
        places_data = load_places_data()

    # If the destination is unknown, fall back to the first known city
    # but keep the original destination name for display.
    if destination in places_data:
        city_key = destination
    else:
        city_key = next(iter(places_data.keys()))

    city_data = places_data[city_key]
    city_name = destination

    # Filter places once based on interests and travel type.
    available_places = _filter_places(city_data, interests, travel_type)

    # How many unique attractions does this city currently have for the
    # given interests and travel type?
    available_place_count = len(available_places)
    if available_place_count:
        # We normally show up to 3 activities per day, so this gives an
        # approximate upper bound on how many *active sightseeing days*
        # the city can meaningfully support.
        max_activity_days = (available_place_count + 2) // 3
    else:
        max_activity_days = 0

    # Auto-limit the number of planned sightseeing days based on how
    # many attractions we actually have. For example, if there is only
    # one place in the city, we generate a 1-day plan even if the user
    # typed 3 days.
    if max_activity_days > 0:
        planned_days = min(requested_days, max_activity_days)
    else:
        # No specific attractions matched – still keep at least one
        # flexible day so the app returns something useful.
        planned_days = max(1, requested_days)

    daily_budget: Optional[float] = None
    if total_budget is not None and total_budget > 0:
        daily_budget = total_budget / float(planned_days)

    used_place_names: Set[str] = set()
    days: List[Dict[str, Any]] = []
    total_estimated_cost = 0.0

    for day in range(1, planned_days + 1):
        day_plan = _build_day_plan(
            day_number=day,
            available_places=available_places,
            daily_budget=daily_budget,
            used_place_names=used_place_names,
            city_data=city_data,
            interests=interests,
            city_name=city_name,
        )
        days.append(day_plan)
        total_estimated_cost += float(day_plan.get("estimated_cost", 0) or 0)

    general_tips = [
        "Travel with friends to share room and cab costs.",
        "Prefer public transport or walking instead of point-to-point cabs.",
        "Carry a refillable water bottle and basic snacks.",
        "Check for student discounts at museums and attractions.",
    ]
    general_tips.extend(city_data.get("general_tips", []))

    return {
        "destination": city_name,
        "num_days": planned_days,
        "requested_days": requested_days,
        "available_place_count": available_place_count,
        "max_activity_days": max_activity_days,
        "total_estimated_cost": total_estimated_cost if total_estimated_cost > 0 else None,
        "daily_budget": daily_budget,
        "days": days,
        "general_tips": general_tips,
    }
