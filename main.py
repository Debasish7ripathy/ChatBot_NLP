from flask import Flask, render_template, request
import spacy
from spacy.matcher import Matcher
import datetime

app = Flask(__name__)

def get_greeting_response(time_of_day):
    """Returns a greeting response based on the time of day."""
    if 5 <= time_of_day.hour < 12:
        return "Good morning!"
    elif 12 <= time_of_day.hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

current_date = datetime.datetime.now().date()
current_time = datetime.datetime.now()

patterns = [
    {"label": "greeting", "pattern": [{"LOWER": "hi"}, {"LOWER": "there"}]},
    {"label": "greeting", "pattern": [{"LOWER": "hello"}]},
    {"label": "greeting", "pattern": [{"LOWER": "hey"}]},
    {"label": "greeting", "pattern": [{"LOWER": "howdy"}]},
    {"label": "greeting", "pattern": [{"LOWER": "hiya"}]},
    {"label": "greeting", "pattern": [{"LOWER": "what's"}, {"LOWER": "up"}]},
    {"label": "greeting", "pattern": [{"LOWER": "good"}, {"LOWER": "morning"}]},
    {"label": "greeting", "pattern": [{"LOWER": "good"}, {"LOWER": "afternoon"}]},
    {"label": "greeting", "pattern": [{"LOWER": "good"}, {"LOWER": "evening"}]},
    {"label": "goodbye", "pattern": [{"LOWER": "bye"}]},
    {"label": "goodbye", "pattern": [{"LOWER": "see"}, {"LOWER": "you"}]},
    {"label": "goodbye", "pattern": [{"LOWER": "goodbye"}]},
    {"label": "goodbye", "pattern": [{"LOWER": "farewell"}]},
    {"label": "goodbye", "pattern": [{"LOWER": "take"}, {"LOWER": "care"}]},
    {"label": "name", "pattern": [{"POS": "PROPN"}]},
    {"label": "time", "pattern": [{"LOWER": "time"}]},
    {"label": "date", "pattern": [{"LOWER": "date"}]},
    {"label": "news", "pattern": [{"LOWER": "news"}]},
    {"label": "joke", "pattern": [{"LOWER": "joke"}]},
    {"label": "joke", "pattern": [{"LOWER": "funny"}, {"LOWER": "joke"}]},
    {"label": "joke", "pattern": [{"LOWER": "tell"}, {"LOWER": "me"}, {"LOWER": "a"}, {"LOWER": "joke"}]},
    {"label": "joke", "pattern": [{"LOWER": "humor"}, {"LOWER": "me"}]},
    {"label": "joke", "pattern": [{"LOWER": "amuse"}, {"LOWER": "me"}]},
    {"label": "help", "pattern": [{"LOWER": "help"}]},
    {"label": "help", "pattern": [{"LOWER": "how"}, {"LOWER": "to"}, {"LOWER": "use"}]},
    {"label": "help", "pattern": [{"LOWER": "instructions"}]},
    {"label": "help", "pattern": [{"LOWER": "assist"}]},
    {"label": "help", "pattern": [{"LOWER": "guide"}]},
    {"label": "thanks", "pattern": [{"LOWER": "thanks"}, {"LOWER": "a"}, {"LOWER": "lot"}]},
    {"label": "thanks", "pattern": [{"LOWER": "thank"}, {"LOWER": "you"}]},
    {"label": "thanks", "pattern": [{"LOWER": "thanks"}]},
    {"label": "emotion", "pattern": [{"LOWER": "happy"}]},
    {"label": "emotion", "pattern": [{"LOWER": "sad"}]},
    {"label": "emotion", "pattern": [{"LOWER": "angry"}]},
    {"label": "emotion", "pattern": [{"LOWER": "excited"}]},
    {"label": "emotion", "pattern": [{"LOWER": "depressed"}]},
    {"label": "emotion", "pattern": [{"LOWER": "bored"}]},
    {"label": "age", "pattern": [{"LOWER": "how"}, {"LOWER": "old"}, {"LOWER": "are"}, {"LOWER": "you"}]},
    {"label": "age", "pattern": [{"LOWER": "what"}, {"LOWER": "is"}, {"LOWER": "your"}, {"LOWER": "age"}]},
    {"label": "age", "pattern": [{"LOWER": "age"}, {"LOWER": "of"}, {"LOWER": "chatbot"}]},
    {"label": "owner", "pattern": [{"LOWER": "owner"}]},
    {"label": "owner", "pattern": [{"LOWER": "who"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "owner"}]},
    {"label": "owner", "pattern": [{"LOWER": "who"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "owner"}, {"LOWER": "of"}, {"LOWER": "chatbot"}]},
    {"label": "weather", "pattern": [{"LOWER": "weather"}]},
    {"label": "weather", "pattern": [{"LOWER": "what"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "weather"}]},
    {"label": "weather", "pattern": [{"LOWER": "what"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "weather"}, {"LOWER": "like"}]},
    {"label": "weather", "pattern": [{"LOWER": "weather"}, {"LOWER": "of"}]},
]

responses = {
    "greeting": ["Hello!", "Hi!", "Hey!", "Howdy!", "Hiya!", "What's up?", "Good morning!", "Good afternoon!", "Good evening!"],
    "goodbye": ["Goodbye!", "See you later!", "Farewell!", "Take care!"],
    "name": ["I'm a chatbot.", "You can call me a chatbot."],
    "time": ["The current time is " + current_time.strftime("%H:%M"), "It's currently " + current_time.strftime("%H:%M")],
    "date": ["Today's date is " + current_date.strftime("%d-%m-%Y"), "The date today is " + current_date.strftime("%d-%m-%Y")],
    "news": ["I'm sorry, I'm just a chatbot and I don't have access to news information.", "For the latest news, you can check news websites or apps."],
    "joke": ["Why don't scientists trust atoms? Because they make up everything!", "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!"],
    "help": ["How can I assist you?", "I'm here to help. What do you need assistance with?"],
    "emotion": ["I'm just a chatbot, so I don't experience emotions like humans do.", "I'm programmed to assist you, regardless of my emotions."],
    "age": ["I'm just a chatbot. I don't have an age.", "I don't have an age. I'm here to assist you!"],
    "thanks": ["You're welcome!", "No problem!", "My pleasure!"],
    "owner": ["Lord Debasish Tripathy is the owner of this chatbot."],
    "weather": ["I'm sorry, I'm just a chatbot and I don't have access to weather information.", "For the latest weather, you can check weather websites or apps."],
}
patterns.extend([
    {"label": "location", "pattern": [{"LOWER": "location"}]},
    {"label": "location", "pattern": [{"LOWER": "where"}, {"LOWER": "are"}, {"LOWER": "you"}]},
    {"label": "location", "pattern": [{"LOWER": "where"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "live"}]},
    {"label": "location", "pattern": [{"LOWER": "where"}, {"LOWER": "are"}, {"LOWER": "you"}, {"LOWER": "from"}]},
    {"label": "location", "pattern": [{"LOWER": "where"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "come"}, {"LOWER": "from"}]},
    {"label": "location", "pattern": [{"LOWER": "place"}, {"LOWER": "are"}, {"LOWER": "you"}, {"LOWER": "at"}]},
    {"label": "location", "pattern": [{"LOWER": "place"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "live"}]},
    {"label": "location", "pattern": [{"LOWER": "place"}, {"LOWER": "are"}, {"LOWER": "you"}, {"LOWER": "from"}]},
    {"label": "location", "pattern": [{"LOWER": "place"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "come"}, {"LOWER": "from"}]},
    {"label": "music", "pattern": [{"LOWER": "music"}]},
    {"label": "music", "pattern": [{"LOWER": "what"}, {"LOWER": "music"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "like"}]},
    {"label": "music", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "listen"}, {"LOWER": "to"}, {"LOWER": "music"}]},
    {"label": "music", "pattern": [{"LOWER": "favorite"}, {"LOWER": "music"}]},
    {"label": "music", "pattern": [{"LOWER": "music"}, {"LOWER": "genre"}]},
    {"label": "music", "pattern": [{"LOWER": "what"}, {"LOWER": "kind"}, {"LOWER": "of"}, {"LOWER": "music"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "like"}]},
    {"label": "programming", "pattern": [{"LOWER": "programming"}]},
    {"label": "programming", "pattern": [{"LOWER": "what"}, {"LOWER": "programming"}, {"LOWER": "language"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "code"}]},
    {"label": "programming", "pattern": [{"LOWER": "favorite"}, {"LOWER": "programming"}, {"LOWER": "language"}]},
    {"label": "programming", "pattern": [{"LOWER": "what"}, {"LOWER": "language"}, {"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "code"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}, {"LOWER": "python"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}, {"LOWER": "java"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}, {"LOWER": "c++"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}, {"LOWER": "javascript"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}, {"LOWER": "html"}]},
    {"label": "programming", "pattern": [{"LOWER": "do"}, {"LOWER": "you"}, {"LOWER": "know"}, {"LOWER": "css"}]},
    {"label": "master", "pattern": [{"LOWER": "master"}]},
    {"label": "master", "pattern": [{"LOWER": "who"}, {"LOWER": "is"}, {"LOWER": "the"}, {"LOWER": "master"}, {"LOWER": "of"}, {"LOWER": "chatbot"}]},
    {"label": "how are you", "pattern": [{"LOWER": "how"}, {"LOWER": "are"}, {"LOWER": "you"}]},
    {"label": "how are you", "pattern": [{"LOWER": "how"}, {"LOWER": "are"}, {"LOWER": "you"}, {"LOWER": "doing"}]},
    {"label": "you", "pattern": [{"LOWER": "you"}]},
    {"label": "you", "pattern": [{"LOWER": "you"}, {"LOWER": "are"}]},
    {"label": "you", "pattern": [{"LOWER": "you"}, {"LOWER": "want"}]},
    {"label": "you", "pattern": [{"LOWER": "you"}, {"LOWER": "want"}, {"LOWER": "to"}]},
    {"label": "you", "pattern": [{"LOWER": "you"}, {"LOWER": "want"}, {"LOWER": "to"}, {"LOWER": "do"}]},
    {"label": "you", "pattern": [{"LOWER": "you"}, {"LOWER": "want"}, {"LOWER": "to"}, {"LOWER": "learn"}]},
    {"label": "fine", "pattern": [{"LOWER": "fine", "OP": "+"}, {"LOWER": "thank", "OP": "+"}, {"LOWER": "you", "OP": "+"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank", "OP": "+"}, {"LOWER": "you", "OP": "+"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank", "OP": "+"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank"}, {"LOWER": "you"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank"}, {"LOWER": "you"}, {"LOWER": "for"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank"}, {"LOWER": "you"}, {"LOWER": "for"}, {"LOWER": "the"}, {"LOWER": "service"}]},
    {"label": "fine", "pattern": [{"LOWER": "thank"}, {"LOWER": "you"}, {"LOWER": "for"}, {"LOWER": "the"}, {"LOWER": "help"}]},
])

responses.update({
    "location": ["I exist in the virtual world!", "I don't have a physical location, I'm just a program running on a server."],
    "music": ["I don't have ears to listen to music, but I can recommend some tunes!", "I enjoy listening to the sound of code executing."],
    "programming": ["I'm fluent in the language of Python, but I can understand some other languages too!", "I speak the language of programming. Python is my favorite dialect."],
    "master": ["I'm the master of the virtual world!"],
    "how are you": ["I'm doing well! How about you?"],
    "you": ["I'm fine! How are you?"],
    "fine": ["I'm oni-chan's assistant. How can I help you?", "I'm oni-chan's chatbot. How are you?"]
})


nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

for pattern in patterns:
    matcher.add(pattern["label"], [pattern["pattern"]])

def chat(user_input):
    """Processes user input and returns a response."""
    doc = nlp(user_input)
    matches = matcher(doc)
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        return responses[label][0]
    return "Sorry, I didn't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chatbot():
    user_input = request.form["user_input"]
    response = chat(user_input)
    return response

if __name__ == "__main__":
    app.run(debug=True)
