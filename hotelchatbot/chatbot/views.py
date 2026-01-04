from django.shortcuts import render
from .chatbot_nlp import get_response
from datetime import datetime

chat_history = []

def chatbot_view(request):
    global chat_history
    if request.method == "POST":
        user_input = request.POST.get("message")
        bot_reply = get_response(user_input)

        chat_history.append({
            "user": user_input,
            "time": datetime.now().strftime("%H:%M"),
            "bot": bot_reply,
            "bot_time": datetime.now().strftime("%H:%M")
        })

    elif not chat_history:
        chat_history.append({
            "bot": "Hello! How can I assist you today?",
            "bot_time": datetime.now().strftime("%H:%M")
        })

    return render(request, "chatbot.html", {"chat_history": chat_history})
