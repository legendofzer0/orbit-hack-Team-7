import asyncio
import websockets
import json
import os
import time
import pyttsx3
import requests
import datetime
import speech_recognition as sr

# WebSocket server handler
async def handle_connection(websocket, path):
    print("Client connected")
    
    # Send an initial message to the client
    initial_message = {"type": "welcome", "content": "Welcome to the WebSocket server!"}
    await websocket.send(json.dumps(initial_message))
    
    try:
        async for message in websocket:
            print(f"Received: {message}")
            data = json.loads(message)

            # Process different message types
            if data.get("type") == "text":
                response = {"type": "response", "content": f"Hello {data['content']}"}
                await websocket.send(json.dumps(response))
            elif data.get("type") == "audio":
                # Handle audio data and send acknowledgment
                with open("received_audio.wav", "wb") as f:
                    f.write(data['content'].encode('latin1'))  # Decode if necessary
                ack = {"type": "audio_ack", "status": "received"}
                await websocket.send(json.dumps(ack))
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # Run indefinitely

# Run the WebSocket server
if __name__ == "__main__":
    asyncio.run(main())
