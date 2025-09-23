# src/cli/main.py
from src.services.movie_service import MovieService

def main():
    service = MovieService()

    while True:
        print("\n--- Movie Recommendation System ---")
        print("1. Movie Recommendations")
        print("2. View All Movies")
        print("3. Search Movies")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            print("\n--- Get Recommendations ---")
            print("Available Genres (IDs): 1. Action, 2. Adventure, 3. Comedy, 4. Drama, 5. Thriller, 6. Sci-Fi, 7. Romance,8. Horror,9. Animation,10. Fantasy")
            fav_genres = input("Enter your favorite genre IDs (comma-separated): ").strip()

            fav_genres = [int(gid) for gid in fav_genres.split(",") if gid.isdigit()]
            min_rating = input("Minimum rating (1-10, default 7): ").strip()
            min_rating = float(min_rating) if min_rating else 7.0
            recommendations = service.get_recommendations(fav_genres, min_rating)
            if recommendations:
                print("\nTop Recommendations:")
                for m in recommendations:
                    print(f"{m['title']} | {m['language']} | {m['region']} | {m['release_year']} | Rating: {m['rating']}")
            else:
                print("No recommendations found.")

        elif choice == '2':
            print("\n--- All Movies ---")
            movies = service.list_all_movies()
            for m in movies:
                print(f"{m['title']} | {m['language']} | {m['region']} | {m['release_year']} | Rating: {m['rating']}")

        elif choice == '3':
            print("\n--- Search Movies ---")
            genre_ids = input("Genre IDs (comma-separated, leave blank for all): ").strip()
            genre_ids = [int(gid) for gid in genre_ids.split(",") if gid.isdigit()] if genre_ids else None
            language = input("Language (leave blank for any): ").strip() or None
            region = input("Region (leave blank for any): ").strip() or None
            results = service.search_movies(genre_ids=genre_ids, language=language, region=region)
            if results:
                print("\nSearch Results:")
                for m in results:
                    print(f"{m['title']} | {m['language']} | {m['region']} | {m['release_year']} | Rating: {m['rating']}")
            else:
                print("No movies found matching your criteria.")

        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
