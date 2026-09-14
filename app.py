import html
import urllib.parse
import requests
import random
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="MovieHub - MD Edition",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# SESSION STATE 
# =========================================================
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if "history" not in st.session_state: st.session_state.history = []
if "ui" not in st.session_state:
    st.session_state.ui = {
        "home_search_results": [], "m_seed": None, "m_recs": [],
        "tv_seed": None, "tv_recs": [], "cast_person": None, 
        "cast_credits": [], "surprise_movie": None
    }

def add_to_history(item, media_type="movie"):
    item_copy = dict(item); item_copy["media_type"] = media_type 
    history = [x for x in st.session_state.history if str(x.get("id")) != str(item_copy.get("id"))]
    history.insert(0, item_copy)
    st.session_state.history = history[:20] 

# =========================================================
# 🔴 SMOOTH MD LOGO RED & BLACK SPLASH
# =========================================================
if not st.session_state.splash_done:
    st.markdown("""
        <style>
        #md-splash {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: #000000; z-index: 9999999;
            display: flex; justify-content: center; align-items: center;
            animation: smoothFade 0.6s ease-in-out 2.0s forwards;
        }
        .md-logo-text {
            font-family: 'Arial Black', Impact, sans-serif;
            font-size: clamp(80px, 18vw, 200px);
            font-weight: 900;
            color: #E50914;
            text-transform: uppercase;
            letter-spacing: 4px;
            text-align: center;
            animation: mdZoomSmooth 2.0s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        @keyframes mdZoomSmooth {
            0% { opacity: 0; transform: scale(0.6); filter: blur(10px); }
            30% { opacity: 1; transform: scale(1); filter: blur(0px); text-shadow: 0 0 40px rgba(229, 9, 20, 0.8); }
            85% { opacity: 1; transform: scale(1.1); text-shadow: 0 0 80px rgba(229, 9, 20, 1); }
            100% { opacity: 0; transform: scale(2.5); filter: blur(15px); visibility: hidden; }
        }
        @keyframes smoothFade {
            to { opacity: 0; visibility: hidden; display: none; }
        }
        </style>
        <div id="md-splash">
            <div class="md-logo-text">MD</div>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.splash_done = True

# =========================================================
# TMDB CONFIG
# =========================================================
TMDB_TOKEN = str(st.secrets.get("TMDB_API_KEY", "")).strip()
TMDB_BASE = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
PROVIDER_LOGO_BASE = "https://image.tmdb.org/t/p/w92"

# =========================================================
# PREMIUM CUSTOM CSS FOR MAIN UI & CLEAN ARRANGEMENT
# =========================================================
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: #0b0b0d !important;
        background-image: radial-gradient(circle at top left, rgba(229, 9, 20, 0.08) 0%, transparent 40%),
                          radial-gradient(circle at bottom right, rgba(124, 58, 237, 0.05) 0%, transparent 40%) !important;
        color: #ffffff;
    }
    [data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { display: none !important; }
    .block-container { max-width: 1400px; padding: 1rem 2rem 5rem 2rem; }

    .hero-banner {
        position: relative; width: 100%; height: 300px; border-radius: 20px; overflow: hidden; margin-bottom: 25px;
        background: url('https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?q=80&w=2070&auto=format&fit=crop') center/cover;
        border: 1px solid rgba(255,255,255,0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.8);
    }
    .hero-gradient {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(90deg, rgba(11,11,13,1) 0%, rgba(11,11,13,0.85) 50%, transparent 100%);
        display: flex; flex-direction: column; justify-content: center; padding: 40px 60px;
    }
    .hero-tag { display: inline-block; padding: 5px 12px; background: #e50914; color: #fff; font-size: 11px; font-weight: 800; letter-spacing: 2px; border-radius: 4px; text-transform: uppercase; margin-bottom: 12px; width: fit-content; }
    .hero-title { font-size: 45px; font-weight: 900; line-height: 1.1; margin: 0 0 10px 0; color: #fff; letter-spacing: -2px; }
    .hero-desc { font-size: 14px; color: #a1a1aa; max-width: 500px; line-height: 1.5; margin-bottom: 0; }

    .row-title { font-size: 22px; font-weight: 700; color: #e4e4e7; margin: 25px 0 12px 0; padding-left: 10px; border-left: 4px solid #e50914; line-height: 1; }
    button[data-baseweb="tab"] { font-weight: 600 !important; font-size: 16px !important; color: #71717a !important; background: transparent !important; border: none !important;}
    button[data-baseweb="tab"][aria-selected="true"] { color: #fff !important; }
    div[data-baseweb="tab-highlight"] { background-color: #e50914 !important; height: 3px !important; }

    .movie-card-box {
        background: #141418; border-radius: 12px; overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08); transition: 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-bottom: 15px; position: relative;
    }
    .movie-card-box:hover { transform: translateY(-4px); border-color: rgba(229, 9, 20, 0.5); }
    
    .poster-wrap { position: relative; width: 100%; aspect-ratio: 2/3; background: #18181b; overflow: hidden; }
    .poster-wrap img { width: 100%; height: 100% !important; object-fit: cover; }
    .rating-badge { position: absolute; top: 8px; right: 8px; background: rgba(0,0,0,0.85); padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); z-index: 5; }
    
    .card-info { padding: 10px; position: relative; z-index: 5; }
    .c-title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .c-meta { font-size: 11px; color: #94a3b8; display: flex; justify-content: space-between; margin-bottom: 6px; }
    
    .prov-tray { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; margin-top: 8px; position: relative; z-index: 10; min-height: 28px; }
    .prov-tray a { display: inline-flex; transition: transform 0.2s; cursor: pointer; }
    .prov-tray a:hover { transform: scale(1.15); }
    .prov-tray img { width: 24px; height: 24px; border-radius: 4px; object-fit: cover; border: 1px solid rgba(255,255,255,0.2); }
    
    .play-overlay { position: absolute; top: 0; left: 0; width: 100% !important; height: 100% !important; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.4); opacity: 0; transition: 0.3s ease; text-decoration: none; z-index: 2; }
    .poster-wrap:hover .play-overlay { opacity: 1; }
    .play-btn { width: 40px; height: 40px; background: rgba(229,9,20,0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 15px; box-shadow: 0 0 15px rgba(229,9,20,0.6); }

    .booking-btn {
        display: block; text-align: center; background: #e50914; color: white !important;
        padding: 6px; border-radius: 6px; text-decoration: none; font-weight: 800;
        font-size: 11px; margin-bottom: 8px; transition: 0.2s;
    }
    .booking-btn:hover { background: #ff1a25; color: white !important; }

    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-radius: 8px !important; background: #18181b !important; border-color: #27272a !important; color: white !important; font-size: 14px !important;}
    .stButton > button, div[data-testid="stFormSubmitButton"] > button { border-radius: 8px !important; font-weight: 700 !important; background: #e50914 !important; color: #fff !important; border: none !important; padding: 6px 16px !important; transition: .2s !important; }
    .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover { background: #f11c27 !important; transform: scale(1.02); }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# API HELPER & LOGIC
# =========================================================
@st.cache_data(ttl=3600)
def tmdb_get(endpoint, params=None):
    if not TMDB_TOKEN: return {}
    request_params = dict(params or {})
    headers = {"accept": "application/json"}
    if TMDB_TOKEN.startswith("eyJ"): headers["Authorization"] = f"Bearer {TMDB_TOKEN}"
    else: request_params["api_key"] = TMDB_TOKEN
    try:
        response = requests.get(TMDB_BASE + endpoint, headers=headers, params=request_params, timeout=15)
        if response.status_code == 200: return response.json()
    except: pass
    return {}

@st.cache_data(ttl=3600)
def get_now_playing_movies():
    res = tmdb_get("/movie/now_playing", {"language": "en-US", "page": 1, "region": "IN"})
    return res.get("results", [])[:10] if isinstance(res, dict) else []

@st.cache_data(ttl=3600)
def get_upcoming_movies():
    res = tmdb_get("/movie/upcoming", {"language": "en-US", "page": 1, "region": "IN"})
    return res.get("results", [])[:12] if isinstance(res, dict) else []

@st.cache_data(ttl=3600)
def get_surprise_movie():
    data = tmdb_get("/discover/movie", {"language": "en-US", "sort_by": "popularity.desc", "with_original_language": "hi", "vote_count.gte": 50, "vote_average.gte": 6.8, "page": random.randint(1, 3)})
    res = data.get("results", []) if isinstance(data, dict) else []
    return random.choice(res) if res else None

def search_movie(title):
    results = tmdb_get("/search/movie", {"query": title, "include_adult": False, "language": "en-US", "page": 1}).get("results", [])
    if not results: return None
    exact = [i for i in results if i.get("title", "").lower() == title.lower()]
    return exact[0] if exact else results[0]

def search_tv(title, language_code=None):
    results = tmdb_get("/search/tv", {"query": title, "include_adult": False, "language": "en-US", "page": 1}).get("results", [])
    if not results: return None
    if language_code: 
        results = [i for i in results if i.get("original_language") == language_code] or results
    exact = [i for i in results if i.get("name", "").lower() == title.lower()]
    return exact[0] if exact else results[0]

def search_person(name): 
    res = tmdb_get("/search/person", {"query": name, "include_adult": False, "language": "en-US", "page": 1}).get("results", [])
    return res[0] if res else None

def get_person_credits(person_id):
    data = tmdb_get(f"/person/{person_id}/combined_credits", {"language": "en-US"})
    if not isinstance(data, dict): return []
    cast = data.get("cast", [])
    crew = [c for c in data.get("crew", []) if c.get("job") == "Director"]
    combined = cast + crew
    combined.sort(key=lambda x: x.get("vote_count", 0), reverse=True)
    seen = set(); unique = []
    for item in combined:
        if item.get("id") not in seen and item.get("poster_path"):
            seen.add(item.get("id"))
            unique.append(item)
    return unique[:10]

def get_smart_recommendations(media_type, seed_id, language_code=None, count=5):
    seen = {seed_id}; final_results = []
    details = tmdb_get(f"/{media_type}/{seed_id}", {"append_to_response": "keywords"})
    if not isinstance(details, dict): return []
    genres = [str(g.get("id")) for g in details.get("genres", []) if g.get("id")]
    kw_key = "results" if media_type == "tv" else "keywords"
    kw_obj = details.get("keywords", {})
    keywords_list = kw_obj.get(kw_key, []) if isinstance(kw_obj, dict) else []
    keywords = [str(k.get("id")) for k in keywords_list if k.get("id")]

    if genres:
        params = {"language": "en-US", "sort_by": "vote_average.desc", "vote_count.gte": 20, "with_genres": genres[0], "page": 1}
        if keywords: params["with_keywords"] = "|".join(keywords[:4])
        if language_code: params["with_original_language"] = language_code
        disc = tmdb_get(f"/discover/{media_type}", params)
        if isinstance(disc, dict):
            for item in disc.get("results", []):
                if item.get("id") not in seen:
                    final_results.append(item); seen.add(item.get("id"))
                    if len(final_results) >= count: return final_results[:count]

    if len(final_results) < count:
        sim = tmdb_get(f"/{media_type}/{seed_id}/similar", {"language": "en-US", "page": 1})
        if isinstance(sim, dict):
            for item in sim.get("results", []):
                if language_code and item.get("original_language") != language_code: continue
                if item.get("id") not in seen:
                    final_results.append(item); seen.add(item.get("id"))
                    if len(final_results) >= count: return final_results[:count]
                
    return final_results[:count]

def multi_search(query):
    query = str(query or "").strip()
    if not query: return []
    m_data = tmdb_get("/search/movie", {"query": query, "include_adult": False, "language": "en-US", "page": 1}).get("results", [])[:8]
    t_data = tmdb_get("/search/tv", {"query": query, "include_adult": False, "language": "en-US", "page": 1}).get("results", [])[:8]
    for i in m_data: i["media_type"] = "movie"
    for i in t_data: i["media_type"] = "tv"
    unique = []; seen = set()
    for item in m_data + t_data:
        key = (item.get("media_type"), item.get("id"))
        if key not in seen: seen.add(key); unique.append(item)
    unique.sort(key=lambda x: float(x.get("popularity") or 0), reverse=True)
    return unique[:10]

def get_watch_providers(media_type, media_id): 
    res = tmdb_get(f"/{media_type}/{media_id}/watch/providers")
    if not isinstance(res, dict): return {}
    provs = res.get("results", {})
    return provs.get("IN", {}) if isinstance(provs, dict) else {}

def encoded(text): return urllib.parse.quote_plus(str(text))

def provider_search_url(provider_name, title, media_type):
    name = str(provider_name).lower()
    q = encoded(title)
    if "netflix" in name: return f"https://www.netflix.com/search?q={q}"
    if "prime" in name or "amazon" in name: return f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={q}"
    if "hotstar" in name or "disney" in name: return f"https://www.hotstar.com/in/explore?searchQuery={q}"
    if "jiocinema" in name: return f"https://www.jiocinema.com/search?q={q}"
    if "zee5" in name: return f"https://www.zee5.com/search?q={q}"
    if "sonyliv" in name: return f"https://www.sonyliv.com/search/{q}"
    if "apple" in name: return f"https://tv.apple.com/in/search?term={q}"
    return f"https://www.google.com/search?q={encoded(f'{title} watch on {provider_name}')}"

def bookmyshow_main_link(): return "https://in.bookmyshow.com/"
def youtube_link(title, content_type): return f"https://www.youtube.com/results?search_query={encoded(f'{title} official trailer {content_type}')}"
def safe_text(value): return html.escape(str(value if value is not None else ""))

# =========================================================
# CLEAN SAFE HTML CARD RENDERER (WITH SMART OTT FALLBACK)
# =========================================================
def show_movie_card(movie, show_booking=False):
    title = movie.get("title") or movie.get("name") or "Unknown"
    media_type = movie.get("media_type") or ("movie" if "title" in movie else "tv")
    poster = movie.get("poster_path")
    poster_url = IMAGE_BASE + poster if poster else "https://via.placeholder.com/500x750/18181b/ffffff?text=No+Image"
    rating = float(movie.get("vote_average") or 0)
    year = str(movie.get("release_date") or movie.get("first_air_date") or "N/A")[:4]
    
    overview_raw = str(movie.get("overview") or "Story details not available.")
    overview = html.escape(overview_raw)

    providers = get_watch_providers(media_type, str(movie.get("id")))
    seen_logos = set()
    logos_list_html = ""
    
    if isinstance(providers, dict):
        for category in ["flatrate", "free", "rent", "buy"]:
            cat_provs = providers.get(category, [])
            if isinstance(cat_provs, list):
                for p in cat_provs:
                    path = p.get("logo_path")
                    p_name = p.get("provider_name", "OTT")
                    if path and path not in seen_logos:
                        seen_logos.add(path)
                        p_url = provider_search_url(p_name, title, media_type)
                        logos_list_html += f'<a href="{p_url}" target="_blank" title="Watch on {html.escape(str(p_name))}"><img src="{PROVIDER_LOGO_BASE}{path}"></a>'

    yt_link = youtube_link(title, media_type)
    safe_title = safe_text(title)

    # Smart Fallback if No OTT Provider Found
    if not logos_list_html:
        logos_list_html = f'<div style="width: 100%;"><div style="font-size: 11px; color: #a1a1aa; line-height: 1.4; margin-bottom: 8px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis;">{overview}</div><a href="{yt_link}" target="_blank" style="display:block; text-align:center; background:#27272a; border: 1px solid #3f3f46; color:#fff; padding:5px; border-radius:4px; font-size:11px; font-weight:700; text-decoration:none; transition: 0.2s;">▶ Watch on YouTube</a></div>'

    booking_btn_html = ""
    if show_booking:
        bms_url = bookmyshow_main_link()
        booking_btn_html = f'<a href="{bms_url}" target="_blank" class="booking-btn">🎟️ Book Tickets</a>'

    # NO indentation here to strictly prevent Markdown block errors
    card_html = f"""<div class="movie-card-box">
<div class="poster-wrap">
<img src="{poster_url}" alt="Poster">
<div class="rating-badge">⭐ {rating:.1f}</div>
<a href="{yt_link}" target="_blank" class="play-overlay"><div class="play-btn">▶</div></a>
</div>
<div class="card-info">
<div class="c-title" title="{safe_title}">{safe_title}</div>
<div class="c-meta"><span>{year}</span><span style="text-transform: uppercase;">{media_type}</span></div>
{booking_btn_html}
<div class="prov-tray">{logos_list_html}</div>
</div>
</div>"""

    st.markdown(card_html, unsafe_allow_html=True)

# =========================================================
# UI MAIN LAYOUT
# =========================================================

st.markdown("""
    <div class="hero-banner">
        <div class="hero-gradient">
            <div class="hero-tag">MD MOVIES AI</div>
            <div class="hero-title">MovieHub</div>
            <div class="hero-desc">Powered by exact semantic plot matching. Discover your favorite Hindi & Global blockbusters effortlessly.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================================================
# PERSISTENT PAGE NAVIGATION
# =========================================================
pages = [
    "🔥 Home",
    "🎟️ Upcoming",
    "🎬 Movie Match",
    "📺 Series Match",
    "🎭 Cast & crew",
    "🕒 History",
]

if "active_page" not in st.session_state:
    st.session_state.active_page = "🔥 Home"

selected_page = st.segmented_control(
    "Navigation",
    pages,
    default=st.session_state.active_page,
    label_visibility="collapsed",
)

if selected_page:
    st.session_state.active_page = selected_page

language_map = {
    "All Languages": None, 
    "Hindi": "hi", 
    "English": "en", 
    "Tamil": "ta", 
    "Telugu": "te", 
    "Malayalam": "ml", 
    "Kannada": "kn", 
    "Marathi": "mr"
}

if st.session_state.active_page == "🔥 Home":
    st.markdown('<div class="row-title">🔍 Global Search</div>', unsafe_allow_html=True)

    with st.form(key="home_search_form"):
        col1, col2 = st.columns([4, 1])
        with col1:
            h_query = st.text_input("Enter Movie or Series Name...", label_visibility="collapsed", placeholder="Search any movie or web series globally...")
        with col2:
            h_search_btn = st.form_submit_button("Search", use_container_width=True)
            
    if h_query or h_search_btn:
        if h_query:
            with st.spinner("Searching..."):
                res = multi_search(h_query)
                st.session_state.ui["home_search_results"] = res
                if res: add_to_history(res[0], res[0].get("media_type", "movie"))

    if st.session_state.ui.get("home_search_results"):
        st.markdown("<br>", unsafe_allow_html=True)
        for i in range(0, len(st.session_state.ui["home_search_results"]), 5):
            cols = st.columns(5)
            for col, r in zip(cols, st.session_state.ui["home_search_results"][i:i+5]):
                with col: show_movie_card(r, show_booking=False)
        st.markdown("<hr style='border-color: #27272a; margin: 20px 0;'>", unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 1])
    with col_a: st.markdown('<div class="row-title">🍿 Now Playing in Theaters & OTT</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<br>', unsafe_allow_html=True)
        if st.button("🎲 Surprise Pick", use_container_width=True): st.session_state.ui["surprise_movie"] = get_surprise_movie()

    if st.session_state.ui.get("surprise_movie"):
        st.success("✨ Random Highly-Rated Pick:")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: show_movie_card(st.session_state.ui["surprise_movie"], show_booking=True)
        st.markdown("<hr style='border-color: #27272a'>", unsafe_allow_html=True)

    now_playing = get_now_playing_movies()
    if now_playing:
        for i in range(0, len(now_playing), 5):
            cols = st.columns(5)
            for col, rec in zip(cols, now_playing[i:i+5]):
                with col: show_movie_card(rec, show_booking=True)

elif st.session_state.active_page == "🎟️ Upcoming":
    st.markdown('<div class="row-title">🎟️ Upcoming Movies (Theatrical & OTT)</div>', unsafe_allow_html=True)

    with st.form(key="upcoming_form"):
        col_up_1, col_up_2 = st.columns([3, 1])
        with col_up_1:
            up_query = st.text_input("Search upcoming movie...", placeholder="Type movie name to filter...", label_visibility="collapsed")
        with col_up_2:
            up_search_btn = st.form_submit_button("Filter", use_container_width=True)
            
    upcoming_list = get_upcoming_movies()
    if up_query:
        upcoming_list = [m for m in upcoming_list if up_query.lower() in (m.get("title") or m.get("name") or "").lower()]

    if upcoming_list:
        for i in range(0, len(upcoming_list), 5):
            cols = st.columns(5)
            for col, movie in zip(cols, upcoming_list[i:i+5]):
                with col: show_movie_card(movie, show_booking=True)
    else:
        st.info("Aisi koi upcoming movie nahi mili.")

elif st.session_state.active_page == "🎬 Movie Match":
    st.markdown('<div class="row-title" style="margin-bottom: 20px;">Exact Story Match</div>', unsafe_allow_html=True)

    with st.form(key="movie_match_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1: 
            m_query = st.text_input("Movie Name", label_visibility="collapsed", placeholder="Enter Movie Name")
        with col2: 
            m_lang = st.selectbox("Language", list(language_map.keys()), label_visibility="collapsed")
        with col3:
            match_btn = st.form_submit_button("Match Story", use_container_width=True)

    if m_query or match_btn:
        if m_query:
            with st.spinner("Analyzing plot keywords..."):
                movie = search_movie(m_query)
                st.session_state.ui["m_seed"] = movie
                if movie:
                    st.session_state.ui["m_recs"] = get_smart_recommendations("movie", movie["id"], language_map[m_lang])
                    add_to_history(movie, "movie")
                else:
                    st.session_state.ui["m_recs"] = []

    if st.session_state.ui.get("m_seed"):
        st.markdown(f"### Matches for '{st.session_state.ui['m_seed']['title']}'")
        recs = st.session_state.ui["m_recs"]
        if recs:
            for i in range(0, len(recs), 5):
                cols = st.columns(5)
                for col, rec in zip(cols, recs[i:i+5]):
                    with col: show_movie_card(rec, show_booking=False)
        else: st.info("No exact keyword matches found.")

elif st.session_state.active_page == "📺 Series Match":
    st.markdown('<div class="row-title" style="margin-bottom: 20px;">Web Series Match</div>', unsafe_allow_html=True)

    with st.form(key="series_match_form"):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1: 
            tv_query = st.text_input("Series Name", label_visibility="collapsed", placeholder="Enter Series Name")
        with col2: 
            tv_lang = st.selectbox("Language", list(language_map.keys()), label_visibility="collapsed")
        with col3:
            match_tv_btn = st.form_submit_button("Match Concept", use_container_width=True)

    if tv_query or match_tv_btn:
        if tv_query:
            with st.spinner("Analyzing plot keywords..."):
                series = search_tv(tv_query, language_map[tv_lang])
                st.session_state.ui["tv_seed"] = series
                if series:
                    st.session_state.ui["tv_recs"] = get_smart_recommendations("tv", series["id"], language_map[tv_lang])
                    add_to_history(series, "tv")
                else:
                    st.session_state.ui["tv_recs"] = []

    if st.session_state.ui.get("tv_seed"):
        st.markdown(f"### Matches for '{st.session_state.ui['tv_seed']['name']}'")
        recs = st.session_state.ui["tv_recs"]
        if recs:
            for i in range(0, len(recs), 5):
                cols = st.columns(5)
                for col, rec in zip(cols, recs[i:i+5]):
                    with col: show_movie_card(rec, show_booking=False)
        else: st.info("No exact matches found.")

elif st.session_state.active_page == "🎭 Cast & Crew":
    st.markdown('<div class="row-title" style="margin-bottom: 20px;">Actor/Director Portfolio</div>', unsafe_allow_html=True)

    with st.form(key="cast_form"):
        col1, col2 = st.columns([4, 1])
        with col1: 
            person_query = st.text_input("Search Name", label_visibility="collapsed", placeholder="Search Actor or Director...")
        with col2:
            explore_btn = st.form_submit_button("Explore Work", use_container_width=True)

    if person_query or explore_btn:
        if person_query:
            with st.spinner("Loading portfolio..."):
                person = search_person(person_query)
                st.session_state.ui["cast_person"] = person
                if person: st.session_state.ui["cast_credits"] = get_person_credits(person["id"])
                else: st.session_state.ui["cast_credits"] = []

    if st.session_state.ui.get("cast_person"):
        st.markdown(f"### Best of {st.session_state.ui['cast_person']['name']}")
        credits = st.session_state.ui["cast_credits"]
        if credits:
            for i in range(0, len(credits), 5):
                cols = st.columns(5)
                for col, credit in zip(cols, credits[i:i+5]):
                    with col: show_movie_card(credit, show_booking=False)
        else: st.info("No major work found.")

elif st.session_state.active_page == "🕒 History":
    st.markdown('<div class="row-title">Recently Viewed</div>', unsafe_allow_html=True)
    if not st.session_state.history: st.info("History is empty.")
    else:
        history_items = st.session_state.history
        for i in range(0, len(history_items), 5):
            cols = st.columns(5)
            for col, item in zip(cols, history_items[i:i+5]):
                with col: show_movie_card(item, show_booking=False)
