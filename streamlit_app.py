# streamlit_app.py
import streamlit as st
from src.services.movie_service import MovieService

# Initialize service
service = MovieService()

st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# -----------------------------
# Sidebar / Menu
# -----------------------------
st.sidebar.title("Movie Recommendation System")
menu = st.sidebar.radio("Menu", ["Recommendations", "View All Movies", "Search Movies"])

# Available genres
genre_options = {
    1: "Action", 2: "Adventure", 3: "Comedy", 4: "Drama",
    5: "Thriller", 6: "Sci-Fi", 7: "Romance", 8: "Horror",
    9: "Animation", 10: "Fantasy"
}

# -----------------------------
# 1. Recommendations
# -----------------------------
if menu == "Recommendations":
    st.header("🎬 Movie Recommendations")

    selected_genres = st.multiselect(
        "Select your favorite genres:",
        options=list(genre_options.keys()),
        format_func=lambda x: genre_options[x]
    )

    min_rating = st.slider("Minimum rating:", 1.0, 10.0, 7.0, 0.1)

    if st.button("Get Recommendations"):
        if not selected_genres:
            st.warning("Please select at least one genre!")
        else:
            recommendations = service.get_recommendations(selected_genres, min_rating)
            if recommendations:
                st.success(f"Top {len(recommendations)} Recommendations:")
                
                # Display in 3 columns
                cols = st.columns(3)
                for idx, m in enumerate(recommendations):
                    col = cols[idx % 3]
                    col.markdown(f"### {m['title']}")
                    col.markdown(f"**Language:** {m['language']}")
                    col.markdown(f"**Region:** {m['region']}")
                    col.markdown(f"**Release Year:** {m['release_year']}")
                    col.markdown(f"**Rating:** {m['rating']}")
                    col.markdown(f"**Platform:** {m.get('platform', 'N/A')}")
                    col.markdown("---")
            else:
                st.info("No recommendations found for your criteria.")

# -----------------------------
# 2. View All Movies
# -----------------------------
elif menu == "View All Movies":
    st.header("🎥 All Movies")
    movies = service.list_all_movies(limit=1000)
    if movies:
        cols = st.columns(3)
        for idx, m in enumerate(movies):
            col = cols[idx % 3]
            col.markdown(f"### {m['title']}")
            col.markdown(f"**Language:** {m['language']}")
            col.markdown(f"**Region:** {m['region']}")
            col.markdown(f"**Release Year:** {m['release_year']}")
            col.markdown(f"**Rating:** {m['rating']}")
            col.markdown(f"**Platform:** {m.get('platform', 'N/A')}")
            col.markdown("---")
    else:
        st.info("No movies available.")

# -----------------------------
# 3. Search Movies
# -----------------------------
elif menu == "Search Movies":
    st.header("🔍 Search Movies")

    selected_genres = st.multiselect(
        "Genres (optional):",
        options=list(genre_options.keys()),
        format_func=lambda x: genre_options[x]
    )

    language = st.text_input("Language (optional)")
    region = st.text_input("Region (optional)")

    if st.button("Search"):
        results = service.search_movies(
            genre_ids=selected_genres if selected_genres else None,
            language=language or None,
            region=region or None
        )
        if results:
            st.success(f"Found {len(results)} movies:")
            cols = st.columns(3)
            for idx, m in enumerate(results):
                col = cols[idx % 3]
                col.markdown(f"### {m['title']}")
                col.markdown(f"**Language:** {m['language']}")
                col.markdown(f"**Region:** {m['region']}")
                col.markdown(f"**Release Year:** {m['release_year']}")
                col.markdown(f"**Rating:** {m['rating']}")
                col.markdown(f"**Platform:** {m.get('platform', 'N/A')}")
                col.markdown("---")
        else:
            st.info("No movies found matching your criteria.")
