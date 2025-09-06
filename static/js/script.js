// Function to handle sending the message
async function sendMessage(event) {
    // Prevent the form from submitting in the traditional way
    event.preventDefault(); 
    
    const promptInput = document.getElementById('prompt-input');
    const userPrompt = promptInput.value.trim();

    if (!userPrompt) return; // Don't send empty messages

    appendMessage('user', userPrompt);
    promptInput.value = ''; // Clear the input field

    // The URL should match your Flask server's endpoint
    const apiEndpoint = 'http://127.0.0.1:5000/ask'; 
    
    try {
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: userPrompt })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const llmResponse = data.response;

        if (llmResponse) {
            appendMessage('bot', llmResponse);
        } else {
            appendMessage('bot', 'An error occurred or no response was received.');
        }
    } catch (error) {
        console.error('Fetch error:', error);
        appendMessage('bot', `Failed to get a response from the server. Error: ${error.message}`);
    }
}

// Function to add a message to the chat window
function appendMessage(sender, text) {
    const chatWindow = document.getElementById('chat-window');
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('message-container', sender);
    
    const messageBox = document.createElement('div');
    messageBox.classList.add('message-box');
    messageBox.textContent = text;
    
    messageContainer.appendChild(messageBox);
    chatWindow.appendChild(messageContainer);
    
    // Scroll to the bottom of the chat window
    chatWindow.scrollTop = chatWindow.scrollHeight;
}