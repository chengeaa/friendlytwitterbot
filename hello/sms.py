import os
from twilio.rest import Client


def send_text(msg, phone_num):

	account_sid = AC8e0d5e16da424d81f0f509396e9afd25 #os.environ['TWILIO_ACCOUNT_SID']
	auth_token = b8fa6ae659a94171a9a2b751a2878c7d #os.environ['TWILIO_AUTH_TOKEN']
	client = Client(account_sid, auth_token)

	message = client.messages \
	    .create(
	         body=msg,
	         from_='+14158180469',
	         to="+" + phone_num
	     )

	return message.sid