from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from .utils import read_csv
from .extractor import main
from .api import get_data

app = Flask(__name__)

@app.route("/fetch_data", methods=["GET"])
def fetch_data():
    """Fetches workout data from extracted CSVs and returns JSON."""
    main()

    data = {
        "bench_press": read_csv("data/Bench Press (Barbell).csv") or [],
        "deadlift": read_csv("data/Deadlift (Barbell).csv") or [],
        "squat": read_csv("data/Squat (Barbell).csv") or [],
        "bodyweight": read_csv("data/Bodyweight.csv") or [],
    }

    return jsonify(data)

if __name__ == "__main__":
    # set configuration values
    class Config:
        SCHEDULER_API_ENABLED = True
    scheduler = APScheduler()
    
    # Job to fetch data every 24 hours
    @scheduler.task('cron', id='fetch_data', hour='0')
    def fetch_data():
        get_data()
    
    app.config.from_object(Config())
    # initialize scheduler
    # if you don't wanna use a config, you can set options here:
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run(debug=True)
