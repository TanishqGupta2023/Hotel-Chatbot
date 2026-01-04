import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

with open("chatbot/chatbot_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

X = []
y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        X.append(pattern)
        y.append(intent["tag"])


vectorizer = TfidfVectorizer()
X_vectors = vectorizer.fit_transform(X)

model = LinearSVC()
model.fit(X_vectors, y)
with open("chatbot/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("chatbot/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
    X_train, X_test, y_train, y_test = train_test_split(X_vectors, y, test_size=0.2, random_state=42)

model = LinearSVC()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Training completed. Model and vectorizer saved.")
