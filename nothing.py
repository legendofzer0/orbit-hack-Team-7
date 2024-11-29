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

            # Process the client's message and use it in the query logic
            if data.get("type") == "text":
                query = data.get("content", "")  # Extract text content from the message
                print(f"Query received from client: {query}")
                
                if query.lower() == "exit":
                    response = {"type": "response", "content": "Exiting... Goodbye!"}
                    await websocket.send(json.dumps(response))
                    break
                
                # Simulate using query with your input-based logic
                if query == "1":
                    choice = query
                    while True:
                        # Receive client input for further interaction
                        response_prompt = {"type": "prompt", "content": "Send another query or type 'exit' to quit."}
                        await websocket.send(json.dumps(response_prompt))

                        message = await websocket.recv()
                        next_data = json.loads(message)
                        next_query = next_data.get("content", "")

                        if next_query.lower() == "exit":
                            response = {"type": "response", "content": "Session ended. Goodbye!"}
                            await websocket.send(json.dumps(response))
                            break
                        
                        # Simulate handling the next query
                        response_content = f"Processed your query: {next_query}"
                        response = {"type": "response", "content": response_content}
                        await websocket.send(json.dumps(response))

                else:
                    response = {"type": "response", "content": f"Received and processed: {query}"}
                    await websocket.send(json.dumps(response))
                    
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start WebSocket server
async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

# Run the server
asyncio.run(main())
