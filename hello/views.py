from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .main import main

from .models import Greeting

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
	print("analyzeUserTwitter received a request with some data! " + request.data.handle)

	# twitterhandle may need to have the @ stripped off
	if twitterHandle[0] == "@":
		twitterhandle = twitterhandle[1:]

	if "@" in twitterhandle:
		# something's terribly wrong here :(
		return -1

	output = main(twitterhandle, analyze_friends = False)

	return render(request, "index.html")



	