from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Your API key and default country
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DEFAULT_COUNTRY = os.getenv('DEFAULT_COUNTRY', 'za')

def fetch_news(topic=None, country=None, search_term=None):
    base_url = "https://newsapi.org/v2/top-headlines"

    # Set default country if none provided
    if not country:
        country = DEFAULT_COUNTRY

    # Build parameters
    params = {
        'apiKey': NEWS_API_KEY,
        'country': country
    }

    # Add topic if provided
    if topic:
        # Use string concatenation instead of f-string
        if search_term:
            topic = topic + " " + search_term
        params['q'] = topic

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # If no articles found for ZA, try US as fallback
        if country == 'za' and (not data.get('articles') or len(data['articles']) == 0):
            params['country'] = 'us'
            response = requests.get(base_url, params=params)
            data = response.json()

        return data
    except Exception as e:
        print("Error fetching news:", str(e))
        return {'articles': [], 'error': str(e)}

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "API is working!"})

@app.route('/fetch-news', methods=['GET'])
def get_news():
    topic = request.args.get('topic')
    country = request.args.get('country')
    search_term = request.args.get('search_term')

    data = fetch_news(topic, country, search_term)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)