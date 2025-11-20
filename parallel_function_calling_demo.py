import os
import json
from openai import AzureOpenAI
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint="<your-endpoint>",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="<your-api-version>"
)

# Provide the model deployment name you want to use for this example

deployment_name = "<your-deployment-name>" 

# Simplified weather data
WEATHER_DATA = {
    "tokyo": {"temperature": "10", "unit": "celsius"},
    "san francisco": {"temperature": "72", "unit": "fahrenheit"},
    "paris": {"temperature": "22", "unit": "celsius"}
}

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris"
}

def get_current_weather(location, unit=None):
    """Get the current weather for a given location"""
    location_lower = location.lower()
    print(f"get_current_weather called with location: {location}, unit: {unit}")  
    
    for key in WEATHER_DATA:
        if key in location_lower:
            print(f"Weather data found for {key}")  
            weather = WEATHER_DATA[key]
            return json.dumps({
                "location": location,
                "temperature": weather["temperature"],
                "unit": unit if unit else weather["unit"]
            })
    
    print(f"No weather data found for {location_lower}")  
    return json.dumps({"location": location, "temperature": "unknown"})

def get_current_time(location):
    """Get the current time for a given location"""
    print(f"get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            print(f"Timezone found for {key}")  
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    messages = [{"role": "user", "content": "What's the weather and current time in San Francisco, Tokyo, and Paris?"}]

    # Define the functions for the model (freeform calling style)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location. Call with location name and optionally temperature unit (celsius or fahrenheit).",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": True
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location. Call with location name.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": True
                },
            }
        }
    ]

    # First API call: Ask the model to use the functions
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    print("Model's response:")  
    print(response_message)  

    # Handle function calls (freeform parsing)
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"Function call: {function_name}")  
            print(f"Function arguments (freeform): {function_args}")  
            
            if function_name == "get_current_weather":
                # Extract location from any key that might contain it
                location = function_args.get("location") or function_args.get("city") or function_args.get("place") or list(function_args.values())[0] if function_args else None
                unit = function_args.get("unit") or function_args.get("temperature_unit") or function_args.get("temp_unit")
                function_response = get_current_weather(location=location, unit=unit)
            elif function_name == "get_current_time":
                # Extract location from any key that might contain it
                location = function_args.get("location") or function_args.get("city") or function_args.get("place") or list(function_args.values())[0] if function_args else None
                function_response = get_current_time(location=location)
            else:
                function_response = json.dumps({"error": "Unknown function"})
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content

# Run the conversation and print the result
print(run_conversation())