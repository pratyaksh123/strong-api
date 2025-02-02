# 🏋️ Strong API & Dashboard

 This project is a dashboard for visualizing workout data from the Strong App and customizing the graphs and charts to track progress! I made it to help me track my progress and see how I'm doing over time and share with others who might find it useful. It's a dockerized **Flask API** and **Streamlit dashboard** for visualizing strength progression and weekly workout volumes. I also have a cron job that automatically fetches and updates the workout data from the Strong App on a daily basis. 

---

## 🚀 Features

- **API Endpoints** to fetch and process workout data from Strong App.
- **Streamlit Dashboard** to visualize PRs, 1RM projections, bodyweight trends, and weekly muscle group volumes.
- **Dark/Light Mode** toggle for personalized themes.
- **Automated Data Refresh** with cron jobs in the backend.

---

## 📂 Project Structure

```
strong-api/
├── backend/
│   ├── app/
│   │   ├── data/  # Contains extracted CSVs and JSON data
│   │   ├── api.py  # Handles data fetching from Strong Api
│   │   ├── extractor.py  # Processes and saves workout logs
│   │   ├── routes.py  # API endpoints
│   │   └── constants.py  # Paths and API constants
│   ├── Dockerfile
│   └── .env  # API credentials and environment variables
├── frontend/
│   ├── app.py  # Streamlit dashboard
│   ├── Dockerfile
│   └── .env  # API Base URL
└── README.md
```

---

## 🚫 Prerequisites

1. **Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli):**
   ```bash
   brew tap heroku/brew && brew install heroku  # macOS
   sudo snap install --classic heroku  # Linux
   ```
2. **Login to Heroku:**
   ```bash
   heroku login
   ```
3. **Ensure Docker is Installed and Running.**

---

## 🔧 Setup Instructions

### 1. **Backend API Deployment**

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create your **Heroku App** for the backend:
   ```bash
   heroku create <your-backend-app-name>
   ```

3. Set up environment variables in `.env` ( rename `.env.example` to `.env`):
   ```env
   username=your_strong_api_username
   password=your_strong_api_password
   ```

4. Deploy to Heroku:
   ```bash
   heroku stack:set container
   git add .
   git commit -m "Deploy backend API"
   git push heroku main
   ```

5. Verify the deployment:
   ```bash
   heroku open
   ```

---

### 2. **Frontend Dashboard Deployment**

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Create your **Heroku App** for the frontend:
   ```bash
   heroku create <your-frontend-app-name>
   ```

3. Configure the API Base URL in `.env` (replace `<your-backend-app-name>`):
   ```env
   API_BASE_URL=https://<your-backend-app-name>.herokuapp.com
   ```

4. Deploy to Heroku:
   ```bash
   heroku stack:set container
   git add .
   git commit -m "Deploy frontend dashboard"
   git push heroku main
   ```

5. Open the dashboard:
   ```bash
   heroku open
   ```

---

## 🌊 API Endpoints

- **Home:**
  ```
  GET /
  ```
  Returns a welcome message.

- **Fetch Data:**
  ```
  GET /fetch_data
  ```
  Extracts workout data from Strong App and returns as JSON.

- **Refresh Data:**
  ```
  GET /refresh_data
  ```
  Re-fetches and updates the workout data from Strong App.

---

## 🌐 Dashboard Features

1. **PR Progression:**
   - Bench Press, Deadlift, Squat, Overhead Press.
   - Visualize Max Weight and 1RM Projections.

2. **Bodyweight Tracking:**
   - Plot changes in bodyweight over time.

3. **Weekly Volume Analysis:**
   - Breakdown of weekly sets per muscle group.
   - Area charts for muscle-specific workload.

4. **Dark/Light Mode:**
   - Toggle between light and dark themes.

---

## 🛡️ Troubleshooting

- **App Crashes or Blank Screen:**
  - Check logs using:
    ```bash
    heroku logs --tail --app <your-app-name>
    ```

- **API Not Connecting to Frontend:**
  - Verify the `API_BASE_URL` in your frontend `.env` matches the deployed backend URL.

---

## 🎉 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Feel free to raise issues and submit pull requests to help improve the project, add your custom charts or fix any bugs.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

---

## 📅 License

This project is licensed under the [MIT License](LICENSE).

---

**Happy Lifting! 💪**
