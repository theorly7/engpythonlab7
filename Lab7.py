import requests
import json

#-------------TASK 1 OpenWeather-------------
def get_coordinates(city_name, api_key):

    print('#-------------TASK 1 OpenWeather-------------')
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city_name,
        'limit': 1,
        'appid': api_key
    }

    try:
        response = requests.get(geo_url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon'], data[0].get('country', 'N/A')
            else:
                return None, None, None
        else:
            print(f"Geocode error: {response.status_code}")
            return None, None, None
    except Exception as e:
        print(f"Error with the coordinates request: {e}")
        return None, None, None


def get_weather(lat, lon, api_key):
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',
    }

    try:
        response = requests.get(weather_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"OneCall API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error with the weather request: {e}")
        return None


def display_weather(city_name, api_key):

    # 1. Get the coordinates using OpenWeather geocode
    lat, lon, country = get_coordinates(city_name, api_key)

    # 2. Get the weather
    weather_data = get_weather(lat, lon, api_key)

    main = weather_data['main']

    # 3. Final result
    print(f"City: {city_name}, {country}")
    print(f"Temperature: {main['temp']}°C")
    print(f"Humidity: {main['humidity']}%")
    print(f"Pressure: {main['pressure']} гПа")


#-------------TASK 2 NewsAPI-------------

def get_news(category, api_key_newsapi, output_file):

    print('-------------TASK 2 NewsAPI-------------')
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'category': category,
        'pageSize': 50,
        'apiKey': api_key_newsapi
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Structured output
            articles_clean = []
            for article in data.get('articles', []):
                clean_article = {
                    "title": article.get('title'),
                    "source": article.get('source', {}).get('name'),
                    "author": article.get('author') or "No author",
                    "description": article.get('description'),
                    "published_at": article.get('publishedAt'),
                    "url": article.get('url')
                }
                articles_clean.append(clean_article)

            # Final structure
            output_data = {
                "category": category,
                "total_results": len(articles_clean),
                "articles": articles_clean
            }

            # JSON output
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f"{len(articles_clean)} articles in file '{output_file}'")
            return True

        else:
            print(f"NewsAPI error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error with the NewsAPI request: {e}")
        return None


if __name__ == "__main__":

    # ===== TASK 1 =====
    API_KEY = "b24d732e90fa4731f0b9546aae6f6d93"
    city = "Berezniki"
    display_weather(city, API_KEY)

    # ===== TASK 2 =====
    CATEGORY = 'business'
    API_KEY_NEWSAPI = 'd581663fecc142d4a392715e135b1ddf'
    OUTPUT_FILE = "news_output.json"
    get_news(CATEGORY, API_KEY_NEWSAPI, OUTPUT_FILE)

