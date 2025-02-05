# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_view, name="chat"),
    path("new_conversation/", views.new_conversation, name="new_conversation"),
    path("load_conversation/<str:thread_id>/", views.load_conversation, name="load_conversation"),
]
