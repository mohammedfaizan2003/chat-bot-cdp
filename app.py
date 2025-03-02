from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.chat.util import Chat, reflections

app = Flask(__name__, static_folder='static')
CORS(app)

# Basic response handler
responses = {
    "hello": "Hi! How can I help you today?",
    "help": "I can assist with technical documentation!"
}

# Define some question-answer pairs for NLP
pairs = [
    ['hi|hello', ['Hello!', 'Hi there!']],
    ['help', ['I can assist with technical documentation!']],
    ['how are you', ['I am just a bot, but thanks for asking!']],
    ['bye|goodbye', ['Goodbye!', 'See you later!']]
]

def chatbot_response(query):
    # Create a chatbot instance
    chat = Chat(pairs, reflections)
    # Get a response based on the user's query
    return chat.respond(query)

def scrape_docs(url):
    try:
        # Fetch the webpage
        response = requests.get(url)
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all paragraphs and join them into a single string
        return ' '.join([p.text for p in soup.find_all('p')])[:1000]  # Limit to 1000 characters
    except:
        return "Could not retrieve documentation."

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('query', '').lower()
    
    # Check if the user is asking for documentation
    if "documentation" in user_input or "docs" in user_input:
        docs_url = "https://example.com/docs"  # Replace with your actual docs URL
        docs_content = scrape_docs(docs_url)
        return jsonify({"response": docs_content})
    
    # Use the NLP chatbot to generate a response
    response = chatbot_response(user_input)
    
    # If no response from NLP, fallback to default
    if not response:
        response = "I'm still learning. Can you rephrase that?"
    
    return jsonify({"response": response})

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)