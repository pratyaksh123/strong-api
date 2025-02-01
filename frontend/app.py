import streamlit as st
import requests
import pandas as pd
import altair as alt
from dotenv import load_dotenv

import os

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "192.168.0.214")

# ✅ Clean Title with Less Space
st.markdown("<h1 style='text-align: center;'>🏋️‍♂️ Gym PR Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Track your strength progress over time with clear visualizations!</p>", unsafe_allow_html=True)


# ✅ Initialize Theme Settings
ms = st.session_state
if "themes" not in ms: 
    ms.themes = {
        "current_theme": "light",
        "refreshed": True,
        
        "light": {
            "theme.base": "light",
            "theme.backgroundColor": "white",
            "theme.primaryColor": "#5591f5",
            "theme.secondaryBackgroundColor": "#82E1D7",
            "theme.textColor": "#0a1464",
            "button_face": "🌙"
        },

        "dark": {
            "theme.base": "dark",
            "theme.backgroundColor": "#121212",
            "theme.primaryColor": "#c98bdb",
            "theme.secondaryBackgroundColor": "#5591f5",
            "theme.textColor": "white",
            "button_face": "☀️"
        },
    }

def ChangeTheme():
    """Switches the theme dynamically and forces rerun."""
    previous_theme = ms.themes["current_theme"]
    theme_dict = ms.themes["dark"] if previous_theme == "light" else ms.themes["light"]

    for key, val in theme_dict.items():
        if key.startswith("theme"):
            st._config.set_option(key, val)  

    ms.themes["refreshed"] = False
    ms.themes["current_theme"] = "dark" if previous_theme == "light" else "light"

# ✅ Add Dark Mode Toggle at the Top
top_bar = st.columns([8, 1])
with top_bar[1]:
    btn_label = ms.themes["dark"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["light"]["button_face"]
    st.button(btn_label, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
    ms.themes["refreshed"] = True
    st.rerun()

# @st.cache_data(ttl=600)  # Cache API response for 10 minutes
def fetch_data():
    """Fetches user workout data from Flask API."""
    response = requests.get(f"{API_BASE_URL}/fetch_data")
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to fetch data.")
        return None

def show_dashboard():
    """Renders the Gym PR Dashboard."""
    data = fetch_data()
    if not data:
        return  # Stop execution if data fetch fails

    # Selection options
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.subheader("📊 Select Time Frame:")
        time_range = st.radio("", ["All Time", "Last 6 Months", "Last 1 Year"], index=1, horizontal=True)  # ✅ Default to "Last 6 Months"

    with col2:
        st.subheader("⚖️ Unit:")
        use_kg = st.toggle("Use KG", value=False)  # ✅ Default to Pounds (lbs)

    with col3:
        st.subheader("📈 Best Set View:")
        chart_type = st.radio("", ["Max Weight", "1RM Projection"], horizontal=True)

    # Convert weight if needed
    unit_label = "KGs" if use_kg else "LBs"
    conversion_factor = 1 / 2.20462 if use_kg else 1  # ✅ Default: Pounds

    def process_exercise_data(exercise_name, data_key, has_reps=True):
        """Processes exercise data and plots the graph. Handles bodyweight separately."""
        if data_key not in data or not data[data_key]:
            st.warning(f"No data available for {exercise_name}")
            return

        df = pd.DataFrame(data[data_key])

        # Ensure correct data types
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

        # Drop NaN values
        df = df.dropna()

        if has_reps:
            df["reps"] = pd.to_numeric(df["reps"], errors="coerce")
            df["1RM"] = df["weight"] * (1 + df["reps"] / 30)  # Compute 1RM using Epley's formula

            best_weight_sets = df.groupby("timestamp", as_index=False)["weight"].max()
            best_pr_sets = df.groupby("timestamp", as_index=False)["1RM"].max()

            selected_data = best_weight_sets if chart_type == "Max Weight" else best_pr_sets
            y_column = "weight" if chart_type == "Max Weight" else "1RM"
        else:
            selected_data = df.groupby("timestamp", as_index=False)["weight"].max()
            y_column = "weight"

        # Apply conversion
        selected_data[y_column] *= conversion_factor

        # Filter based on time range
        end_date = selected_data["timestamp"].max()
        if time_range == "Last 6 Months":
            start_date = end_date - pd.DateOffset(months=6)
        elif time_range == "Last 1 Year":
            start_date = end_date - pd.DateOffset(years=1)
        else:
            start_date = selected_data["timestamp"].min()

        selected_data = selected_data[selected_data["timestamp"] >= start_date]

        chart_title = f"{exercise_name} - Progression ({unit_label})"

        if selected_data.empty:
            st.warning(f"No data available for {exercise_name} in this time range.")
            return

        # Set Y-axis scale dynamically
        y_min, y_max = selected_data[y_column].min() * 0.9, selected_data[y_column].max() * 1.1

        # Create Altair Chart (Line + Markers for Each Workout)
        chart = (
            alt.Chart(selected_data)
            .mark_line(color="lightblue", strokeWidth=2)
            .encode(x="timestamp:T", y=alt.Y(y_column, title=chart_title, scale=alt.Scale(domain=[y_min, y_max])))
        )

        points = (
            alt.Chart(selected_data)
            .mark_circle(size=70, color="red", opacity=0.8)
            .encode(x="timestamp:T", y=y_column)
        )

        # Display Chart
        st.subheader(chart_title)
        st.altair_chart(chart + points, use_container_width=True)


    # Render charts for all exercises
    process_exercise_data("Bench Press", "bench_press")
    process_exercise_data("Deadlift", "deadlift")
    process_exercise_data("Squat", "squat")
    process_exercise_data("Overhead Press", "overhead_press")
    process_exercise_data("Bodyweight", "bodyweight", has_reps= False)

show_dashboard()
