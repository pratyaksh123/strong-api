from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from utils import read_csv
from extractor import main
from api import get_data

app = Flask(__name__)

@app.route("/fetch_data", methods=["GET"])
def fetch_data():
    """Fetches workout data from extracted CSVs and returns JSON."""
    main()
    data = {
        "bench_press": read_csv("data/Bench Press (Barbell).csv") or [],
        "deadlift": read_csv("data/Deadlift (Barbell).csv") or [],
        "squat": read_csv("data/Squat (Barbell).csv") or [],
        "overhead_press": read_csv("data/Strict Military Press (Barbell).csv") or [],
        "bodyweight": read_csv("data/Bodyweight.csv") or [],
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
