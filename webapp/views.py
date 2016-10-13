from django.shortcuts import render
from django.core import serializers
from evm.models import Event,Content,UserEvents,EventRatings,UserFollow,Club
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
import datetime
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib.sites.models import get_current_site
from django.utils.encoding import smart_str
from django.conf import settings
from django.core.mail import send_mail
import os
from django.core.files import File
from shutil import make_archive
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from authentication.views import get_client_ip
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.


def loginpage(request):
	response={}
	if request.user.is_authenticated():
		return HttpResponseRedirect('/eventhub/events/')
	response['login']=True
	print "Login"
	return render(request,'webapp/site/login.djt',response)

@login_required(login_url='/eventhub/')
def viewevents(request):
	response={}
	dt=datetime.datetime.now()
	end_date = dt + datetime.timedelta(days=30)
	events=Event.objects.filter(date_time__range = (dt,end_date)).order_by('date_time')
	response['upcoming']=events
	end_date = dt - datetime.timedelta(days=30)
	events=Event.objects.filter(date_time__range = (dt,end_date))
	response['previous']=events
	events=Event.objects.filter(date_time__year=dt.year).filter(date_time__month=dt.month).filter(date_time__day=dt.day).order_by('date_time')
	response['today']=events
	email=request.user.username
	user=User.objects.get(username=email)
	userevents=UserEvents.objects.filter(user=user)
	events=[]
	for u in userevents:
		events.append(u.event)
	print events
	response['myevents']=events
	return render(request,'webapp/site/index.djt',response)


@login_required(login_url='/eventhub/')
def getevent(request,eventid):
	response={}
	response['inner']=True
	user = User.objects.get(username = request.user.username)
	event=Event.objects.get(id=eventid)
	try:
		uevent = UserEvents.objects.get(user = user, event = event)
		response['going'] = 1
	except UserEvents.DoesNotExist:
		response['going'] = 0
	try:
		ufeedback = EventRatings.objects.get(user = user, event = event)
		response['feedback'] = 1
	except EventRatings.DoesNotExist:
		response['feedback'] = 0
	
	cur_time = datetime.datetime.now()
	event_time = event.date_time 
	if event_time < cur_time:
		response['started'] = 1
	else:
		response['started'] = 0
	users=UserEvents.objects.filter(event=event)
	ratings=EventRatings.objects.filter(event=event)
	response['event']=event
	response['user']=user
	response['average_rating']=ratings.aggregate(Avg('rating'))['rating__avg']
	response['today']=datetime.datetime.now()
	print response['today']
	return render(request,'webapp/site/viewevent.djt',response)
