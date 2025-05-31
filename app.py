from flask import Flask, render_template
import requests
import random

def create_app():
    app = Flask(__name__)

    # Fetch Kanjis from kanjiapi based on type
    def get_kanjis(type):
        url = f"https://kanjiapi.dev/v1/kanji/{type}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else []
    
    # Fetch Kanji from kanjiapi based on jlpt level
    def fetch_kanji_list(jlpt_level):
        url = f"https://kanjiapi.dev/v1/kanji/jlpt-{jlpt_level}"
        response = requests.get(url)
        return response.json() if response.status_code == 200 else []

    # Fetches details of a certain kanji
    def kanji_details(kanji):
        details = requests.get(f"https://kanjiapi.dev/v1/kanji/{kanji}").json()
        return details
    
    # Converts katakana to hiragana
    def kata_to_hira(text):
        """Convert all katakana in the string to hiragana."""
        return ''.join(
            chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c
            for c in text
        )

    # Include with or without okurigana
    def expand_kunyomi(readings):
        expanded = []
        for reading in readings:
            parts = reading.split('.')
            if len(parts) == 2:
                expanded.append(parts[0])              
                expanded.append(''.join(parts))        
            else:
                expanded.append(reading)
        return expanded
    
    @app.route("/readings")
    def readings():
        combined = get_kanjis("all")
        random_kanji = random.choice(combined)
        details = kanji_details(random_kanji)
        on = [kata_to_hira(text) for text in details["on_readings"]]
        kun = expand_kunyomi(details["kun_readings"])
        print(f"Random Kanji Selected: {random_kanji}, Reading: {kun + on}")
        return render_template(
            "readings.html", 
            kanji=random_kanji, 
            kanji_readings=kun + on
        )

    @app.route("/meanings")
    def meanings():
        n5 = fetch_kanji_list(5)
        n4 = fetch_kanji_list(4)
        combined = n5 + n4
        random_kanji = random.choice(combined)
        details = kanji_details(random_kanji)
        meanings = details["meanings"]
        print(f"Random Kanji Selected: {random_kanji}, Meanings: {meanings}")
        return render_template(
            "meanings.html", 
            kanji=random_kanji, 
            kanji_meanings=meanings
        )
    return app


if __name__ == "__main__":
    app = create_app()
    FLASK_PORT = 3000
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=True)
else:
    app = create_app()