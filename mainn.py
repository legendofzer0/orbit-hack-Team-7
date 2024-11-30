import os
import asyncio
import websockets
import json
import joblib
import requests
from hardware_controll import mainxer
from google.generativeai import GenerativeModel, configure

# Setup the chatbot
def setup_chatbot():
    os.environ["YOUR_API_KEY_VARIABLE"] = "AIzaSyBnD13QcYH59_15GYyFu2MpzukmS8oxy8c"
    configure(api_key=os.environ["YOUR_API_KEY_VARIABLE"])

    model = GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1.75,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
        system_instruction="Your name is Temmer, created to assist in daily human life and control devices.",
    )
    return model.start_chat(history=[])

# WebSocket server handler
async def handle_query(query, chat_session):
    if query in ["1", "chatbot"]:
        response_content = chat_session.send_message("Chatbot started").text
    elif query in ["2", "smart home"]:
        response_content = "Switching to Smart Home Assistant..."
        mainxer()  # Assuming this function does something related to smart home
    elif query in ["3", "weather"]:
        response_content = "Weather feature is under construction."
    else:
        response_content = chat_session.send_message(query).text

    # Prepare the response
    response = {"type": "response", "content": response_content}
    json_response = json.dumps(response)
    print(f"Sending response: {json_response}")
    return json_response

async def handle_message(websocket, message, chat_session):
    print(f"Received: {message}")
    try:
        data = json.loads(message)  # Parse the received JSON message
        query = data.get("content", "").strip()

        if not query:
            print("No valid content received")
            return None  # Return None if no valid content

        print(f"Query received: {query}")
        if query == "exit":
            print("Session closed by client")
            return "exit"  # Special case for exit command

        # Handle the query by calling the separate function
        json_response = await handle_query(query, chat_session)
        return json_response
    except Exception as e:
        print(f"Error processing message: {e}")
        return json.dumps({"type": "error", "content": str(e)})

# Function to handle WebSocket connection
async def handle_connection(websocket, path):
    print("Client connected")
    initial_message = {"type": "welcome", "content": "Welcome to the WebSocket server!"}
    try:
        await websocket.send(json.dumps(initial_message))  # Send initial message to client
        print("Sent welcome message to client")

        chat_session = setup_chatbot()  # Initialize the AI chatbot session

        async for message in websocket:
            # Use handle_message to process incoming messages
            response = await handle_message(websocket, message, chat_session)

            if response == "exit":
                break  # End the session if "exit" command was received

            if response:
                # Send the response to the client
                await websocket.send(response)

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("Client disconnected")
# Function to handle WebSocket connection
# Start the WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
