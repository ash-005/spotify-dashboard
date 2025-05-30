# My Spotify Stats — Visualized Dashboard

Welcome to **My Spotify Stats**, a Flask + Plotly-powered web dashboard.

This project fetches and analyzes your top 500 Spotify tracks to reveal patterns, genre trends, artist insights, and temporal changes in your listening habits — all presented in a beautiful interactive interface.

## Features

- **Genre Evolution Over Time**: Watch how your music taste changes across the years.
- **Duration Analysis**: Discover average track lengths by genre and release year.
- **Popularity Insights**:
  - Track popularity distribution
  - Artist popularity trends
  - Correlation between artist & track popularity

- **Top Artists**: See which artists dominate your rotation.
- **Genre Distribution**: Multi-label genre analysis using binarization.

## Tech Stack

- **Frontend**: Plotly, HTML/CSS (Jinja templates)
- **Backend**: Flask
- **Data Handling**: Pandas, NumPy
- **Deployment**: Docker + Render
- **APIs**: Spotify Web API via `spotipy`

## Project Structure

```

spotify\_analysis\_code/
│
├── app.py                      # Flask application entry point
├── Dockerfile                  # Docker setup for deployment
├── render.yaml                 # Render deployment config
├── requirements.txt            # Python dependencies
│
├── data/                       # JSON/CSV files with song & genre info
│   ├── top\_500songs.csv
│   ├── top\_500songs\_detailed.json
│   └── ...
│
├── static/                     # CSS styles
│   └── style.css
├── templates/                  # HTML templates (Jinja)
│   └── index.html
│
├── utils/                      # Utility scripts
│   ├── caching.py
│   └── data\_loader.py
│
└── visualizations/            # Plotly graph modules
├── genre\_trends.py
├── duration\_analysis.py
├── popularity\_analysis.py
└── ...

````

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ash-005/spotify-dashboard.git
cd spotify-dashboard
````

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env` File (For Spotify API, if needed)

```env
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8000/callback
```

### 5. Run Locally

```bash
python app.py
```

Navigate to `http://localhost:8080` in your browser.

## Docker Setup

### Build and Run with Docker

```bash
docker build -t spotify-dashboard .
docker run -p 8080:8080 spotify-dashboard
```

## Deployed Version

Check it out live here:
**[my-spotify-statsS.onrender.com](https://my-spotify-statss.onrender.com)**

## To-Do / Future Improvements

* Integrate audio features (tempo, danceability, etc.)
* Add ML-based song/genre recommendations
* Animate visualizations for more vibe
---

