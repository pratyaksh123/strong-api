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
Install Docker Desktop from [here](https://www.docker.com/products/docker-desktop).

---

## 🔧 Setup Instructions

### 1. **Backend API Deployment**

1. Navigate to the backend directory:
   ```bash
    cd backend
   ```

2. Create your **Heroku App** for the backend:
   ```bash
    heroku create gym-api-backend
   ```

3. Set up environment variables in `.env` ( rename `.env.example` to `.env`):
   ```env
   username=your_strong_api_username
   password=your_strong_api_password
   ```

4. Deploy to Heroku:
   ```bash
    heroku stack:set container --app gym-api-backend
    heroku container:push web --app gym-api-backend
    heroku container:release web --app gym-api-backend
   ```

5. Verify the deployment:
   ```bash
    heroku open --app gym-api-backend
   ```
    or go to hero dashboard and open the app. 

6. Monitor the logs for any errors.
   ```bash
    heroku logs --tail --app gym-api-backend
   ```
---

### 2. **Frontend Dashboard Deployment**

1. Navigate to the frontend directory:
   ```bash
    cd ../frontend
   ```

2. Create your **Heroku App** for the frontend:
   ```bash
    heroku create gym-api-frontend
   ```

3. Configure the API Base URL in `.env` , check the backend app url in heroku dashboard:
   ```env
    API_BASE_URL=<> # Backend API URL

    Example: API_BASE_URL=https://gym-api-backend-cd72bdw589b1.herokuapp.com/
   ```

4. Deploy to Heroku:
   ```bash
    heroku stack:set container --app gym-api-frontend
    heroku container:push web --app gym-api-frontend
    heroku container:release web --app gym-api-frontend
   ```
Monitor the logs for any errors.
   ```bash
    heroku logs --tail --app gym-api-frontend
   ```

5. Open the dashboard:
   ```bash
   heroku open --app gym-api-frontend
   ```
    Or go to hero dashboard and open the frontend app.

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
  Re-fetches and updates the workout data from Strong App. It's automatically called by the cron job every midnight, you can call it manually if you want to update the data.

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

## Self Hosting 
I have the app running on my own Raspberry Pi server, you can check it out [here](https://strong.pratyaksh.me).

For those who prefer self-hosting, follow these additional steps:

- Use the provided **Dockerfile_SelfHosted** for setting up the application.
- Check the `nginx` folder for sample configuration files.
- Example Nginx Configuration:

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name strong.pratyaksh.me;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
        allow all;
    }

    return 301 https://$host$request_uri;
}

# HTTPS Server for API and Frontend
server {
    listen 443 ssl;
    server_name strong.pratyaksh.me;

    ssl_certificate /etc/letsencrypt/live/strong.pratyaksh.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/strong.pratyaksh.me/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location /api {
        proxy_pass http://localhost:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Firewall Configuration (UFW):

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow from 192.168.0.0/24 to any port 22 ( basically ssh only from local network )
sudo ufw allow 172.30.0.0/16  # Allow Docker Containers to communicate ( super importnant ) 
sudo ufw enable
```
You might not need firewall at all if you are behind a router or a firewall.

- **Port Forwarding:** Ensure ports 80 and 443 are forwarded in your router settings.
- **SSL:** Use [Certbot](https://certbot.eff.org/) to configure SSL for HTTPS.

**Need help with self-hosting?** Feel free to contact me!


## 📅 License

This project is licensed under the [MIT License](LICENSE).

---

**Happy Lifting! 💪**
