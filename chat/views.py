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

        conversation = request.session.get("conversation")
        if not conversation:
            conversation = [{"role": "system", "content": "You are a helpful assistant!"}]
        conversation.append({"role": "user", "content": user_input})

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
        # Reset the "saved" flag so that if the user sends more messages before clicking new conversation,
        # the conversation will be unsaved again.
        request.session["conversation_saved"] = False

        return JsonResponse({"response": response_text})
    else:
        previous_chats = ChatSession.objects.order_by('-created_at')
        return render(request, "chat/chat.html", {"previous_chats": previous_chats})

def new_conversation(request):
    """
    Saves the current conversation (if it contains more than the initial system message)
    and then resets session data to start a new conversation.
    """
    if request.method == "POST":
        try:
            # Define the initial conversation state.
            initial_convo = [{"role": "system", "content": "You are a helpful assistant!"}]
            
            # Get the current conversation and thread id from the session.
            conversation = request.session.get("conversation", initial_convo)
            thread_id = request.session.get("thread_id")
            
            saved_data = None
            
            # Save the conversation only if it is different from the initial state.
            if conversation and conversation != initial_convo and thread_id:
                # Check if a ChatSession with this thread_id already exists to avoid duplicates.
                if not ChatSession.objects.filter(thread_id=thread_id).exists():
                    chat_session = ChatSession.objects.create(thread_id=thread_id, conversation=conversation)
                    saved_data = {
                        "thread_id": thread_id,
                        "created_at": chat_session.created_at.strftime("%b %d, %Y %H:%M")
                    }
                else:
                    # Already saved – do nothing.
                    pass
            
            # Now, reset the conversation by generating a new thread_id and setting the conversation to the initial state.
            new_thread_id = str(uuid.uuid4())
            request.session["conversation"] = initial_convo
            request.session["thread_id"] = new_thread_id
            
            return JsonResponse({
                "status": "new conversation started",
                "new_thread_id": new_thread_id,
                "saved": saved_data
            })
        except Exception as e:
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
            # When loading a conversation, consider it unsaved in the session.
            request.session["conversation_saved"] = True
            return JsonResponse({"status": "conversation loaded", "conversation": chat_session.conversation})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Conversation not found."}, status=404)
    return JsonResponse({"error": "POST request required."}, status=400)
