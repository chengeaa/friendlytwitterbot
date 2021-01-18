import os
from twilio.rest import Client


def send_text(msg, phone_num):

	account_sid = os.environ['TWILIO_ACCOUNT_SID']
	auth_token = os.environ['TWILIO_AUTH_TOKEN']
	client = Client(account_sid, auth_token)

	message = client.messages \
	    .create(
	         body=msg,
	         from_='+14158180469',
	         to="+" + phone_num
	     )

	return message.sid