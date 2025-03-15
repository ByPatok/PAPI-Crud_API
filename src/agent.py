import requests
import json
from typing import List, Optional, Callable
from openai import OpenAI

# API base URL
BASE_URL = "http://127.0.0.1:8000"

# Define functions that the agent can call to interact with the API
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

class Agent:
    def __init__(self, callback: Callable[[str], None] = None):
        """
        Initialize the agent
        
        Args:
            callback: Optional function to call with response text updates
        """
        self.client = OpenAI(
            base_url="http://localhost:1234/v1",  # Default LM Studio server address
            api_key="openthinker-7b"  # LM Studio doesn't require an actual API key locally
        )
        self.callback = callback
        
    def process_query(self, query: str) -> str:

        try:
            messages = [{"role": "user", "content": query}]
            response = self.client.chat.completions.create(
                model="local-model",  # ignored by LM Studio but required
                messages=messages,
                tools=function_definitions,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # Check if the model wants to call a function using standard OpenAI format
            if message.tool_calls:
                results = []
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    # Call the function
                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        function_response = function_to_call(**function_args)
                        
                        # Format the result
                        results.append(f"Result from {function_name}:\n{json.dumps(function_response, indent=2)}")
                    else:
                        results.append(f"Error: Function {function_name} not found")
                
                return "\n\n".join(results)
            else:
                # Alternative: Check for XML-style function calls in the content
                content = message.content if message.content else ""
                if "<call>" in content and "</call>" in content:
                    # Extract function call information from XML format
                    call_start = content.find("<call>") + len("<call>")
                    call_end = content.find("</call>")
                    call_content = content[call_start:call_end].strip()
                    
                    try:
                        # Parse the function call JSON
                        call_data = json.loads(call_content)
                        function_name = call_data.get("name")
                        function_args = call_data.get("arguments", {})
                        
                        # Call the function
                        if function_name in available_functions:
                            function_to_call = available_functions[function_name]
                            function_response = function_to_call(**function_args)
                            
                            # If the content has text before/after the function call, include it
                            result = f"I called {function_name} for you. Here are the results:\n\n"
                            result += json.dumps(function_response, indent=2)
                            return result
                        else:
                            return f"Error: Function {function_name} not found"
                    except json.JSONDecodeError:
                        # If JSON parsing fails, return the original content
                        return content
                
                # The model didn't call a function, just return the response
                return content if content else "No response from assistant"
                    
        except Exception as e:
            return f"Error: {str(e)}"