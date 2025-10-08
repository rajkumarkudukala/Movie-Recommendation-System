# src/services/movie_service.py
from typing import List, Dict
from src.dao.movie_dao import MovieDAO

class MovieError(Exception):
    """Custom exception for movie service errors"""
    pass

class MovieService:
    def __init__(self):
        self.dao = MovieDAO()

    # -----------------------------
    # Create and Manage Movies
    # -----------------------------
    def add_movie(
        self,
        title: str,
        language: str,
        region: str,
        release_year: int,
        rating: float,
        platform: str = None,
        genre_ids: List[int] = None
    ) -> Dict:
        if rating < 0 or rating > 10:
            raise MovieError("Rating must be between 0 and 10")
        
        # Check if movie already exists
        existing_movies = self.dao.list_movies(limit=1000)
        if any(m["title"].lower() == title.lower() for m in existing_movies):
            raise MovieError(f"Movie '{title}' already exists.")
        
        movie = self.dao.create_movie(title, language, region, release_year, rating)
        # Update platform if provided
        if platform:
            self.dao.update_movie(movie["movie_id"], {"platform": platform})
            movie["platform"] = platform
        
        # Add genres if provided
        if genre_ids:
            self.dao.add_genres_to_movie(movie["movie_id"], genre_ids)
        
        return movie

    # -----------------------------
    # List all movies
    # -----------------------------
    def list_all_movies(self, limit: int = 100) -> List[Dict]:
        return self.dao.list_movies(limit=limit)

    # -----------------------------
    # Search & Recommendations
    # -----------------------------
    def search_movies(
        self,
        genre_ids: List[int] = None,
        language: str = None,
        region: str = None,
        platform: str = None
    ) -> List[Dict]:
        movies = self.dao.list_movies(limit=1000)  # fetch all
        results = movies

        # Filter by language
        if language:
            results = [m for m in results if m["language"].lower() == language.lower()]
        # Filter by region
        if region:
            results = [m for m in results if m["region"].lower() == region.lower()]
        # Filter by platform
        if platform:
            results = [m for m in results if platform.lower() in (m.get("platform") or "").lower()]
        # Filter by genres
        if genre_ids:
            filtered = []
            for m in results:
                movie_genres = self.dao.get_genres_of_movie(m["movie_id"])
                if any(gid in movie_genres for gid in genre_ids):
                    filtered.append(m)
            results = filtered
        return results

    # -----------------------------
    # Recommendations
    # -----------------------------
    def get_recommendations(
        self,
        favorite_genres: List[int],
        min_rating: float = 7.0,
        limit: int = 10
    ) -> List[Dict]:
        movies = self.dao.get_movies_by_genres(favorite_genres, limit=1000)
        # Filter by rating
        recommendations = [m for m in movies if m["rating"] >= min_rating]
        # Sort by rating descending and limit
        recommendations.sort(key=lambda x: x["rating"], reverse=True)
        return recommendations[:limit]
