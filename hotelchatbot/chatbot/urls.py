from django.urls import path
from . import views
urlpatterns = [
     path('', views.chatbot_view, name='chatbot'),  
    path('get-response/', views.chatbot_view, name='get_chat_response'),
]
