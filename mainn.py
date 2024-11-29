import os
import asyncio
import websockets
import json
import datetime
import requests
from hardware_main import mainx
from google.generativeai import GenerativeModel, configure

# Function to set up the chatbot
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


# Function to get weather info
def get_weather(city_name=""):
    if not city_name:
        try:
            loc_res = requests.get("http://ipinfo.io/json")
            loc_res.raise_for_status()
            city_name = loc_res.json().get("city", "your location")
        except requests.RequestException:
            return "Could not retrieve your location."
    try:
        weather_res = requests.get(f"http://wttr.in/{city_name}?format=%t")
        weather_res.raise_for_status()
        temperature = weather_res.text.strip().replace("+", "")
        return f"The temperature in {city_name} is {temperature}."
    except requests.RequestException:
        return "Unable to retrieve weather data."


# WebSocket server handler
async def handle_connection(websocket, path):
    print("Client connected")
    initial_message = {"type": "welcome", "content": "Welcome to the WebSocket server!"}
    await websocket.send(json.dumps(initial_message))
    
    chat_session = setup_chatbot()
    try:
        async for message in websocket:
            print(f"Received: {message}")
            data = json.loads(message)
            if data.get("type") == "text":
                query = data.get("content", "").strip()
                print(f"Query received from client: {query}")

                if query.lower() == "exit":
                    response = {"type": "response", "content": "Exiting... Goodbye!"}
                    await websocket.send(json.dumps(response))
                    break

                # Menu handling
                if query == "1":
                    while True:
                        response_prompt = {"type": "prompt", "content": "Send a query or type 'exit' to quit."}
                        await websocket.send(json.dumps(response_prompt))
                        message = await websocket.recv()
                        next_data = json.loads(message)
                        next_query = next_data.get("content", "").strip()

                        if next_query.lower() == "exit":
                            response = {"type": "response", "content": "Session ended. Goodbye!"}
                            await websocket.send(json.dumps(response))
                            break

                        response_content = chat_session.send_message(next_query).text
                        response = {"type": "response", "content": response_content}
                        await websocket.send(json.dumps(response))

                elif query == "2":
                    mainx()
                    response = {"type": "response", "content": "Home assistance executed."}
                    await websocket.send(json.dumps(response))

                elif query == "3":
                    city = "current location"
                    weather = get_weather(city)
                    response = {"type": "response", "content": weather}
                    await websocket.send(json.dumps(response))

                else:
                    response = {"type": "response", "content": "Invalid choice. Please try again."}
                    await websocket.send(json.dumps(response))

    except websockets.ConnectionClosed:
        print("Client disconnected")


# Main function to start the WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever


# Run the server
if __name__ == "__main__":
    asyncio.run(main())
