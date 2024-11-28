import asyncio
import websockets
import json

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

            # Send a response based on the received message
            if data.get("type") == "text":
                response = {"type": "response", "content": f"Hello {data['content']}"}
                await websocket.send(json.dumps(response))
            elif data.get("type") == "audio":
                # Handle audio data and send acknowledgment
                with open("received_audio.wav", "wb") as f:
                    f.write(data['content'].encode('latin1'))  # Decode if necessary
                ack = {"type": "audio_ack", "status": "received"}
                await websocket.send(json.dumps(ack))
            
            # Broadcast to all connected clients (optional)
            # await asyncio.gather(*[ws.send(json.dumps(response)) for ws in connected_clients])
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("Web Socket Started")
        await asyncio.Future()  # Run forever

asyncio.run(main())
