# Local vLLM Chat Application

A simple, full-stack chat application that uses a local Large Language Model (LLM) for real-time conversation. This project demonstrates how to set up a powerful LLM backend with **vLLM** and connect it to a web frontend. It features a key **conversation memory** system using a SQLite database.

## ✨ Features

  * **Local LLM Inference**: Runs an LLM locally on your GPU, ensuring data privacy and fast responses without external APIs.
  * **Conversation Memory**: Implements a chat history system using a **SQLite database**, allowing the LLM to remember previous messages and maintain context throughout a single session.
  * **Simple Web Interface**: A clean and minimal chat UI built with HTML, CSS, and JavaScript.
  * **Python Backend**: A Flask server to manage API requests between the frontend and the vLLM backend.

## 🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites

  * **Python 3.8+**
  * A **NVIDIA GPU** with sufficient VRAM to run the model.
  * **pip**

### Installation

1.  Clone this repository:

    ```bash
    git clone https://github.com/sh4shv4t/vllmproject
    cd vllmproject
    ```

2.  Install the required Python packages for the backend:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

This project requires two separate components to run simultaneously: the vLLM server and the Flask backend.

#### Step 1: Start the vLLM Server

In your first terminal, start the vLLM server. This command will download and load the `facebook/opt-125m` model onto your GPU. The `--gpu-memory-utilization` flag is crucial to prevent out-of-memory errors.

```bash
python -m vllm.entrypoints.openai.api_server --model facebook/opt-125m --gpu-memory-utilization 0.7
```

You can change the model as per your requirements.

Wait for the server to finish loading the model and show a message like `Uvicorn running on http://0.0.0.0:8000`.

#### Step 2: Start the Flask Backend

In a **new** terminal, start the Flask server. This server connects the frontend to vLLM and manages the chat history in the `chat_history.db` file.

```bash
python app.py
```

You should see a message indicating the server is running on `http://127.0.0.1:5000`.

## 🌐 Usage

Open your web browser and navigate to `http://127.0.0.1:5000`. You can now start chatting with your local LLM. The conversation history will be stored in the `chat_history.db` file.

## 🧠 Memory Implementation

This project uses a simple, yet effective, method for conversational memory:

1.  **Database Storage**: Each user and assistant message is saved to a **SQLite database** with a unique `session_id`.
2.  **Contextual Prompting**: For every new message, the Flask backend retrieves all previous messages for that session from the database.
3.  **LLM Input**: The entire conversation history is then formatted into a single string and passed as the `prompt` to the vLLM. This gives the model the full context needed to generate a relevant response, creating the illusion of memory.

## 🔧 Project Structure

```
.
├── app.py          # Flask backend, handles API logic and database interactions.
├── requirements.txt  # Python dependencies.
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── templates/
    └── index.html
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! Please reach out to me as I am currently still in the process of setting this project up.