
import os
from twilio.rest import Client

# --- Configuration ---
# Your Account SID and Auth Token from twilio.com/console
# It's recommended to set these as environment variables for security
# For Windows: set TWILIO_ACCOUNT_SID=your_sid
#              set TWILIO_AUTH_TOKEN=your_token
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

# Your Twilio phone number
twilio_number = "+15017122661"  # Replace with your Twilio phone number

# The phone number you want to call
to_number = "+15558675310"      # Replace with the recipient's phone number

# The message you want to convert to speech
message_to_say = "Hello! This is a test call from our new automated system. We are offering a special promotion on our services. Thank you!"

# --- Create a Twilio Client ---
if not account_sid or not auth_token:
    print("Error: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set as environment variables.")
else:
    client = Client(account_sid, auth_token)

    # --- Make the Call ---
    try:
        print(f"Initiating call from {twilio_number} to {to_number}...")
        call = client.calls.create(
            twiml=f'<Response><Say>{message_to_say}</Say></Response>',
            to=to_number,
            from_=twilio_number
        )
        print(f"Call initiated successfully! SID: {call.sid}")

    except Exception as e:
        print(f"An error occurred: {e}")

