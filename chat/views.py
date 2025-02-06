import uuid
from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_utils import create_graph
from .models import ChatSession
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from django.utils import timezone

graph = create_graph()

def chat_view(request):
    if request.method == "POST":
        # [POST logic unchanged...]
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
        # messages = graph.invoke({"messages": messages},config)
        # response_text = messages['messages'][-1].content
        print(response_text)
        conversation.append({"role": "assistant", "content": response_text})
        request.session["conversation"] = conversation
        
        return JsonResponse({"response": response_text})
    else:
        # GET request: initialize thread_id if missing
        if "thread_id" not in request.session:
            request.session["thread_id"] = str(uuid.uuid4())
        previous_chats = ChatSession.objects.order_by('-created_at')
        current_convo = request.session.get("conversation", [])
        active_chat = request.session.get("active_chat", False)
        return render(request, "chat/chat.html", {
            "previous_chats": previous_chats,
            "current_convo": current_convo,
            "active_chat": active_chat
        })

def new_conversation(request):
    """
    Saves the current conversation (even if it's just the system prompt) and then resets session data
    to start a new conversation. This ensures that every conversation gets a unique chat ID and is accessible
    in the sidebar. The new conversation is also immediately opened.
    """
    if request.method == "POST":
        try:
            # Define the initial conversation state.
            initial_convo = [{"role": "system", "content": "You are a helpful assistant!"}]
            
            # Retrieve current conversation and thread ID from session.
            conversation = request.session.get("conversation", initial_convo)
            thread_id = request.session.get("thread_id")
            
            saved_data = None
            if thread_id:
                # Try to save the conversation only if a ChatSession with this thread_id doesn't exist.
                if not ChatSession.objects.filter(thread_id=thread_id).exists():
                    try:
                        chat_session = ChatSession.objects.create(thread_id=thread_id, conversation=conversation)
                        saved_data = {
                            "thread_id": thread_id,
                            "created_at": chat_session.created_at.strftime("%b %d, %Y %H:%M")
                        }
                    except IntegrityError:
                        # In case of a race condition or duplicate request, retrieve the existing record.
                        chat_session = ChatSession.objects.get(thread_id=thread_id)
                        saved_data = {
                            "thread_id": thread_id,
                            "created_at": chat_session.created_at.strftime("%b %d, %Y %H:%M")
                        }
            
            # Now, reset the session data to start a new conversation.
            new_thread_id = str(uuid.uuid4())
            request.session["conversation"] = initial_convo
            request.session["thread_id"] = new_thread_id
            request.session["active_chat"] = True  # Mark that a chat is active
            
            new_data = {
                "thread_id": new_thread_id,
                "created_at": timezone.now().strftime("%b %d, %Y %H:%M")
            }
            
            return JsonResponse({
                "status": "new conversation started",
                "saved": saved_data,  # Details of the conversation that was just saved.
                "new": new_data       # Details of the new active conversation.
            })
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print("Error in new_conversation:", error_trace)
            return JsonResponse({
                "error": "Internal server error in new_conversation.",
                "trace": error_trace
            }, status=500)
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
            request.session["active_chat"] = True
            return JsonResponse({"status": "conversation loaded", "conversation": chat_session.conversation})
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Conversation not found."}, status=404)
    return JsonResponse({"error": "POST request required."}, status=400)
