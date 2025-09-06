from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) 

VLLM_API_URL = "http://localhost:8000/v1/completions"

@app.route('/')
def index():
    """
    Renders the main HTML page.
    """
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_llm():
    """
    Handles the API request from the frontend.
    It takes the user's prompt, sends it to the vLLM server, and returns the response.
    """
    user_input = request.json.get('prompt')
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400

    
    formatted_prompt = f"### Human: {user_input}\n### Assistant:"
    
    payload = {
        "model": "facebook/opt-125m", 
        "prompt": formatted_prompt,
        "max_tokens": 128,  
        "temperature": 0.7 
    }

    try:
        response = requests.post(VLLM_API_URL, json=payload, timeout=60)
        response.raise_for_status() 
        llm_response = response.json()
        
        output_text = llm_response['choices'][0]['text']
        return jsonify({"response": output_text})
    
    except requests.exceptions.RequestException as e:
        print(f"API request to vLLM failed: {e}")
        return jsonify({"error": f"Failed to connect to the LLM backend."}), 500

if __name__ == '__main__':
    app.run(debug=True)