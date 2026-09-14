# 🎬 WatchHub India

**WatchHub India** is a movie and web-series discovery platform built with Python and Streamlit. It helps users discover movies and web series, explore cast & crew, search content, view recommendations, and find where a title is available to watch.

🌐 **Live Demo:** https://movieapp-india.streamlit.app/

> 🎬 A smart movie & web-series discovery platform built with Python, Streamlit and TMDB API.

[🚀 Live Demo](https://movieapp-india.streamlit.app/) • [📂 GitHub Repository](https://github.com/deepaknagar-dn/WatchHub-India)

## 🚀 Key Features

- 🎬 Movie Discovery
- 📺 Web Series Discovery
- 🔍 Global Movie & Series Search
- 🤖 Content-Based Recommendation System
- 🎭 Cast & Crew Search
- ⭐ TMDB Ratings
- 🎟️ Upcoming Movies
- 📺 OTT Availability in India
- ▶️ Official Trailer Search
- 🕒 Recently Viewed History
- 🌐 Multiple Language Support
- 🎲 Surprise Movie Pick
- 📱 Responsive Streamlit Interface

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Requests
- Scikit-learn
- TMDB API
- GitHub
- Git LFS
- HTML/CSS

## 🤖 Recommendation System

MovieHub India uses a content-based recommendation approach to find similar movies and web series.

The system uses:
- Movie/Series genres
- Keywords
- Content information
- Language filtering
- TMDB similar-content results

The recommendation system helps users discover content related to the movie or series they select.

## 📺 Where to Watch

The application displays available streaming providers and provides links for users to find the selected movie or series on supported platforms.

## 🚀 Run Locally

Clone the repository:

bash
git clone https://github.com/deepaknagar-dn/WatchHub-India.git
cd WatchHub-India

Install dependencies:
pip install -r requirements.txt

Run the application:
streamlit run app.py

## 🔌 TMDB API

MovieHub India uses the TMDB API to fetch live entertainment data such as:

- Movie information
- Web series information
- Ratings
- Posters
- Cast & Crew
- Upcoming movies
- Now playing movies
- OTT/Watch provider information

🔐 API Configuration

Create:  .streamlit/secrets.toml

Add your TMDB API key:
TMDB_API_KEY = "YOUR_TMDB_API_KEY"


## ☁️ Deployment

The application is deployed using Streamlit Community Cloud.

### Live Demo
[MovieHub India](https://watchapp-india.streamlit.app/)

📂 Project Structure
WatchHub-India/
│
├── app.py
├── requirements.txt
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── .gitignore
└── .gitattributes


👨‍💻 Author

Deepak Nagar

B.Tech — Artificial Intelligence & Machine Learning / Data Science

## 📸 Screenshots

### 🏠 Home
<img src="./Home.png.png" width="800">

### 🎬 Movies
<img src="./Movie.png.png" width="800">

### 📺 Web Series
<img src="./webseries.png.png" width="800">

### 🎭 Cast & Crew
<img src="./Cast&crew.png.png" width="800">

### 📺 OTT / Where to Watch
<img src="./OTT,global.png.png" width="800">
