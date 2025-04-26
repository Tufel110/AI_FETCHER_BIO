from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyAavza2qWGY484PblZOyXoUn3Kmy-isAHE"  # Replace with your actual API key

@app.route('/bio', methods=['GET'])
def get_biography():
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Please provide a celebrity name using ?name=YourCelebrity'}), 400

    # Corrected the model name to 'gemini-pro' which is the correct identifier
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyAavza2qWGY484PblZOyXoUn3Kmy-isAHE"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Write a short, clear, 100-150 word biography of {name} including key facts, background, and major achievements."
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    try:
        bio_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({
            'status': 'success',
            'input': name,
            'bio': bio_text
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'input': name,
            'bio': "Gemini returned no content or model error.",
            'details': str(e),
            'raw': data
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)