from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import feedparser
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

RSS_FEEDS = {
    "Reuters": "http://feeds.reuters.com/reuters/businessNews",
    "FXStreet": "https://www.fxstreet.com/rss/news",
    "Treasury": "https://home.treasury.gov/news/press-releases/rss"
}

TRIGGER_KEYWORDS = ["Trump", "tariff", "trade war", "inflation", "rate hike", "Powell", "ECB", "PBOC", "GDP", "NFP"]

def fetch_alerts():
    alerts = []
    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Just latest 5 from each
            title = entry.title
            if any(kw.lower() in title.lower() for kw in TRIGGER_KEYWORDS):
                alert = {
                    "source": source,
                    "timestamp": entry.published if 'published' in entry else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "news": title,
                    "link": entry.link
                }
                alerts.append(alert)
    return alerts

@app.route("/alerts")
def get_alerts():
    return jsonify(fetch_alerts())

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
