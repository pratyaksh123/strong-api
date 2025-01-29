import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets current dir (backend/app/)
DATA_DIR = os.path.join(BASE_DIR, "data")  # Path to backend/app/data/
JSON_FILE_PATH = os.path.join(DATA_DIR, "data.json")  # Full path to JSON file

# Exercise CSV Paths
BENCH_PRESS_PATH = os.path.join(DATA_DIR, "Bench Press (Barbell).csv")
DEADLIFT_PATH = os.path.join(DATA_DIR, "Deadlift (Barbell).csv")
SQUAT_PATH = os.path.join(DATA_DIR, "Squat (Barbell).csv")
OVERHEAD_PRESS_PATH = os.path.join(DATA_DIR, "Strict Military Press (Barbell).csv")
BODYWEIGHT_PATH = os.path.join(DATA_DIR, "Bodyweight.csv")

# API Base URL
STRONG_API_BASE_URL = "https://back.strong.app"
