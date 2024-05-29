from flask import Flask, request, render_template
import logging
import re

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='error.log', level=logging.DEBUG)

# Define a class for storing messages
class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content

# Create an empty list to store messages
messages = []

# Advanced Context Manager
class ContextManager:
    def __init__(self):
        self.context = {}

    def update_context(self, key, value):
        self.context[key] = value

    def get_context(self, key):
        return self.context.get(key, None)

    def clear_context(self, key):
        if key in self.context:
            del self.context[key]
# Sentiment Analysis
def analyze_sentiment(text):
    positive_keywords = ["good", "great", "fantastic", "amazing", "happy", "wonderful"]
    negative_keywords = ["bad", "terrible", "awful", "sad", "depressing", "unhappy"]

    text = text.lower()
    if any(word in text for word in positive_keywords):
        return "positive"
    elif any(word in text for word in negative_keywords):
        return "negative"
    else:
        return "neutral"

# Advanced Chatbot Response Logic
def chatbot_response(user_input, context_manager):
    user_input = user_input.lower()

    # Greet user by name if known
    user_name = context_manager.get_context("user_name")
    if user_name:
        if re.search(r"how are you", user_input):
            return f"I'm doing well, {user_name}! How can I assist you today?"

    # Handle name introduction
    if re.search(r"my name is (\w+)", user_input):
        name = re.findall(r"my name is (\w+)", user_input)[0]
        context_manager.update_context("user_name", name)
        return f"Nice to meet you, {name}!"

    # Remember user's favorite color (Example of context usage)
    if re.search(r"my favorite color is (\w+)", user_input):
        color = re.findall(r"my favorite color is (\w+)", user_input)[0]
        context_manager.update_context("favorite_color", color)
        return f"{color.capitalize()} is a beautiful color! I'll remember that."

    # Retrieve favorite color if asked
    if re.search(r"what is my favorite color", user_input):
        color = context_manager.get_context("favorite_color")
        if color:
            return f"Your favorite color is {color.capitalize()}."
        else:
            return "I don't know your favorite color yet. You can tell me by saying 'my favorite color is [color]'."

    # Handle multi-turn conversations
    if context_manager.get_context("topic") == "Weather":
        weather_data = get_weather(user_input)
        context_manager.clear_context("topic")
        return weather_data

    # Handle interactive elements
    if re.search(r"get weather", user_input):
        context_manager.update_context("topic", "Weather")
        return "Sure! Please enter the city for which you want to know the weather."

    # Handle common questions and responses
    responses = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What can I do for you?",
        "how are you": "I'm just a program, but I'm here to help you!",
        "bye": "Goodbye! Have a nice day!",
        "what is your name": "I am a simple AI chatbot created to assist you.",
        "what can you do": "I can chat with you, answer basic questions, and provide information!",
        "who created you": "I was created by a developer using Python.",
        "what is the capital of france": "The capital of France is Paris.",
        "what is the capital of germany": "The capital of Germany is Berlin."
    }

    # Personalized responses
    user_name = context_manager.get_context("user_name")
    if user_name:
        return f"Hello, {user_name}! How can I assist you today?"

    # Sentiment analysis
    sentiment = analyze_sentiment(user_input)
    if sentiment == "positive":
        return "I'm glad to hear that! How can I assist you further?"
    elif sentiment == "negative":
        return "I'm sorry to hear that. How can I help you?"

    # Get the response from predefined responses or default message
    return responses.get(user_input, "I don't understand that. Can you rephrase?")

# Initialize context manager
context_manager = ContextManager()

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            user_input = request.form["user_input"]
            bot_response = chatbot_response(user_input, context_manager)
            # Add user input and bot response to messages list
            messages.append(Message(sender="user", content=user_input))
            messages.append(Message(sender="bot", content=bot_response))
            return render_template("index.html", messages=messages)
        return render_template("index.html", messages=messages)
    except Exception as e:
        logging.exception("Exception occurred")
        return "An error occurred, please try again later."

if __name__ == "__main__":
    app.run(debug=True)
