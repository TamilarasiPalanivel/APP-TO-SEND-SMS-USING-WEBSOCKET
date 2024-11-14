import asyncio
import websockets
from twilio.rest import Client
import re

# Twilio configuration
TWILIO_ACCOUNT_SID = 'AC912ec1f56edf82775d7262c6f203ba17'  # Replace with your actual Account SID
TWILIO_AUTH_TOKEN = '1ac2de843a3f17e4d4cb1793fe07a503'      # Replace with your actual Auth Token
TWILIO_PHONE_NUMBER = '+18644774589'       # Replace with your Twilio phone number
#TWILIO_ACCOUNT_SID = 'AC22f5824e0a588a3ff105a9e5ce17cf8c'  # Replace with your actual Account SID
#TWILIO_AUTH_TOKEN = '6f54f0ab3b11a47b8e67186d1cb64d90'      # Replace with your actual Auth Token
#TWILIO_PHONE_NUMBER = '+18644774589'      

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to validate phone number format
def is_valid_phone_number(phone_number):
    # Simple regex to validate phone number format
    return re.match(r'^\+\d{1,15}$', phone_number) is not None

# Handle incoming WebSocket connections
async def sms_server(websocket, path):
    print("New client connected!")

    # Send a welcome message to the new client
    welcome_message = "Server: Welcome to the SMS server!"
    await websocket.send(welcome_message)

    try:
        async for message in websocket:
            print(f"Message received from client: {message}")

            # Extract the phone number and text from the message
            try:
                phone_number, sms_body = message.split(',', 1)  # Expecting format "phone_number,sms_body"
                phone_number = phone_number.strip()
                sms_body = sms_body.strip()

                if not is_valid_phone_number(phone_number):
                    response = "Server: Invalid phone number format. Please use international format (e.g., +1234567890)."
                    await websocket.send(response)
                    continue

                twilio_client.messages.create(
                    to=phone_number,
                    from_=TWILIO_PHONE_NUMBER,
                    body=sms_body
                )
                response = "Server: SMS sent successfully!"

            except ValueError:
                response = "Server: Message format is incorrect. Use 'phone_number,sms_body'."
            except Exception as e:
                response = f"Server: Failed to send SMS - {str(e)}"

            # Acknowledge the message
            await websocket.send(response)

    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start the WebSocket server
async def main():
    async with websockets.serve(sms_server, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # run forever

# Run the server
asyncio.run(main())
