from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
# Enable CORS for local development
CORS(app) 

# This is the URL of your running vLLM API server.
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

    # Format the input as a single string, which is what the /v1/completions endpoint expects.
    # This also helps to guide the model's response.
    formatted_prompt = f"### Human: {user_input}\n### Assistant:"
    
    # Prepare the payload for the vLLM completions API.
    # The key is now "prompt", not "messages".
    payload = {
        "model": "facebook/opt-125m",  # The model name must match the one used to start vLLM
        "prompt": formatted_prompt,
        "max_tokens": 128,  # A good practice to limit the response length
        "temperature": 0.7  # Controls the randomness of the output
    }

    try:
        # Send the request to the vLLM completions endpoint
        response = requests.post(VLLM_API_URL, json=payload, timeout=60)
        # Raise an exception for HTTP errors (e.g., 404, 500)
        response.raise_for_status() 
        llm_response = response.json()
        
        # Extract the text from the completions response
        output_text = llm_response['choices'][0]['text']
        return jsonify({"response": output_text})
    
    except requests.exceptions.RequestException as e:
        print(f"API request to vLLM failed: {e}")
        return jsonify({"error": f"Failed to connect to the LLM backend."}), 500

if __name__ == '__main__':
    # Running the Flask app in debug mode.
    app.run(debug=True)