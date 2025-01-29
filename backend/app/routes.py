from flask import Blueprint, jsonify
from app.utils import read_csv
from app.extractor import main
from app.constants import (
    BENCH_PRESS_PATH,
    DEADLIFT_PATH,
    SQUAT_PATH,
    OVERHEAD_PRESS_PATH,
    BODYWEIGHT_PATH
)

api = Blueprint("api", __name__)

@api.route("/fetch_data", methods=["GET"])
def fetch_data():
    """Fetches workout data from extracted CSVs and returns JSON."""
    main()  # Runs the extractor script

    data = {
        "bench_press": read_csv(BENCH_PRESS_PATH) or [],
        "deadlift": read_csv(DEADLIFT_PATH) or [],
        "squat": read_csv(SQUAT_PATH) or [],
        "overhead_press": read_csv(OVERHEAD_PRESS_PATH) or [],
        "bodyweight": read_csv(BODYWEIGHT_PATH) or [],
    }

    return jsonify(data)
