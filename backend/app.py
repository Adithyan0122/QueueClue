from flask import Flask, request, jsonify
from flask_cors import CORS
import openai  # or your preferred LLM API

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Configure your OpenAI key
openai.api_key = "your-openai-api-key"

@app.route('/')
def index():
    return "QueueClue Backend is Running!"

@app.route('/api/generate-hint', methods=['POST'])
def generate_hint():
    data = request.json
    question = data.get('question', '')
    user_code = data.get('user_code', '')

    if not question or not user_code:
        return jsonify({'error': 'Both question and user_code are required.'}), 400

    # Construct your prompt (be sure to fine-tune this for best results)
    prompt = f"""
You are a helpful coding assistant for data structures and algorithms (DSA).
You are given a LeetCode-style question and a user's code attempt.
Instead of solving the problem, give a guiding hint that helps the user improve their approach or correct their logic.
Be constructive and avoid giving the final answer.

Question:
{question}

User's Code:
{user_code}

Helpful Hint:
"""

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # or gpt-4 / gpt-3.5-turbo with ChatCompletion API
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
            stop=["\n\n"]
        )
        hint = response.choices[0].text.strip()
        return jsonify({'hint': hint})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)