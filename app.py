from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

# HTML page with a form and JavaScript for interactivity
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fake News Checker</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        input { padding: 8px; width: 80%; }
        button { padding: 10px; margin-top: 10px; }
        .result { margin-top: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <h2>Fake News Checker</h2>
    <input type="text" id="urlInput" placeholder="Enter a URL...">
    <button onclick="checkFakeNews()">Check</button>
    <div class="result" id="result"></div>

    <script>
        function checkFakeNews() {
            const url = document.getElementById("urlInput").value;
            if (!url) {
                document.getElementById("result").innerHTML = "Please enter a URL.";
                return;
            }

            fetch('/check', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ "url": url })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").innerHTML = 
                    `<p><b>URL:</b> ${data.url}</p>
                     <p><b>Fake Probability:</b> ${data.fake_probability * 100}%</p>`;
            })
            .catch(error => {
                document.getElementById("result").innerHTML = "Error checking the URL.";
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check_fake_news():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400

    user_url = data['url']
    fake_probability = round(random.uniform(0, 1), 2)

    return jsonify({
        "url": user_url,
        "fake_probability": fake_probability
    })

if __name__ == '__main__':
    app.run(debug=True)
