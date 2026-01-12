import streamlit as st

from travel_logic import generate_itinerary, load_places_data


def main() -> None:
    """Streamlit UI for the AI-based student travel planner.

    This file focuses on **user interaction and display**, while all
    "AI logic" lives in travel_logic.py. This separation is very easy
    to explain during viva.
    """

    st.set_page_config(
        page_title="Student Travel Planner",
        page_icon="🧳",
        layout="centered",
    )

    # Global font and basic theming: Times New Roman for main text,
    # clearer headings, and visible links with a soft card-style layout.
    st.markdown(
        """
        <style>
        /* Inter variable font with optical sizing */
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300..700&display=swap');

        /* Base Inter style, similar to the snippet you shared */
        .inter-text {
            font-family: "Inter", sans-serif;
            font-optical-sizing: auto;
            font-weight: 400;
            font-style: normal;
        }

        /* Use Inter for main content in the app */
        html, body,
        [class^="css"],
        .stMarkdown, .stText,
        .stButton > button,
        input, textarea, select,
        .stSelectbox, .stMultiSelect, .stNumberInput,
        .stTextInput, .stDateInput, .stRadio, .stCheckbox,
        .stAlert, .stSidebar, .st-expander, .st-expanderHeader,
        .st-bw, .st-bx, .st-by, .st-bz {
            font-family: "Inter", sans-serif !important;
            font-optical-sizing: auto !important;
            font-style: normal !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: "Inter", sans-serif !important;
            font-weight: 600 !important;
            font-optical-sizing: auto !important;
            font-style: normal !important;
        }

        /* Make links clearly visible */
        a, .stMarkdown a {
            color: #0056b3 !important;
            text-decoration: underline !important;
        }

        /* Page background and main container */
        body {
            background: radial-gradient(circle at top, #fdfbfb 0, #ebedee 55%, #e2e2f0 100%);
        }

        .block-container {
            max-width: 800px;
            margin: auto;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        /* Cards for summary and sections */
        .stMarkdown h2, .stMarkdown h3 {
            margin-top: 1.8rem;
        }

        .summary-card, .tips-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06);
            margin-bottom: 1.2rem;
        }

        /* Nicer expanders for each day */
        .st-expander {
            background-color: #ffffff !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            margin-bottom: 0.9rem;
        }

        .st-expander summary {
            font-weight: 600;
        }

        /* Primary button styling */
        .stButton > button {
            background-color: #0056b3 !important;
            color: #ffffff !important;
            border-radius: 999px !important;
            padding: 0.4rem 1.4rem !important;
            border: none !important;
        }

        .stButton > button:hover {
            background-color: #004495 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Student Travel Planner")
    st.write("Plan a simple, budget-friendly trip in a few clicks.")

    # Load sample data (cities & places)
    places_data = load_places_data()

    # Build destination list from *all* cities in the dataset.
    # (Earlier we showed only cities with many places, but that hid
    # some cities like Kolhapur; this keeps the UI simple.)
    city_options = sorted(places_data.keys()) + ["Other / Not listed"]
    with st.form("travel_form"):
        st.subheader("Trip details")

        destination = st.selectbox("Destination city", city_options, index=0)
        num_days = st.number_input("Number of days", min_value=1, max_value=14, value=3)
        total_budget = st.number_input(
            "Total trip budget (₹)",
            min_value=0,
            value=5000,
            step=500,
        )

        interests = st.multiselect(
            "Interests",
            ["nature", "food", "culture", "adventure", "shopping", "history"],
            default=["nature", "food"],
        )

        travel_type = st.selectbox(
            "Travel type",
            ["solo", "friends"],
        )

        submitted = st.form_submit_button("Generate Itinerary")

    if submitted:
        with st.spinner("Creating your itinerary..."):
            itinerary = generate_itinerary(
                destination=destination,
                num_days=int(num_days),
                total_budget=int(total_budget) if total_budget > 0 else None,
                interests=list(interests),
                travel_type=travel_type.lower(),
                places_data=places_data,
            )

        st.success("Itinerary ready. 🎉")

        st.subheader("Trip summary")
        st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
        st.write(f"**Destination:** {itinerary['destination']}")
        # Show both what the user typed and what the planner actually used.
        requested_days = itinerary.get("requested_days", itinerary["num_days"])
        st.write(f"**Days you requested:** {requested_days}")
        st.write(f"**Days planned in this city:** {itinerary['num_days']}")

        # Optional info: how many days this budget roughly supports
        # for this city, based on average_daily_cost from the dataset.
        city_info = places_data.get(destination)
        if total_budget and city_info is not None:
            avg_daily_cost = city_info.get("average_daily_cost")
            if isinstance(avg_daily_cost, (int, float)) and avg_daily_cost > 0:
                suggested_days = max(1, int(total_budget // avg_daily_cost))
                # Also respect how many days of sightseeing this city
                # realistically supports based on available places.
                max_activity_days = itinerary.get("max_activity_days")
                if isinstance(max_activity_days, int) and max_activity_days > 0:
                    suggested_days = max(1, min(suggested_days, max_activity_days))

                st.write(
                    f"**Budget-based suggestion:** With ₹{int(total_budget):,}, "
                    f"a typical student trip in this city is about "
                    f"{suggested_days} day(s)."
                )

        if itinerary.get("total_estimated_cost") is not None:
            est = itinerary["total_estimated_cost"]
            st.write(f"**Estimated total cost:** ₹{est:.0f} (approx.)")

            if total_budget:
                diff = total_budget - est
                if diff >= 0:
                    st.write(f"**Budget buffer:** You may save around ₹{diff:.0f}.")
                else:
                    st.write(
                        f"**Budget warning:** Plan exceeds budget by about ₹{-diff:.0f}. "
                        "You can remove 1–2 paid activities to fit the budget."
                    )

        if itinerary.get("daily_budget") is not None:
            st.write(f"**Approx. daily budget:** ₹{itinerary['daily_budget']:.0f} per day")

        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Day-wise itinerary")
        for day in itinerary["days"]:
            with st.expander(f"Day {day['day']} – {day['focus']}"):
                st.write(day["description"])
                st.write(f"**Estimated cost for this day:** ₹{day['estimated_cost']:.0f}")

                for place in day["places"]:
                    st.markdown(f"**{place['name']}**")
                    st.write(f"Cost: ₹{place['approx_cost']}")
                    if place.get("tip"):
                        st.write("Tip: " + place["tip"])
                    if place.get("map_link"):
                        st.markdown(f"[Open in Google Maps]({place['map_link']})")
                    st.markdown("---")

                if day.get("extra_tips"):
                    st.write("Extra local tips:")
                    for tip in day["extra_tips"]:
                        st.write(f"- {tip}")

        if itinerary.get("general_tips"):
            st.subheader("Tips for students")
            for tip in itinerary["general_tips"]:
                st.write(f"- {tip}")

        st.caption(
            "Note: All costs are approximate and meant for learning/demo purposes, "
            "not real-time booking or pricing."
        )


if __name__ == "__main__":
    main()
