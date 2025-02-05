# chat/views.py
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_utils import create_graph
from .models import ChatSession
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

graph = create_graph()

def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        if not user_input:
            return JsonResponse({"error": "No message provided."}, status=400)
        # Retrieve or initialize conversation in session.
        conversation = request.session.get("conversation")
        if not conversation:
            conversation = [{"role": "system", "content": "You are a helpful assistant!"}]
        conversation.append({"role": "user", "content": user_input})
        
        # Convert conversation to message objects.
        messages = []
        for msg in conversation:
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        thread_id = request.session.get("thread_id")
        if not thread_id:
            thread_id = str(uuid.uuid4())
            request.session["thread_id"] = thread_id
        
        config = {"configurable": {"thread_id": thread_id}}
        
        response_text = ""
        for data, stream_mode in graph.stream({"messages": messages}, config=config, stream_mode="messages"):
            if data.type == "AIMessageChunk":
                response_text += data.content
        
        conversation.append({"role": "assistant", "content": response_text})
        request.session["conversation"] = conversation
        
        return JsonResponse({"response": response_text})
    else:
        # GET request: pass previous chats and current conversation (if any).
        previous_chats = ChatSession.objects.order_by('-created_at')
        current_convo = request.session.get("conversation", [])
        return render(request, "chat/chat.html", {"previous_chats": previous_chats, "current_convo": current_convo})

def new_conversation(request):
    """
    Saves the current conversation (even if empty) only if it hasn’t been saved yet,
    and then resets session data to start a new conversation.
    Returns JSON including info about the saved conversation so that the sidebar can update.
    """
    if request.method == "POST":
        try:
            # Define the initial conversation state.
            initial_convo = [{"role": "system", "content": "You are a helpful assistant!"}]
            
            # Retrieve the current conversation and thread id from the session.
            conversation = request.session.get("conversation", initial_convo)
            thread_id = request.session.get("thread_id")
            
            saved_data = None
            # Only attempt to save if thread_id exists and there isn't already a ChatSession with that thread_id.
            if thread_id is not None and not ChatSession.objects.filter(thread_id=thread_id).exists():
                chat_session = ChatSession.objects.create(thread_id=thread_id, conversation=conversation)
                saved_data = {
                    "thread_id": thread_id,
                    "created_at": chat_session.created_at.strftime("%b %d, %Y %H:%M")
                }
            
            # Reset the conversation and generate a new thread ID in the session.
            new_thread_id = str(uuid.uuid4())
            request.session["conversation"] = initial_convo
            request.session["thread_id"] = new_thread_id
            
            return JsonResponse({
                "status": "new conversation started",
                "new_thread_id": new_thread_id,
                "saved": saved_data
            })
        except Exception as e:
            # Print the full traceback to your Django server log for debugging.
            import traceback
            print("Error in new_conversation:", traceback.format_exc())
            return JsonResponse({"error": "Internal server error in new_conversation."}, status=500)
    return JsonResponse({"error": "POST request required."}, status=400)

def load_conversation(request, thread_id):
    """
    Loads a previously saved conversation into the session and returns its content.
    """
    if request.method == "POST":
        try:
            chat_session = ChatSession.objects.get(thread_id=thread_id)
            request.session["conversation"] = chat_session.conversation
            request.session["thread_id"] = chat_session.thread_id
            return JsonResponse({"status": "conversation loaded", "conversation": chat_session.conversation})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Conversation not found."}, status=404)
    return JsonResponse({"error": "POST request required."}, status=400)
