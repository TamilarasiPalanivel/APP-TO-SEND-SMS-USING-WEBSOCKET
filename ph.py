from twilio.rest import Client

# Your Twilio Account SID and Auth Token
TWILIO_ACCOUNT_SID = 'AC22f5824e0a588a3ff105a9e5ce17cf8c'  # Replace with your actual Account SID
TWILIO_AUTH_TOKEN = '6f54f0ab3b11a47b8e67186d1cb64d90'  # Replace with your actual Auth Token

# Initialize the Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Fetch your Twilio phone numbers
phone_numbers = client.incoming_phone_numbers.list()

# Print the first Twilio phone number associated with your account
if phone_numbers:
    print(f"Your Twilio Phone Number: {phone_numbers[0].phone_number}")
else:
    print("No Twilio phone numbers found.")
