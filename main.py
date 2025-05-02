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
                    "text": f"""
You are a biography expert. Write a full-length biography of {name} in the "Ranked Biography" format used by Paradum.

The format should include the following sections, well-structured, easy-to-read, and detailed:

1. SEO Optimized Title  
2. Meta Description  
3. Summary Paragraph  
4. Personal Details (Full Name, Nickname, Date of Birth, Age, Birthplace, Hometown, Nationality, Religion, Profession)  
5. Physical Stats (Height, Weight, Eye Color, Hair Color, Skin Tone, Tattoos)  
6. Education (School, College/University, Qualification)  
7. Family and Relationships (Father, Mother, Siblings, Relationship Status, Spouse, Children)  
8. Favorites (Food, Actor, Actress, Color, Place, Hobbies, Inspiration)  
9. Social Media Handles (Instagram, YouTube, Twitter, Facebook – link format)  
10. Net Worth (Approx in INR and USD)  
11. Career Journey  
12. Lesser Known Facts  
13. Conclusion (inspiring ending line)  

Use proper formatting, headers, and line breaks. Keep the tone informative, clear, and friendly. No fake info – only provide what's publicly known or likely to be true. Avoid placeholder values like 'N/A' or 'Unknown'.

Do not add tags or keywords at the end.
"""
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
