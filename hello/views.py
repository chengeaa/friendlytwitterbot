from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .main import main

from .models import Greeting
from .sms import send_text

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    print("henlo")
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


@api_view(['POST'])
def analyzeUserTwitter(request):
	""" Takes in a twitter handle and returns a general sentiment analysis
	score, based on:
		- the user's own tweets
		- the content tweeted by people whom this user follows
	"""
	send_text("starting to analyze user twitter", "9258995573")
	print("analyzeUserTwitter received a request with some data! " + request.data.handle)
	phone_num = request.data.phone_num
	phone_num = phone_num.replace(" ", "").replace("-", "")  # strip any whitespace or hyphens


	# twitterhandle may need to have the @ stripped off
	if twitterHandle[0] == "@":
		twitterhandle = twitterhandle[1:]

	if "@" in twitterhandle:
		# something's terribly wrong here :(
		return -1

	user_sentiment, network_sentiment = main(twitterhandle, analyze_friends = True)
	if user_sentiment < -0.1 and user_sentiment > -0.5: # threshold for very minorly negative sentiment
		# send a text to the user with a positive news article
		msg = "Despite what Twitter might make you think, there's also good news out there in the world! https://www.goodnewsnetwork.org/swinhoes-turtle-the-most-endangered-on-earth-found-in-vietnam/"
		send_text(msg, phone_num)
	elif user_sentiment < -0.5:
		# send a meditation tips article
		msg = "Twitter got you down? Here's some tips on how to refocus your mind and stay positive :) https://www.mindful.org/how-to-meditate/"


	return render(request, "index.html")



	