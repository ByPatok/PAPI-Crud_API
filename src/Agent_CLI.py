import requests
import json
import os
from typing import List, Optional
from openai import OpenAI

# API base URL
BASE_URL = "http://127.0.0.1:8000"

# Define functions that the agent can call to interact with your API
def list_items():
    """Get all items from the API"""
    response = requests.get(f"{BASE_URL}/items")
    return response.json()

def get_item(item_id: int):
    """Get a specific item by ID"""
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    return response.json()

def create_item(nome: str, idade: int):
    """Create a new item"""
    data = {"nome": nome, "idade": idade}
    response = requests.post(f"{BASE_URL}/items", json=data)
    return response.json()

def update_item(item_id: int, nome: Optional[str] = None, idade: Optional[int] = None):
    """Update an existing item"""
    data = {}
    if nome is not None:
        data["nome"] = nome
    if idade is not None:
        data["idade"] = idade
    
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=data)
    return response.json()

def delete_item(item_id: int):
    """Delete an item"""
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    return response.json()

# Define function schemas for the AI to use
function_definitions = [
    {
        "type": "function",
        "function": {
            "name": "list_items",
            "description": "Get all items from the database",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_item",
            "description": "Get a specific item by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "integer", "description": "The ID of the item to retrieve"}
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_item",
            "description": "Create a new item",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "description": "The name of the item"},
                    "idade": {"type": "integer", "description": "The age value"}
                },
                "required": ["nome", "idade"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_item",
            "description": "Update an existing item",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "integer", "description": "The ID of the item to update"},
                    "nome": {"type": "string", "description": "The new name (optional)"},
                    "idade": {"type": "integer", "description": "The new age (optional)"}
                },
                "required": ["item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_item",
            "description": "Delete an item",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_id": {"type": "integer", "description": "The ID of the item to delete"}
                },
                "required": ["item_id"]
            }
        }
    }
]

# Dictionary mapping function names to actual functions
available_functions = {
    "list_items": list_items,
    "get_item": get_item,
    "create_item": create_item,
    "update_item": update_item,
    "delete_item": delete_item
}

def main():
    # Initialize OpenAI client to connect to LM Studio
    client = OpenAI(
        base_url="http://localhost:1234/v1",  # Default LM Studio server address
        api_key="openthinker-7b"  # LM Studio doesn't require an API key locally
    )
    
    print("AI Assistant Ready! Type 'exit' to quit.")
    print("Example commands:")
    print("- Show me all items in the database")
    print("- Create a new item with name John and age 25")
    print("- Update item 1 with name Mary")
    print("- Delete item with ID 3")
    
    while True:
        # Get user input
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break
        
        # Call the LLM with function calling
        try:
            messages = [{"role": "user", "content": user_input}]
            response = client.chat.completions.create(
                model="local-model",  # This is ignored by LM Studio but required by the client
                messages=messages,
                tools=function_definitions,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # Check if the model wants to call a function
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the function
                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        function_response = function_to_call(**function_args)
                        
                        # Display the result
                        print(f"\nAI Assistant (using {function_name}):")
                        print(json.dumps(function_response, indent=2))
                    else:
                        print(f"\nError: Function {function_name} not found")
            else:
                # The model didn't call a function, just display the response
                print(f"\nAI Assistant: {message.content}")
                
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()