import html
import urllib.parse
import requests
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# TMDB CONFIG
# =========================================================

TMDB_TOKEN = str(st.secrets.get("TMDB_API_KEY", "")).strip()
TMDB_BASE = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
PROVIDER_LOGO_BASE = "https://image.tmdb.org/t/p/w92"

# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 10% 0%, rgba(91, 33, 182, .20), transparent 28%),
            radial-gradient(circle at 90% 8%, rgba(190, 24, 93, .16), transparent 25%),
            #07070b;
    }

    [data-testid="stHeader"] { background: transparent; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    .block-container { max-width: 1450px; padding-top: 1.5rem; padding-bottom: 4rem; }
    .brand-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
    .brand { font-size: 24px; font-weight: 900; letter-spacing: -.8px; color: #fff; }
    .brand span { color: #a78bfa; }

    .top-pill { padding: 7px 13px; border-radius: 999px; background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.09); color: #aaa8b7; font-size: 12px; }

    .hero-wrap {
        position: relative; overflow: hidden; min-height: 455px; border-radius: 30px; margin-bottom: 28px;
        border: 1px solid rgba(255,255,255,.09);
        background: radial-gradient(circle at 82% 25%, rgba(124,58,237,.42), transparent 32%),
                    radial-gradient(circle at 92% 80%, rgba(236,72,153,.24), transparent 30%),
                    linear-gradient(115deg, #09090d 0%, #0d0c15 55%, #14101c 100%);
        box-shadow: 0 35px 90px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.04);
    }
    .hero-glow { position: absolute; width: 430px; height: 430px; right: -100px; top: -110px; border-radius: 50%; background: radial-gradient(circle, rgba(139,92,246,.24), transparent 68%); filter: blur(8px); }
    .hero-content { position: relative; z-index: 2; padding: 62px 64px; max-width: 820px; }
    .eyebrow { color: #c4b5fd; font-size: 12px; font-weight: 900; letter-spacing: 3px; margin-bottom: 17px; }
    .hero-title { font-size: clamp(48px, 7vw, 86px); line-height: .92; letter-spacing: -4px; font-weight: 950; margin: 0 0 22px 0; color: #fff; }
    .hero-title .accent { background: linear-gradient(90deg, #c4b5fd, #f9a8d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hero-copy { max-width: 680px; color: #b0aebb; font-size: 16px; line-height: 1.75; margin-bottom: 24px; }
    .hero-tags span { display: inline-block; margin: 0 7px 7px 0; padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.09); color: #dedbe6; font-size: 12px; }

    .section-head { display: flex; align-items: end; justify-content: space-between; gap: 15px; margin: 32px 0 17px 0; }
    .section-title { font-size: 28px; font-weight: 900; letter-spacing: -.8px; color: #fff; margin: 0; }
    .section-subtitle { color: #858292; font-size: 13px; margin-top: 5px; }

    .movie-card { border-radius: 22px; padding: 12px; background: linear-gradient(145deg, rgba(255,255,255,.075), rgba(255,255,255,.025)); border: 1px solid rgba(255,255,255,.08); box-shadow: 0 18px 45px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.035); margin-bottom: 12px; }
    .poster-frame { overflow: hidden; border-radius: 16px; background: #15151d; }
    .card-title { color: #fff; font-size: 18px; line-height: 1.25; font-weight: 850; margin: 12px 2px 7px 2px; }
    .card-meta { color: #9c99a8; font-size: 12px; margin: 0 2px 9px 2px; }
    .rating { color: #facc15; font-weight: 800; }
    .type { color: #c4b5fd; background: rgba(124,58,237,.11); border: 1px solid rgba(124,58,237,.20); border-radius: 999px; padding: 4px 8px; font-weight: 800; }
    .overview { color: #9693a1; font-size: 12px; line-height: 1.65; min-height: 98px; margin: 0 2px 7px 2px; }

    .watch-box { border-radius: 18px; padding: 14px; margin-top: 12px; background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.018)); border: 1px solid rgba(255,255,255,.075); box-shadow: inset 0 1px 0 rgba(255,255,255,.025); }
    .watch-heading { color: #f1eef7; font-size: 12px; font-weight: 900; letter-spacing: 1.7px; text-transform: uppercase; margin: 0 0 11px 2px; }

    /* UI Grid */
    .provider-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 8px; margin: 0 0 11px 0; }
    
    .provider-tile { display: flex; align-items: center; gap: 10px; padding: 8px; border-radius: 12px; background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.075); text-decoration: none !important; transition: .18s ease; }
    .provider-tile:hover { background: rgba(124,58,237,.14); border-color: rgba(167,139,250,.38); transform: translateY(-2px); }
    .provider-logo { width: 38px; height: 38px; flex: 0 0 38px; border-radius: 9px; overflow: hidden; display: flex; align-items: center; justify-content: center; background: #fff; }
    .provider-logo img { width: 38px; height: 38px; object-fit: cover; }
    .provider-info { min-width: 0; flex: 1; }
    .provider-name { color: #f4f1f8; font-size: 11px; font-weight: 850; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    
    /* Dynamic pill colors */
    .provider-type { display: inline-block; color: #c4b5fd; font-size: 8px; font-weight: 900; letter-spacing: 1px; margin-top: 3px; padding: 2px 5px; border-radius: 5px; background: rgba(124,58,237,.12); border: 1px solid rgba(124,58,237,.18); }
    .type-free { color: #86efac; background: rgba(34,197,94,.12); border: 1px solid rgba(34,197,94,.20); }
    .type-rent { color: #fca5a5; background: rgba(239,68,68,.12); border: 1px solid rgba(239,68,68,.20); }

    .provider-arrow { color: #c4b5fd; font-size: 15px; flex: 0 0 auto; }

    .watch-action { display: flex; align-items: center; justify-content: center; width: 100%; box-sizing: border-box; border-radius: 12px; padding: 10px 12px; margin-top: 8px; text-decoration: none !important; font-size: 10px; font-weight: 850; color: #f5f3f7 !important; background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.08); }
    .watch-action:hover { background: rgba(124,58,237,.15); border-color: rgba(167,139,250,.35); }
    .empty-watch { color: #858292; font-size: 11px; line-height: 1.5; padding: 9px; border-radius: 11px; background: rgba(255,255,255,.025); }

    .search-hero { border: 1px solid rgba(255,255,255,.08); background: linear-gradient(135deg, rgba(124,58,237,.11), rgba(236,72,153,.06)); border-radius: 22px; padding: 24px; margin-bottom: 18px; }
    .result-row { border: 1px solid rgba(255,255,255,.07); border-radius: 18px; padding: 13px; background: rgba(255,255,255,.025); margin-bottom: 14px; }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { border-radius: 14px !important; background: rgba(255,255,255,.035) !important; border-color: rgba(255,255,255,.08) !important; }
    .stButton > button { border-radius: 12px !important; font-weight: 800 !important; background: linear-gradient(135deg, #7c3aed, #db2777) !important; color: #fff !important; border: 1px solid rgba(255,255,255,.08) !important; }
    button[data-baseweb="tab"] { font-weight: 800 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# API HELPER
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
    except Exception:
        pass
    return {}

# =========================================================
# SMART RECOMMENDATION LOGIC
# =========================================================

def search_movie(title):
    data = tmdb_get("/search/movie", {"query": title, "include_adult": False, "language": "en-US", "page": 1})
    results = data.get("results", [])
    if not results: return None
    exact = [i for i in results if i.get("title", "").lower() == title.lower()]
    return exact[0] if exact else results[0]

def search_tv(title, language_code=None):
    data = tmdb_get("/search/tv", {"query": title, "include_adult": False, "language": "en-US", "page": 1})
    results = data.get("results", [])
    if language_code:
        results = [i for i in results if i.get("original_language") == language_code] or results
    if not results: return None
    exact = [i for i in results if i.get("name", "").lower() == title.lower()]
    return exact[0] if exact else results[0]

def search_person(name):
    data = tmdb_get("/search/person", {"query": name, "include_adult": False, "language": "en-US", "page": 1})
    results = data.get("results", [])
    return results[0] if results else None

def get_person_credits(person_id):
    data = tmdb_get(f"/person/{person_id}/combined_credits", {"language": "en-US"})
    cast = data.get("cast", [])
    crew = [c for c in data.get("crew", []) if c.get("job") == "Director"]
    combined = cast + crew
    combined.sort(key=lambda x: x.get("vote_count", 0), reverse=True)
    seen = set()
    unique_credits = []
    for item in combined:
        if item["id"] not in seen and item.get("poster_path"):
            seen.add(item["id"])
            unique_credits.append(item)
    return unique_credits[:10]

def get_smart_recommendations(media_type, seed_id, language_code=None, count=5):
    results = []
    seen = {seed_id}
    details = tmdb_get(f"/{media_type}/{seed_id}", {"append_to_response": "keywords"})
    
    recs = tmdb_get(f"/{media_type}/{seed_id}/recommendations", {"language": "en-US", "page": 1})
    for item in recs.get("results", []):
        if language_code and item.get("original_language") != language_code: continue
        if item["id"] not in seen:
            seen.add(item["id"])
            results.append(item)

    if len(results) < count:
        sims = tmdb_get(f"/{media_type}/{seed_id}/similar", {"language": "en-US", "page": 1})
        for item in sims.get("results", []):
            if language_code and item.get("original_language") != language_code: continue
            if item["id"] not in seen:
                seen.add(item["id"])
                results.append(item)
                
    if len(results) < count and details:
        genres = [str(g["id"]) for g in details.get("genres", [])[:2]]
        kw_key = "results" if media_type == "tv" else "keywords"
        keywords = [str(k["id"]) for k in details.get("keywords", {}).get(kw_key, [])[:4]]
        
        params = {"language": "en-US", "sort_by": "popularity.desc", "page": 1}
        if language_code: params["with_original_language"] = language_code
        
        if keywords: params["with_keywords"] = "|".join(keywords)
        elif genres: params["with_genres"] = ",".join(genres)
            
        disc = tmdb_get(f"/discover/{media_type}", params)
        for item in disc.get("results", []):
            if item["id"] not in seen:
                seen.add(item["id"])
                results.append(item)

    return results[:count]

def multi_search(query):
    query = str(query or "").strip()
    if not query: return []
    results = []
    m_data = tmdb_get("/search/movie", {"query": query, "include_adult": False, "language": "en-US", "page": 1})
    for i in m_data.get("results", [])[:8]: i["media_type"] = "movie"; results.append(i)
    t_data = tmdb_get("/search/tv", {"query": query, "include_adult": False, "language": "en-US", "page": 1})
    for i in t_data.get("results", [])[:8]: i["media_type"] = "tv"; results.append(i)

    unique_results = []
    seen = set()
    for item in results:
        key = (item.get("media_type"), item.get("id"))
        if key not in seen:
            seen.add(key)
            unique_results.append(item)

    unique_results.sort(key=lambda x: float(x.get("popularity") or 0), reverse=True)
    return unique_results[:8]

# =========================================================
# WATCH PROVIDERS & DIRECT DEEP LINKS
# =========================================================

def get_watch_providers(media_type, media_id):
    data = tmdb_get(f"/{media_type}/{media_id}/watch/providers")
    return data.get("results", {}).get("IN", {}) or {}

def encoded(text): return urllib.parse.quote_plus(str(text))

def provider_search_url(provider_name, title, media_type):
    name = provider_name.lower()
    q = encoded(title)
    if "netflix" in name: return f"https://www.netflix.com/search?q={q}"
    if "prime video" in name or "amazon prime" in name: return f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={q}"
    if "hotstar" in name or "disney" in name: return f"https://www.hotstar.com/in/explore?searchQuery={q}"
    if "jiocinema" in name: return f"https://www.jiocinema.com/search?q={q}"
    if "zee5" in name: return f"https://www.zee5.com/search?q={q}"
    if "sonyliv" in name or "sony liv" in name: return f"https://www.sonyliv.com/search/{q}"
    if "youtube" in name: return f"https://www.youtube.com/results?search_query={encoded(f'{title} full {media_type}')}"
    if "apple tv" in name: return f"https://tv.apple.com/in/search?term={q}"
    if "mx player" in name: return f"https://www.mxplayer.in/search/{q}"
    if "shemaroo" in name: return f"https://www.shemaroome.com/search?q={q}"
    return f"https://www.google.com/search?q={encoded(f'{title} watch on {provider_name}')}"

def youtube_link(title, content_type):
    suffix = "web series" if content_type == "tv" else "movie"
    return f"https://www.youtube.com/results?search_query={encoded(f'{title} official trailer {suffix}')}"

def safe_text(value, fallback=""): return html.escape(str(value if value is not None else fallback))

def show_watch_box(title, providers, content_type):
    raw_entries = []
    seen_names = set()
    
    # Custom priority: 0 is highest (Free/Stream), 4 is lowest (Buy)
    category_priority = {
        "free": {"prio": 0, "label": "FREE", "css": "type-free"},
        "ads": {"prio": 1, "label": "WITH ADS", "css": "type-free"},
        "flatrate": {"prio": 2, "label": "STREAM", "css": ""},
        "rent": {"prio": 3, "label": "RENT", "css": "type-rent"},
        "buy": {"prio": 4, "label": "BUY", "css": "type-rent"}
    }

    # Extract ONLY officially available platforms first
    for category in ["free", "ads", "flatrate", "rent", "buy"]:
        for p in providers.get(category, []) or []:
            name = p.get("provider_name")
            if name not in seen_names:
                seen_names.add(name)
                cat_info = category_priority[category]
                raw_entries.append({
                    "name": name,
                    "logo": p.get("logo_path"),
                    "type": cat_info["label"],
                    "css_class": cat_info["css"],
                    "priority": cat_info["prio"]
                })

    sorted_entries = sorted(raw_entries, key=lambda x: x["priority"])

    # === FORCE ADD YOUTUBE FOR EVERY MOVIE ===
    if not any("youtube" in e["name"].lower() for e in sorted_entries):
        sorted_entries.append({
            "name": "YouTube",
            "logo": "/pTnn5JwWr4p3pG8H6VrpiQo7Vs0.jpg",
            "type": "SEARCH",
            "css_class": "",
            "priority": 5
        })

    st.markdown('<div class="watch-box"><div class="watch-heading">📺 WHERE TO WATCH IN INDIA</div>', unsafe_allow_html=True)
    
    if sorted_entries:
        cards = []
        for e in sorted_entries:
            icon = f'<img src="{PROVIDER_LOGO_BASE}{html.escape(e["logo"])}" alt="logo">' if e.get("logo") else '<div class="provider-fallback-icon">📺</div>'
            url = provider_search_url(e["name"], title, content_type)
            css_class = f'provider-type {e.get("css_class", "")}'
            
            cards.append(f'<a class="provider-tile" href="{html.escape(url)}" target="_blank">'
                         f'<div class="provider-logo">{icon}</div>'
                         f'<div class="provider-info">'
                         f'<div class="provider-name">{safe_text(e["name"])}</div>'
                         f'<div class="{css_class}">{safe_text(e["type"])}</div>'
                         f'</div><div class="provider-arrow">↗</div></a>')
                         
        st.markdown('<div class="provider-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-watch">India me is title ki OTT details nahi mili.</div>', unsafe_allow_html=True)

    # Watch Trailer Button
    st.markdown(f'<a class="watch-action" href="{html.escape(youtube_link(title, content_type))}" target="_blank" style="background: rgba(255, 0, 0, 0.15); color: #ff4b4b !important; border-color: rgba(255, 0, 0, 0.3);">▶️ &nbsp; Watch Official Trailer</a></div>', unsafe_allow_html=True)

def show_movie_card(movie):
    title = movie.get("title") or movie.get("name") or "Unknown"
    media_type = "movie" if "title" in movie else "tv"
    m_id = movie.get("id")
    poster = movie.get("poster_path")
    rating = float(movie.get("vote_average") or 0)
    year = (movie.get("release_date") or movie.get("first_air_date") or "N/A")[:4]
    overview = movie.get("overview", "No overview available.")

    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
    if poster:
        st.markdown('<div class="poster-frame">', unsafe_allow_html=True)
        st.image(IMAGE_BASE + poster, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="card-title">{safe_text(title)}</div>
        <div class="card-meta"><span class="rating">⭐ {rating:.1f}</span> &nbsp; • &nbsp; {year} &nbsp; <span class="type">{media_type.upper()}</span></div>
        <div class="overview">{safe_text(overview[:230])}{'...' if len(overview) > 230 else ''}</div>
    """, unsafe_allow_html=True)
    show_watch_box(title, get_watch_providers(media_type, m_id), media_type)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# UI HEADER
# =========================================================

st.markdown("""
    <div class="brand-row">
        <div class="brand">🎬 Cine<span>Match</span> AI</div>
        <div class="top-pill">Movies + Web Series • India</div>
    </div>
""", unsafe_allow_html=True)

st.html("""
    <div class="hero-wrap">
        <div class="hero-glow"></div>
        <div class="hero-content">
            <div class="eyebrow">AI POWERED ENTERTAINMENT DISCOVERY</div>
            <div class="hero-title">Your next<br><span class="accent">favourite story.</span></div>
            <div class="hero-copy">Discover movies, web series, and explore your favourite actors' work all in one place.</div>
            <div class="hero-tags"><span>🎬 Movies</span> <span>📺 Web Series</span> <span>🎭 Cast & Crew</span></div>
        </div>
    </div>
""")

# =========================================================
# TABS
# =========================================================

tab_movies, tab_series, tab_cast, tab_search = st.tabs(["🎬 Movies", "📺 Web Series", "🎭 Cast & Crew", "🔎 Search"])
language_map = {"All Languages": None, "Hindi": "hi", "English": "en", "Tamil": "ta", "Telugu": "te", "Malayalam": "ml"}

with tab_movies:
    st.markdown('<div class="section-head"><div><div class="section-title">🎬 Find Your Next Movie</div><div class="section-subtitle">Apni favourite movie ka naam likho aur similar movies discover karo.</div></div></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1: m_query = st.text_input("Movie Name", placeholder="e.g. Hanuman, RRR...", key="m_q")
    with col2: m_lang = st.selectbox("Language", list(language_map.keys()), key="m_l")
    
    if st.button("✨ Recommend Movies"):
        if not m_query: st.warning("Movie ka naam enter karein!")
        else:
            with st.spinner("Finding matches..."):
                movie = search_movie(m_query)
                if not movie: st.error("Movie nahi mili.")
                else:
                    recs = get_smart_recommendations("movie", movie["id"], language_map[m_lang])
                    if recs:
                        st.markdown(f"### ✨ Because you liked {movie['title']}")
                        cols = st.columns(min(len(recs), 5))
                        for col, rec in zip(cols, recs):
                            with col: show_movie_card(rec)
                    else: st.info("No close matches found in this language.")

with tab_series:
    st.markdown('<div class="section-head"><div><div class="section-title">📺 Discover Web Series</div><div class="section-subtitle">Favorite show search karein aur waise hi naye shows paayein.</div></div></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1: tv_query = st.text_input("Web Series Name", placeholder="e.g. Panchayat, Breaking Bad...", key="tv_q")
    with col2: tv_lang = st.selectbox("Language", list(language_map.keys()), key="tv_l")
    
    if st.button("✨ Recommend Series"):
        if not tv_query: st.warning("Web series ka naam enter karein!")
        else:
            with st.spinner("Finding matches..."):
                series = search_tv(tv_query, language_map[tv_lang])
                if not series: st.error("Series nahi mili.")
                else:
                    recs = get_smart_recommendations("tv", series["id"], language_map[tv_lang])
                    if recs:
                        st.markdown(f"### 🔥 Shows similar to {series['name']}")
                        cols = st.columns(min(len(recs), 5))
                        for col, rec in zip(cols, recs):
                            with col: show_movie_card(rec)
                    else: st.info("No close matches found.")

with tab_cast:
    st.markdown('<div class="search-hero"><div class="section-title">🎭 Explore by Actor or Director</div><div class="section-subtitle">Kisi bhi actor ya director ki best movies ek jagah dekho.</div></div>', unsafe_allow_html=True)
    person_query = st.text_input("Search Actor or Director", placeholder="e.g. Shahrukh Khan, SS Rajamouli...", key="person_q")
    
    if st.button("🔍 Find Work") and person_query:
        with st.spinner("Loading profile..."):
            person = search_person(person_query)
            if not person: st.error("Person not found.")
            else:
                st.markdown(f"### 🌟 Best of {person['name']}")
                credits = get_person_credits(person["id"])
                if credits:
                    for i in range(0, len(credits), 5):
                        cols = st.columns(5)
                        for col, credit in zip(cols, credits[i:i+5]):
                            with col: show_movie_card(credit)
                else: st.info("No major movies/shows found for this person.")

with tab_search:
    st.markdown('<div class="search-hero"><div class="section-title">🔎 Global Search</div><div class="section-subtitle">Directly search any movie or show to check where to watch.</div></div>', unsafe_allow_html=True)
    g_query = st.text_input("Search Anything...", key="g_q")
    if st.button("Search") and g_query:
        with st.spinner("Searching..."):
            results = multi_search(g_query)
            if results:
                for r in results:
                    st.markdown('<div class="result-row">', unsafe_allow_html=True)
                    col_img, col_info = st.columns([1, 4])
                    
                    title = r.get("title") or r.get("name") or "Unknown"
                    media_type = r.get("media_type", "movie")
                    m_id = r.get("id")
                    
                    with col_img:
                        if r.get("poster_path"): st.image(IMAGE_BASE + r.get("poster_path"))
                    with col_info:
                        st.markdown(f"### {title}")
                        st.write(r.get("overview", "No overview."))
                        
                        providers = get_watch_providers(media_type, m_id)
                        show_watch_box(title, providers, media_type)
                        
                    st.markdown('</div>', unsafe_allow_html=True)
            else: st.info("Kuch nahi mila.")

st.markdown('<div class="footer"><strong>🎬 CineMatch AI</strong><br>Powered by TMDB Native AI & JustWatch OTT Data.</div>', unsafe_allow_html=True)