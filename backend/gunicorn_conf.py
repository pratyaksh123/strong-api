def on_starting(server):
    from flask_apscheduler import APScheduler
    from app.api import get_data  # Import your data fetch function
    from wsgi import app

    class Config:
        SCHEDULER_API_ENABLED = True

    app.config.from_object(Config)

    scheduler = APScheduler()
    scheduler.init_app(app)

    # Add your scheduled job directly in Gunicorn's master process
    @scheduler.task('cron', id='fetch_data_job', hour=0, minute=0)  # Runs daily at midnight
    def fetch_data_job():
        print("🔄 Running scheduled data fetch...")
        result = get_data()
        print(f"✅ Data fetch result: {result}")

    scheduler.start()
    print("✅ Scheduler started in Gunicorn master process with scheduled tasks.")
