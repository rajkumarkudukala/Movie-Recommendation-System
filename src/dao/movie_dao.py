# src/dao/movie_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class MovieDAO:
    def __init__(self):
        self.__sb = get_supabase()
        self.__movies_table = "movies"
        self.__movie_genres_table = "movie_genres"

    # -----------------------------
    # Movies Table Operations
    # -----------------------------
    def create_movie(self, title: str, language: str, region: str, release_year: int, rating: float) -> Optional[Dict]:
        payload = {
            "title": title,
            "language": language,
            "region": region,
            "release_year": release_year,
            "rating": rating
        }
        self.__sb.table(self.__movies_table).insert(payload).execute()
        resp = self.__sb.table(self.__movies_table).select("*").eq("title", title).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_movie_by_id(self, movie_id: int) -> Optional[Dict]:
        resp = self.__sb.table(self.__movies_table).select("*").eq("movie_id", movie_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_movies(self, limit: int = 100) -> List[Dict]:
        resp = self.__sb.table(self.__movies_table).select("*").order("movie_id", desc=False).limit(limit).execute()
        return resp.data or []

    def update_movie(self, movie_id: int, fields: Dict) -> Optional[Dict]:
        self.__sb.table(self.__movies_table).update(fields).eq("movie_id", movie_id).execute()
        resp = self.__sb.table(self.__movies_table).select("*").eq("movie_id", movie_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_movie(self, movie_id: int) -> Optional[Dict]:
        # fetch row before delete
        resp_before = self.__sb.table(self.__movies_table).select("*").eq("movie_id", movie_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self.__sb.table(self.__movies_table).delete().eq("movie_id", movie_id).execute()
        return row

    # -----------------------------
    # Movie_Genres Table Operations
    # -----------------------------
    def add_genres_to_movie(self, movie_id: int, genre_ids: List[int]):
        payloads = [{"movie_id": movie_id, "genre_id": gid} for gid in genre_ids]
        self.__sb.table(self.__movie_genres_table).insert(payloads).execute()

    def get_genres_of_movie(self, movie_id: int) -> List[int]:
        resp = self.__sb.table(self.__movie_genres_table).select("genre_id").eq("movie_id", movie_id).execute()
        return [item["genre_id"] for item in resp.data] if resp.data else []

    def remove_genres_from_movie(self, movie_id: int):
        self.__sb.table(self.__movie_genres_table).delete().eq("movie_id", movie_id).execute()

    # -----------------------------
    # Movies by Genre
    # -----------------------------
    def get_movies_by_genre(self, genre_id: int, limit: int = 50) -> List[Dict]:
        resp = (
            self.__sb.table(self.__movie_genres_table)
            .select("movie_id(*)")  # fetch full movie details
            .eq("genre_id", genre_id)
            .limit(limit)
            .execute()
        )
        movies = [item["movie_id"] for item in resp.data] if resp.data else []
        return movies

    def get_movies_by_genres(self, genre_ids: List[int], limit: int = 50) -> List[Dict]:
        resp = (
            self.__sb.table(self.__movie_genres_table)
            .select("movie_id(*)")
            .in_("genre_id", genre_ids)
            .limit(limit)
            .execute()
        )
        movies = [item["movie_id"] for item in resp.data] if resp.data else []
        return movies
