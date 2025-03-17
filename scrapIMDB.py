from bs4 import BeautifulSoup
import requests
import csv



try:
    source = requests.get('http://127.0.0.1:5500/IMDb%20Top%20250%20Movies.html')
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')

    # Find the movie list
    movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-e22973a9-0 khSCXM compact-list-view ipc-metadata-list--base").find_all('li')

    # Create CSV file and write headers
    with open("imdb_top_movies.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Rank", "Name", "Year", "Duration (min)", "Age Rating", "Rating", "Votes"])  # Header row

        # Extract data from each movie
        for movie in movies:
            name = movie.find('h3', class_='ipc-title__text').text.strip()

            # Extract rank and movie name
            rank, name = name.split(". ", 1)

            # Extract year, duration, and age rating
            additional_info = movie.find_all('span', class_='sc-d5ea4b9d-7 URyjV cli-title-metadata-item')

            if len(additional_info) >= 3:
                year = additional_info[0].text.strip()
                duration_all = additional_info[1].text.strip()
                age_rating = additional_info[2].text.strip()
            else:
                year, duration_all, age_rating = "N/A", "N/A", "N/A"  # Fallback in case of missing data

            # Convert duration to minutes
            hour, minute = 0, 0
            if "h" in duration_all:
                hour = int(duration_all.split("h")[0].strip())
            if "m" in duration_all:
                minute = int(duration_all.split("h")[-1].replace("m", "").strip()) if "h" in duration_all else int(duration_all.replace("m", "").strip())
            duration = (hour * 60) + minute if duration_all != "N/A" else "N/A"

            # Extract IMDb rating
            rating = movie.find('span', class_='ipc-rating-star--rating')
            rating = float(rating.text.strip()) if rating else "N/A"

            # Extract vote count
            rating_no = movie.find('span', class_='ipc-rating-star--voteCount')
            rating_count = rating_no.text.strip().replace("(", "").replace(")", "").replace(",", "") if rating_no else "N/A"

            # Write data to CSV
            writer.writerow([rank, name, year, duration, age_rating, rating, rating_count])

    print("✅ Data successfully saved to 'imdb_top_movies.csv'.")

except requests.exceptions.RequestException as e:
    print(f"❌ Error fetching IMDb data: {e}")