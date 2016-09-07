from twilio.rest import TwilioRestClient
import os

def send_text(phone_number):

    account_sid = os.environ['TWILIO_ACCESS_TOKEN_KEY']
    auth_token = os.environ['TWILIO_ACCESS_TOKEN_SECRET']

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(
        to="+1" + phone_number,
        from_="+19493045384",
        body="Thanks for coming to career day!"
        )

    print message.sid
