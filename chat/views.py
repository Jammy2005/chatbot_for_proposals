from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import JsonResponse
from .chatbot_utils import create_graph
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Create (or reuse) a global graph instance. In a production app, you might manage state differently.
graph = create_graph()

def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message")
        if not user_input:
            return JsonResponse({"error": "No message provided."}, status=400)

        # Retrieve conversation history from the session (initialize if not present)
        conversation = request.session.get("conversation", [])
        if not conversation:
            # Start with a system message prompt
            conversation.append({"role": "system", "content": "You are a helpful assistant!"})

        # Append the user message to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Convert our conversation history into proper message objects
        messages = []
        for msg in conversation:
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        state = {"messages": messages}
        config = {"configurable": {"thread_id": "1"}}

        # Call the graph to process the conversation
        response_text = ""
        for data, stream_mode in graph.stream(state, config=config, stream_mode="messages"):
            if data.type == "AIMessageChunk":
                response_text += data.content

        # Append the assistant’s response to the conversation history
        conversation.append({"role": "assistant", "content": response_text})
        request.session["conversation"] = conversation

        return JsonResponse({"response": response_text})

    else:
        # For GET requests, render the chat interface
        return render(request, "chat/chat.html")

