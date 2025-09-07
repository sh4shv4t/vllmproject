from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import requests
import sqlite3
import json
import uuid

def get_db_connection():
    conn = sqlite3.connect('chat_history.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

create_table()

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_super_secret_key' 

VLLM_API_URL = "http://localhost:8000/v1/completions"

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_llm():
    user_input = request.json.get('prompt')
    session_id = request.json.get('session_id', str(uuid.uuid4()))
    
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400

    conn = get_db_connection()
    
    conn.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
                 (session_id, 'user', user_input))
    conn.commit()

    messages_from_db = conn.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp', (session_id,)).fetchall()
    conn.close()
    
    formatted_prompt = ""
    for msg in messages_from_db:
        if msg['role'] == 'user':
            formatted_prompt += f"### Human: {msg['content']}\n"
        else:
            formatted_prompt += f"### Assistant: {msg['content']}\n"
    formatted_prompt += "### Assistant:"
    
    payload = {
        "model": "facebook/opt-125m",
        "prompt": formatted_prompt,
        "max_tokens": 128,
        "temperature": 0.9,
        "repetition_penalty": 1.1
    }

    try:
        response = requests.post(VLLM_API_URL, json=payload, timeout=60)
        response.raise_for_status() 
        llm_response = response.json()
        output_text = llm_response['choices'][0]['text']

        conn = get_db_connection()
        conn.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)',
                     (session_id, 'assistant', output_text))
        conn.commit()
        conn.close()

        return jsonify({"response": output_text, "session_id": session_id})
    
    except requests.exceptions.RequestException as e:
        print(f"API request to vLLM failed: {e}")
        return jsonify({"error": f"Failed to connect to the LLM backend."}), 500

if __name__ == '__main__':
    app.run(debug=True)