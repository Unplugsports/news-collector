import requests  # Add this line at the top of the file
class NewsCollector:
    def __init__(self, api_key, default_country="za"):
        self.api_key = api_key
        self.default_country = default_country
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def fetch_news(self, topic=None, country=None):
        """
        Fetch news articles based on the topic and country.
        """
        if not country:
            country = self.default_country  # Use the default country if none is provided

        params = {
            "apiKey": self.api_key,
            "country": country,
        }

        if topic:
            params["q"] = topic  # Add the topic to the query if provided

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            # Check if the response is successful and contains articles
            if data.get("status") == "ok" and data.get("articles"):
                return data.get("articles", [])
            else:
                # Fallback to 'us' if no articles are found for the given country
                if country != "us":  # Avoid infinite fallback loop
                    print(f"No articles found for {country}. Falling back to 'us'.")
                    return self.fetch_news(topic=topic, country="us")
                else:
                    print(f"Error fetching news: {data.get('message')}")
                    return []
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []