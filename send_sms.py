from twilio.rest import TwilioRestClient
import os


account_sid = os.environ['TWILIO_ACCESS_TOKEN_KEY']
auth_token = os.environ['TWILIO_ACCESS_TOKEN_SECRET']

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
    to="+19493156013",
    from_="+19495417040",
    body="Get your stuff done!"
    )

print message.sid

