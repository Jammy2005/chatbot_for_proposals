# chat/views.py
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_utils import create_graph
from .models import ChatSession
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Create your chatbot graph (this is the same as your previous integration)
graph = create_graph()

def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        if not user_input:
            return JsonResponse({"error": "No message provided."}, status=400)

        # Load or initialize the conversation from the session.
        conversation = request.session.get("conversation")
        if not conversation:
            conversation = [{"role": "system", "content": "You are a helpful assistant!"}]

        # Append the user's message.
        conversation.append({"role": "user", "content": user_input})

        # Convert conversation to proper message objects.
        messages = []
        for msg in conversation:
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        # Use a thread id from session or generate a new one.
        thread_id = request.session.get("thread_id")
        if not thread_id:
            thread_id = str(uuid.uuid4())
            request.session["thread_id"] = thread_id

        # Set the config with the current thread_id.
        config = {"configurable": {"thread_id": thread_id}}

        # Get the response from GPT-4 via your graph (streaming the response).
        response_text = ""
        for data, stream_mode in graph.stream({"messages": messages}, config=config, stream_mode="messages"):
            if data.type == "AIMessageChunk":
                response_text += data.content

        # Append the assistant's response.
        conversation.append({"role": "assistant", "content": response_text})
        request.session["conversation"] = conversation

        return JsonResponse({"response": response_text})
    else:
        # GET request: load the chat page with a list of previous conversations.
        previous_chats = ChatSession.objects.order_by('-created_at')
        return render(request, "chat/chat.html", {"previous_chats": previous_chats})


def new_conversation(request):
    """
    Saves the current conversation (if any) and resets session data for a new chat.
    """
    if request.method == "POST":
        conversation = request.session.get("conversation")
        thread_id = request.session.get("thread_id")
        if conversation and thread_id:
            # Save the current conversation into the DB.
            ChatSession.objects.create(thread_id=thread_id, conversation=conversation)
        # Reset the conversation in the session with a new system prompt.
        request.session["conversation"] = [{"role": "system", "content": "You are a helpful assistant!"}]
        new_thread_id = str(uuid.uuid4())
        request.session["thread_id"] = new_thread_id
        return JsonResponse({"status": "new conversation started", "thread_id": new_thread_id})
    return JsonResponse({"error": "POST request required."}, status=400)


def load_conversation(request, thread_id):
    """
    Loads a previously saved conversation into the session.
    """
    if request.method == "POST":
        try:
            chat_session = ChatSession.objects.get(thread_id=thread_id)
            request.session["conversation"] = chat_session.conversation
            request.session["thread_id"] = chat_session.thread_id
            return JsonResponse({"status": "conversation loaded"})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Conversation not found."}, status=404)
    return JsonResponse({"error": "POST request required."}, status=400)
