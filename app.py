from flask import Flask, request, jsonify
from google_reviews_scraper import scrape_google_reviews

app = Flask(__name__)

@app.route("/scrape/google", methods=["POST"])
def scrape_google():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        reviews = scrape_google_reviews(url, max_reviews=30)
        return jsonify({"status": "success", "reviews": reviews})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
