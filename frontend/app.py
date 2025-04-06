import streamlit as st
import requests
import pandas as pd
import altair as alt
from dotenv import load_dotenv

import os
import platform

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "192.168.0.214")

st.set_page_config(page_title="Strong Dashboard", page_icon=":weight_lifter:", layout="centered", initial_sidebar_state="auto", menu_items=None)

# ✅ Clean Title with Less Space
st.markdown("<h1 style='text-align: center;'>🏋️‍♂️ Gym PR Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Track your strength progress over time with clear visualizations!</p>", unsafe_allow_html=True)

def apply_custom_styles():
    st.markdown("""
        <style>
            .stApp {
                background-color: white !important;
                color: black !important;
            }

            .stMultiSelect > div > div > div {
                border: 2px solid #5591f5;
                border-radius: 10px;
                background-color: #f0f8ff;
            }

            .stMultiSelect div[data-baseweb="tag"] {
                background-color: #5591f5 !important;
                color: white !important;
                border-radius: 5px;
            }

            .stMultiSelect svg {
                fill: #5591f5;
            }

            h1, h2, h3, h4, h5, h6, p, label, span {
                color: black !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Apply styles when the dashboard is rendered
apply_custom_styles()

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
    col1, col2 = st.columns([6, 1])

    with col1:
        st.subheader("📊 Select Time Frame:")
        time_range = st.radio("", ["All Time", "Last 6 Months", "Last 1 Year"], index=1, horizontal=True)  # ✅ Default to "Last 6 Months"

    with col2:
        st.subheader("⚖️ Unit:")
        use_kg = st.toggle("Use KG", value=False)  # ✅ Default to Pounds (lbs)

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
        df["weight"] = pd.to_numeric(df["weight"], errors="coerce").round(0)  # ✅ Round weight to whole numbers

        # Drop NaN values
        df = df.dropna()

        if has_reps:
            df["reps"] = pd.to_numeric(df["reps"], errors="coerce")
            df = df[df["reps"] > 0]
            df["1RM"] = (df["weight"] * (1 + df["reps"] / 30)).round(0)

            # Always use the best set by 1RM
            best_1rm_sets = df.loc[df.groupby("timestamp")["1RM"].idxmax()]
            selected_data = best_1rm_sets.copy()

            # Plot actual weight or 1RM estimate based on chart type
            y_column = "1RM"
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
        
        tooltip_list = [alt.Tooltip("timestamp:T", title="📅 Date")]
        if exercise_name != "Bodyweight":
            selected_data["weight"] = (selected_data["weight"] * conversion_factor).round(1)
        else:
            # Only convert if the original data is in pounds
            if not use_kg:
                selected_data["weight"] = (selected_data["weight"] / 2.20462)
        tooltip_list.append(alt.Tooltip("weight:Q", title=f"🏋️ Weight ({unit_label})", format=".1f"))
        if has_reps:
            tooltip_list.append(alt.Tooltip("reps", title="🔄 Reps"))
            tooltip_list.append(alt.Tooltip("1RM", title="📈 1RM Estimate", format=".1f"))

        # ✅ Create Altair Chart (Smooth Line + Stylish Points)
        chart = (
            alt.Chart(selected_data)
            .mark_line(color="#5CC8FF", strokeWidth=3, interpolate="monotone")  # ✅ Smooth line
            .encode(
                x=alt.X("timestamp:T", axis=alt.Axis(labelColor="white", titleColor="white")),
                y=alt.Y(y_column, title=chart_title, scale=alt.Scale(domain=[y_min, y_max])),
            )
        )

        # ✅ Add Points with Orange Color & Slight Glow Effect
        points = (
            alt.Chart(selected_data)
            .mark_circle(size=90, color="#FFA500", opacity=0.85)  # ✅ Brighter and bigger points
            .encode(
                x="timestamp:T",
                y=y_column,
                tooltip=tooltip_list  # ✅ Dynamically apply correct tooltip
            )
        )

        # ✅ Remove default Altair chart border for a clean look
        final_chart = (chart + points).configure_view(strokeWidth=0)

        # Display Chart
        st.subheader(chart_title)
        st.altair_chart(final_chart, use_container_width=True)

        
    def plot_weekly_volume(weekly_volume_key):
        if weekly_volume_key not in data or not data[weekly_volume_key]:
            st.warning("No weekly volume data available.")
            return

        df = pd.DataFrame(data[weekly_volume_key])

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

        # Apply time range filters
        if time_range != "All Time":
            df.set_index("timestamp", inplace=True)  # Temporarily set timestamp as index
        
            if time_range == "Last 6 Months":
                df = df.last('6M')
            elif time_range == "Last 1 Year":
                df = df.last('1Y')
        
            df.reset_index(inplace=True)  # Reset index after filtering
        
        df = df.melt(id_vars=["timestamp"], var_name="Muscle Group", value_name="Sets")

        if df.empty:
            st.warning("No data available for plotting.")
            return

        st.subheader("📊 Weekly Volume by Muscle Group")

        muscle_groups = df["Muscle Group"].unique().tolist()
        selected_muscles = st.multiselect("Select Muscle Groups:", muscle_groups, default=muscle_groups)

        if not selected_muscles:
            st.warning("Please select at least one muscle group.")
            return

        df = df[df["Muscle Group"].isin(selected_muscles)]

        # ✅ Create Altair Chart with Smoothed Curves & Improved Readability
        chart = (
            alt.Chart(df)
            .mark_line(strokeWidth=2, opacity=0.85, interpolate="monotone")  # ✅ Smooth the curves
            .encode(
                x=alt.X("timestamp:T", axis=alt.Axis(labelColor="white", titleColor="white")),
                y=alt.Y("Sets:Q", title="Sets", axis=alt.Axis(labelColor="white", titleColor="white")),
                color=alt.Color("Muscle Group:N", legend=alt.Legend(title="Muscle Group")),
                tooltip=[
                    alt.Tooltip("timestamp:T", title="📅 Date"),
                    alt.Tooltip("Muscle Group:N", title="💪 Muscle Group"),
                    alt.Tooltip("Sets:Q", title="📊 Sets")
                ]
            )
        )

        # ✅ Add Data Points for Better Visualization
        points = (
            alt.Chart(df)
            .mark_circle(size=50, opacity=0.9)
            .encode(
                x="timestamp:T",
                y="Sets:Q",
                color="Muscle Group:N",
                tooltip=[
                    alt.Tooltip("timestamp:T", title="📅 Date"),
                    alt.Tooltip("Muscle Group:N", title="💪 Muscle Group"),
                    alt.Tooltip("Sets:Q", title="📊 Sets")
                ]
            )
        )

        # ✅ Final Chart with Clean Grid & Background
        final_chart = (
            (chart + points)
            .configure_view(strokeWidth=0)  # ✅ Remove default Altair grid border
        )

        st.altair_chart(final_chart, use_container_width=True)



    # Render charts for all exercises
    process_exercise_data("Bench Press", "bench_press")
    process_exercise_data("Deadlift", "deadlift")
    process_exercise_data("Squat", "squat")
    process_exercise_data("Overhead Press", "overhead_press")
    plot_weekly_volume("weekly_volume")
    process_exercise_data("Bodyweight", "bodyweight", has_reps= False)

show_dashboard()
