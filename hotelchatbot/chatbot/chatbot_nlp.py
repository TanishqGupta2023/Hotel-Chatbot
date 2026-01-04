import json
import random
import pickle
import nltk
from nltk.stem import PorterStemmer
import re

nltk.data.path.append("C:/Users/TANISHQ/AppData/Roaming/nltk_data")

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stemmer = PorterStemmer()

with open("chatbot/chatbot_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

with open("chatbot/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("chatbot/model.pkl", "rb") as f:
    model = pickle.load(f)


def tokenize(text):
    return nltk.word_tokenize(text)

def stem(word):
    return stemmer.stem(word.lower())

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[-]', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text

def rule_based_match(message):
    message_words = [stem(word) for word in tokenize(message)]
    best_match = None
    highest_score = 0

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            pattern_words = [stem(word) for word in tokenize(pattern)]
            score = sum(1 for w in pattern_words if w in message_words)
            if score > highest_score:
                highest_score = score
                best_match = intent

    if best_match and highest_score >= 1:
        return random.choice(best_match["responses"])
    return None

def get_response(message):
    try:
        message = preprocess_text(message)
        X = vectorizer.transform([message])
        predicted_tag = model.predict(X)[0]
        confidence = max(model.decision_function(X)[0])

        CONFIDENCE_THRESHOLD = 0.3  
        if confidence >= CONFIDENCE_THRESHOLD:
            for intent in data["intents"]:
                if intent["tag"] == predicted_tag:
                    return random.choice(intent["responses"])
        else:
            return "I'm sorry, I didn't understand that. Could you please rephrase?"

    except Exception as e:
        print("Error:", e)

    fallback_response = rule_based_match(message)
    if fallback_response:
        return fallback_response

    return "I'm sorry, I didn't understand that. Please ask something else."
