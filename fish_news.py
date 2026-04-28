import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ----------------------------
# CONFIG: Add your RSS feeds
# ----------------------------

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=fish+farming",
    "https://news.google.com/rss/search?q=seafood+industry",
    "https://news.google.com/rss/search?q=aquaculture"
]

# ----------------------------
# Helper: Clean HTML
# ----------------------------
def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()

# ----------------------------
# Helper: Simple summarizer
# ----------------------------
def summarize(text, max_words=40):
    words = text.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

# ----------------------------
# Fetch RSS news
# ----------------------------
def fetch_news():
    articles = []
    seen_links = set()

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            link = entry.get("link")

            if not link or link in seen_links:
                continue

            seen_links.add(link)

            title = entry.get("title", "No Title")
            summary = entry.get("summary", "")

            clean_summary = clean_html(summary)
            short_summary = summarize(clean_summary)

            published = entry.get("published", "")
            try:
                published_date = datetime(*entry.published_parsed[:6])
            except:
                published_date = None

            articles.append({
                "title": title,
                "summary": short_summary,
                "link": link,
                "published": str(published_date)
            })

    return articles

# ----------------------------
# Save to JSON
# ----------------------------
def save_to_json(data, filename="fish_news.json"):
    import json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def fetch_news():
    articles = []
    seen_links = set()

    for feed_url in RSS_FEEDS:
        print(f"Fetching: {feed_url}")  # DEBUG

        feed = feedparser.parse(feed_url)

        print(f"Entries found: {len(feed.entries)}")  # DEBUG

        for entry in feed.entries:
            link = entry.get("link")

            if not link or link in seen_links:
                continue

            seen_links.add(link)

            title = entry.get("title", "No Title")
            summary = entry.get("summary", "")

            clean_summary = clean_html(summary)
            short_summary = summarize(clean_summary)

            articles.append({
                "title": title,
                "summary": short_summary,
                "link": link
            })

    return articles




# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    news = fetch_news()
    save_to_json(news)

    print(f"✅ Fetched {len(news)} articles and saved to fish_news.json")