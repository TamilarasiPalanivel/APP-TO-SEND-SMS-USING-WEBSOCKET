import asyncio
import websockets

# Handle WebSocket connection to the server
async def sms_client():
    uri = "ws://localhost:8765"  # Changed port to 8765
    
    async with websockets.connect(uri) as websocket:
        message = input("Enter the message to send (SMS): ")
        
        # Send message to server
        await websocket.send(message)
        print(f"Sent to server: {message}")
        
        # Wait for response from server
        response = await websocket.recv()
        print(f"Received from server: {response}")

# Run the client
asyncio.run(sms_client())
