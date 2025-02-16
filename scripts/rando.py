import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file or environment variables.")

client = openai.OpenAI(api_key=api_key)

import re
import re
import json

import openai
import json
import openai
import json

def multiply(a, b):
    """Performs multiplication of two numbers."""
    return a * b

def query_openai(prompt):
    """Makes an API call to OpenAI and retrieves the response."""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. If the user asks for a multiplication problem, extract the numbers and respond in JSON format: {\"action\": \"use_multiplication_tool\", \"num1\": X, \"num2\": Y}"},
            {"role": "user", "content": prompt}
        ]
    )
    
    try:
        response_json = json.loads(response.choices[0].message.content.strip())
        return response_json  # Return parsed JSON
    except json.JSONDecodeError:
        return {"action": "fallback", "message": response.choices[0].message.content.strip()}

def format_result_with_llm(result):
    """Sends the multiplication result back to the LLM for formatting."""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a formatting assistant. Given a numerical result, format it nicely as a sentence."},
            {"role": "user", "content": f"Format this result nicely: {result}"}
        ]
    )
    return response.choices[0].message.content.strip()

def process_query(user_input):
    """Determines whether to use the multiplication tool or call OpenAI."""
    response_data = query_openai(user_input)
    
    if response_data.get("action") == "use_multiplication_tool":
        num1 = response_data.get("num1")
        num2 = response_data.get("num2")
        if isinstance(num1, (int, float)) and isinstance(num2, (int, float)):
            result = multiply(num1, num2)
            formatted_result = format_result_with_llm(result)
            return formatted_result
        return "Error: Could not extract valid numbers for multiplication."
    
    return response_data.get("message", "Unexpected response format.")

if __name__ == "__main__":
    while True:
        user_input = input("Ask a question (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        print("Response:", process_query(user_input))
