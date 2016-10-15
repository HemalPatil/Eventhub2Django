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
import notification
import json
# Create your views here.


def homepage(request):
	return render(request,'site/home.html',{})

def sendfeedback(request):
	send_mail('Feedback:'+request.POST['name'], request.POST['feedback'], settings.EMAIL_HOST_USER,[request.POST['replyto']], fail_silently=False)

@csrf_exempt
def syncevents(request):
	print 'called syncevents'
	response={}
	if request.method=="POST":
		print request.POST['latest_created_on']
		print request.POST['email']
		flag = 0
		try:
			user = User.objects.get(username = request.POST['email'])
		except User.DoesNotExist:
			flag = 1
		if flag == 0:
			today = datetime.date.today().strftime("%Y-%m-%d 00:00:00")
			events=Event.objects.filter(created_on__gt=request.POST['latest_created_on'], date_time__gte=today).order_by('date_time')
			responsef=[]
			for e in events:
				response={}
				response['id']=e.id
				response['name']=e.name
				print response['name']
				response['date_time']=e.date_time.strftime("%Y-%m-%d %H:%M:%S")
				response['venue']=e.venue
				response['type']=e.type
				response['subtype']=e.subtype
				response['alias'] = e.alias
				if e.club:
					response['club']=e.club.name
					response['club_id'] = e.club.id
				else:
					response['club']='Club'
					response['club_id'] = 0
				response['contact_name_1']=e.contact_name_1
				response['contact_number_1']=e.contact_number_1
				response['contact_name_2']=e.contact_name_2
				response['contact_number_2']=e.contact_number_2
				response['created_on'] = e.created_on
				content = Content.objects.get(event=e.id)
				response['description'] = content.description
				follow = 1
				try:
					userevent = UserEvents.objects.get(event = e.id, user = user.id)
				except UserEvents.DoesNotExist:
					follow = 0
				response['followed'] = follow
				responsef.append(response)
			print 'will return success 1'
			return JsonResponse(dict(events=responsef))
	print 'will return success 0'
	return JsonResponse({'success': 0})

@csrf_exempt
def syncclubs(request):
	response = {}
	print 'syncclubs called'
	if request.method == "POST":
		print request.POST['email']
		flag = 0
		try:
			user = User.objects.get(username = request.POST['email'])
		except User.DoesNotExist:
			flag = 1
		if flag == 0:
			newclubs = json.loads(request.POST['newclubsjson'])
			responsef = []
			for clubID in newclubs['newclubs']:
				response = {}
				club = Club.objects.get(id=clubID)
				response['id'] = clubID
				response['name'] = club.name
				response['alias'] = club.alias
				follow = 1
				try:
					userclub = UserFollow.objects.get(user = user.id, club = clubID)
				except UserFollow.DoesNotExist:
					follow = 0
				response['followed'] = follow
				responsef.append(response)
			return JsonResponse(dict(newclubs=responsef))
	return JsonResponse({'success' : 0})

@csrf_exempt
def followclub(request):
	if request.method == "POST":
		print 'follow club called ' + request.POST['email']
		flag = 0
		try:
			user = User.objects.get(username = request.POST['email'])
		except User.DoesNotExist:
			flag=1
		if flag==0:
			clubexists = 1
			try:
				club = Club.objects.get(id=request.POST['clubid'])
			except Club.DoesNotExist:
				clubexists = 0
			if clubexists == 1:
				# check if already followed, if followed then do nothing
				# if not already followed add a row in UserFollow
				# then get all events by that club
				# check if the user already follows the events by that club
				# if user does then do nothing else add a row in UserEvents
				clubfollowed = 1
				try:
					followobject = UserFollow.objects.get(user = user, club = club)
				except UserFollow.DoesNotExist:
					clubfollowed = 0
				if clubfollowed==0:
					UserFollow(user = user, club = club, follow=True).save()
				clubevents = Event.objects.filter(club = club)
				for e in clubevents:
					eventfollowed = 1
					try:
						usereventfollow = UserEvents.objects.get(user = user, event = e)
					except UserEvents.DoesNotExist:
						eventfollowed = 0
					if eventfollowed==0:
						UserEvents(user=user, event = e).save()
				return JsonResponse({'success' : 1})
	return JsonResponse({'success' : 0})

@csrf_exempt
def unfollowclub(request):
	if request.method == "POST":
		print 'unfollow club called ' + request.POST['email']
		flag =  0
		try:
			user = User.objects.get(username = request.POST['email'])
		except User.DoesNotExist:
			flag = 1
		if flag==0:
			clubexists = 1
			try:
				club = Club.objects.get(id=request.POST['clubid'])
			except Club.DoesNotExist:
				clubexists = 0
			if clubexists==1:
				UserFollow.objects.filter(user = user, club = club).delete()
				clubevents = Event.objects.filter(club = club)
				for e in clubevents:
					UserEvents.objects.get(user=user, event=e).delete()
				return JsonResponse({'success' : 1})
	return JsonResponse({'success' : 0})

@csrf_exempt
def followevent(request):
	if request.method == "POST":
		print 'follow event called ' + request.POST['email']
		userexists = 1
		try:
			user = User.objects.get(username = request.POST['email'])
		except User.DoesNotExist:
			userexists = 0
		if userexists==1:
			eventexists = 1
			try:
				event = Event.objects.get(id=request.POST['eventid'])
			except Event.DoesNotExist:
				eventexists = 0
			if eventexists==1:
				eventfollowed = 1
				try:
					eventfollow = UserEvents.objects.get(user=user, event=event)
				except UserEvents.DoesNotExist:
					eventfollowed = 0
				if eventfollowed==0:
					UserEvents(user=user, event=event).save()
				return JsonResponse({'success' : 1})
	return JsonResponse({'success' : 0})

@csrf_exempt
def unfollowevent(request):
	if request.method == "POST":
		print 'unfollow event called ' + request.POST['email']
		userexists = 1
		try:
			user = User.objects.get(username = request.POST['email'])
		except User.DoesNotExist:
			userexists = 0
		if userexists==1:
			eventexists = 1
			try:
				event = Event.objects.get(id=request.POST['eventid'])
			except Event.DoesNotExist:
				eventexists = 0
			if eventexists==1:
				UserEvents.objects.filter(user=user,event=event).delete()
				return JsonResponse({'success' : 1})
	return JsonResponse({'success' : 0})

@csrf_exempt
def get_list_upcoming(request):
	response={}
	if request.method == "POST":
		date=request.POST['date']
		dt=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") 
		end_date = dt + datetime.timedelta(days=30)
		events=Event.objects.filter(date_time__range = (dt,end_date)).order_by('date_time')
		responsef=[]
		for e in events:
			response={}
			response['id']=e.id
			response['name']=e.name
			response['date']=e.date_time
			response['venue']=e.venue
			response['type']=e.type
			response['subtype']=e.subtype
			if e.club:
				response['club']=e.club.name
			else:
				response['club']='Club'
			response['contact_name_1']=e.contact_name_1
			response['contact_number_1']=e.contact_number_1
			response['contact_name_2']=e.contact_name_2
			response['contact_number_2']=e.contact_number_2
			responsef.append(response)
		return JsonResponse(dict(events=responsef))
	return JsonResponse({'success': 0})

@csrf_exempt
def get_list_previous(request):
	response={}
	if request.method == "POST":
		date=request.POST['date']
		dt=datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") 
		end_date = dt - datetime.timedelta(days=30)
		events=Event.objects.filter(date_time__range = (dt,end_date))
		responsef=[]
		for e in events:
			response={}
			response['id']=e.id
			response['name']=e.name
			response['date']=e.date_time
			response['venue']=e.venue
			response['type']=e.type
			response['subtype']=e.subtype
			if e.club:
				response['club']=e.club.name
			else:
				response['club']='Club'
			response['contact_name_1']=e.contact_name_1
			response['contact_number_1']=e.contact_number_1
			response['contact_name_2']=e.contact_name_2
			response['contact_number_2']=e.contact_number_2
			responsef.append(response)
		return JsonResponse(dict(events=responsef))
	return JsonResponse({'success': 0})



@csrf_exempt
def get_list_date(request):
	response={}
	if request.method == "POST":
		date=request.POST['date']
		dt=datetime.datetime.strptime(date, "%Y-%m-%d") 
		events=Event.objects.filter(date_time__year=dt.year).filter(date_time__month=dt.month).filter(date_time__day=dt.day).order_by('date_time')
		responsef=[]
		for e in events:
			response={}
			response['id']=e.id
			response['name']=e.name
			response['date']=e.date_time
			response['venue']=e.venue
			response['type']=e.type
			response['subtype']=e.subtype
			if e.club:
				response['club']=e.club.name
			else:
				response['club']='Club'
			response['contact_name_1']=e.contact_name_1
			response['contact_number_1']=e.contact_number_1
			response['contact_name_2']=e.contact_name_2
			response['contact_number_2']=e.contact_number_2
			responsef.append(response)
		return JsonResponse(dict(events=responsef))
	return JsonResponse({'success': 0})


@csrf_exempt
def getEvent(request):
	if request.method == "POST":
		response={}
		eventid=request.POST['id']
		email = request.POST['email']
		try:
			user = User.objects.get(username = email)
		except User.DoesNotExist:
			user=User()
			user.first_name=email.split('@')[0]
			user.username=email
			user.password=""
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile=UserProfile()
			profile.user = user
			profile.mobile_id="test12345"
			profile.lastLoginDate = datetime.datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()	
			response['message']="User not found....creating user"		
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
		response['id']=event.id
		response['name']=event.name
		response['date']=event.date_time
		if event.club:
			response['club']=event.club.name
		else:
			response['club']='Club'
		response['contact_name_1']=event.contact_name_1
		response['contact_number_1']=event.contact_number_1
		response['contact_name_2']=event.contact_name_2
		response['contact_number_2']=event.contact_number_2
		response['venue']=event.venue
		response['user_count']=len(users)
		response['content']=event.content.description
		response['average_rating']=ratings.aggregate(Avg('rating'))['rating__avg']
		# try:
		# 	img=open(event.content.image.path,'rb')
		# 	data=img.read()
		# 	response['image']="%s" % data.encode('base64')
		# except IOError:
		# 	return event.content.image.url
		response['image'] = get_current_site(request).domain+event.content.image.url
		return JsonResponse(response)
	return JsonResponse({'success': 0})


@csrf_exempt
def getuserlist(request):
	if request.method == "POST":
		eventid=request.POST['id']
		event=Event.objects.get(id=eventid)
		users=UserEvents.objects.filter(event=event)
		response={}
		response['users']=[]
		for u in users:
			response['users'].append(u.user.first_name)
		return JsonResponse(dict(users=response['users']))
	return JsonResponse({'success':0})



@csrf_exempt
def iamgoing(request):
	if request.method == "POST":
		eventid=request.POST['event_id']
		email=request.POST['email']
		uevent=UserEvents()
		event=Event.objects.get(id=eventid)
		user=User.objects.get(username=email)
		try:
			uevent = UserEvents.objects.get(event = event, user = user)
			return JsonResponse({'success': 1})	
		except UserEvents.DoesNotExist:
			uevent.event=event
			uevent.user=user
			uevent.save()
			return JsonResponse({'success': 1})	
	return JsonResponse({'success': 0})


@csrf_exempt
def iamnotgoing(request):
	if request.method == "POST":
		eventid=request.POST['event_id']
		email=request.POST['email']
		uevent=UserEvents()
		event=Event.objects.get(id=eventid)
		user=User.objects.get(username=email)
		uevent = UserEvents.objects.get(event = event, user = user)
		uevent.delete()
		return JsonResponse({'success': 1})	
	return JsonResponse({'success': 0})


@csrf_exempt
def getMyEvents(request):
	if request.method == "POST":
		email=request.POST['email']
		user=User.objects.get(username=email)
		events=UserEvents.objects.filter(user=user)
		print events
		responsef=[]
		for e in events:
			response={}
			response['id']=e.event.id
			response['name']=e.event.name
			response['date']=e.event.date_time
			response['venue']=e.event.venue
			responsef.append(response)
		return JsonResponse(dict(events=responsef))
	return JsonResponse({'success': 0})

@csrf_exempt
def addfeedback(request):
	if request.method == "POST":
		event_id=request.POST['event_id']
		email=request.POST['email']
		rating=request.POST['rating']
		feedback=request.POST['feedback']
		event=Event.objects.get(id=event_id)
		user=User.objects.get(username=email)
		review=EventRatings()
		review.event=event
		review.user=user
		review.rating=rating
		review.feedback=feedback
		review.save()
		return JsonResponse({'sucess':1, 'message': 'Review recorded'})
	return JsonResponse({'sucess':0, 'message': 'Invalid'})

@csrf_exempt
def addfollowing(request):
	"""
	Following view
	Input: email:
		   club_id: ids of clubs he has checked in clid|clid|... format
		   club_id_unchecked : ids of clubs unchecked same format
	Output: success : 0 or 1
	"""
	response={}
	response['success']=0
	if request.method == "POST":
		email=request.POST["email"]
		try:
			user=User.objects.get(username=email)
		except User.DoesNotExist:
			response["message"] = "User does not exist"
			return response
		
		club_ids=request.POST['club_id']
		if club_ids != "":
			club_ids=club_ids.split('|')
			for club_id in club_ids:
				club=Club.objects.get(id=club_id)
				try:
					u=UserFollow.objects.get(user=user,club=club)
					u.follow=True
					u.save()
				except:
					u=UserFollow()
					u.user=user
					u.club=club
					u.follow=True
					u.save()
		club_ids=request.POST['club_id_unchecked']
		if club_ids != "":
			club_ids=club_ids.split('|')
			for club_id in club_ids:
				club=Club.objects.get(id=club_id)
				try:
					u=UserFollow.objects.get(user=user,club=club)
					u.follow=False
					u.save()
				except:
					u=UserFollow()
					u.user=user
					u.club=club
					u.follow=False
					u.save()

		response['success']=1
	return JsonResponse(response)


@csrf_exempt
def addevent(request):
	print 'called after event added before content added'
	"""
	Add an event if the user is admin
	=======input===========
	name
	type
	subtype
	club
	date_time
	contact_name_1
	contact_name_2
	contact_number_1
	contact_number_2
	venue
	photo -> It is an image that is sent here
	description

	====Output==========
	success 0 or 1
	message -> for toast

	"""
	response={}
	response['success']=0
	if request.method == 'POST':
		email=request.POST['email']
		user=User.objects.get(username=email)
		if user.is_active and user.is_staff:
			event_name=request.POST['name']
			event_type=request.POST['type']
			event_subtype=request.POST['subtype']
			event_club_name=request.POST['club']
			event_club = Club.objects.get(name = event_club_name)
			event_date_time=request.POST['date_time']
			event_contact_name_1=request.POST['contact_name_1']
			event_contact_name_2=request.POST['contact_name_2']
			event_contact_number_1=request.POST['contact_number_1']
			event_contact_number_2=request.POST['contact_number_2']
			event_venue=request.POST['venue']
			event_alias=event_name+event_date_time.replace(' ','')+event_venue
			event_addedby=user
			event=Event(name=event_name,type=event_type,subtype=event_subtype,club=event_club,date_time=event_date_time,contact_name_1=event_contact_name_1,contact_number_1=event_contact_number_1,contact_name_2=event_contact_name_2,contact_number_2=event_contact_number_2,venue=event_venue,alias=event_alias,addedby=event_addedby)
			event.save()
			event_image=request.FILES['photo']
			event_description=request.POST['description']
			event_desp=Content(event=event,image=event_image,description=event_description,addedby=event_addedby)
			event_desp.save()
			#Sending notification about the new event
			clubc=event.club
			ids = UserFollow.objects.values_list('user__userprofile__mobile_id', flat=True).filter(club = clubc)
			if len(ids) > 0:
				message="A new event '"+event.name+"' has been added by "+clubc.name+". Check it out!"
				notification.send_notification_custom(event,ids,message)
			response['message']="Event "+event_name+" has been added"
			response['success']=1
		else:
			response['message']="User is not an admin. Cannot add the event"
			response['success']=0
	else:
		response['message']="Sorry wrong place"
	return JsonResponse(response)

@csrf_exempt
def delevent(request):
	"""
	Delete an event if the user is admin
	=======input===========
	event_id
	email
	====Output==========
	success 0 or 1
	message -> for toast

	"""
	response={}
	response['success']=0
	if request.method == 'POST':
		event_id=request.POST['event_id']
		email=request.POST['email']
		user=User.objects.get(username=email)
		if user.is_active and user.is_staff:
			event=Event.objects.get(id=event_id)
			if event.addedby == user:
				event.delete() #cascade deleting
				response['success']=1
			else:
				response['message']="Not the event admin"
		else:
			response['message']="User is not an admin. Cannot add the event"
			response['success']=0
	else:
		response['message']="Sorry wrong place"
	return JsonResponse(response)

@csrf_exempt
def updateevent(request):
	"""
	Update event venue or time and a notification is sent otherwise only it is changed
	=======Input===============
	email
	event_id
	description
	date_time
	venue
	========Output==============
	success
	message
	"""
	response={}
	response['success']=0
	if request.method == "POST":
		event_id=request.POST['event_id']
		email=request.POST['email']
		user=User.objects.get(username=email)
		if user.is_active and user.is_staff:
			event=Event.objects.get(id=event_id)
			old_venue = event.venue
			old_date_time = event.date_time
			if event.addedby == user:
				event.content.description=request.POST['description']
				event.date_time=request.POST['date_time']
				event.venue=request.POST['venue']
				event.content.save()
				event.save()
				# sending notification in case the time or venue changed in the update.
				if event.date_time != old_date_time or event.venue != old_venue:
					users = UserEvents.objects.values_list('user__userprofile__mobile_id', flat=True).filter(event = event)
					print "list is------------------------ ",users
					ids = users
					if len(ids) > 0:
						notification.send_notification(event,ids)
				response['success']=1
			else:
				response['message']="User did not create event"
		else:
			response['message']="User is not superuser"
	return JsonResponse(response)


@csrf_exempt
def sendnotification(request):
	"""
	Send notification to followers of event
	====Input=======
	email
	event_id
	message
	=====output=======
	success 
	sometimes message 
	"""
	response={}
	response['success']=0
	if request.method == 'POST':
		email=request.POST['email']
		event_id=request.POST['event_id']
		message=request.POST['message']
		user=User.objects.get(username=email)
		if user.is_active and user.is_staff:
			event=Event.objects.get(id=event_id)
			if event.addedby == user:
				ids=UserEvents.objects.values_list('user__userprofile__mobile_id', flat=True).filter(event = event)
				if len(ids) > 0:
					notification.send_notification_custom(event,ids,message)
				response['success']=1	
			else:
				response['message']="Not an event of the user"
		else:
			response['message']="Not a super user"
	return JsonResponse(response)

@csrf_exempt
def geteventlist(request):
	"""
	Get list of events added by user
	======Input=========
	email
	======Output========
	json array of events
	"""
	response={}
	if request.method == 'POST':
		email=request.POST['email']
		user=User.objects.get(username=email)
		events=Event.objects.filter(addedby=user)
		for e in events:
			temp={}
			temp['name']=e.name
			temp['venue']=e.venue
			response[e.name]=temp
	return JsonResponse(response)

@csrf_exempt
def app_refresh_events(request):
	response={}
	if request.method == "POST":
		event_id = request.POST['id']
		events=Event.objects.filter(id__gt = event_id).order_by('date_time')
		responsef=[]
		for e in events:
			response={}
			response['id']=e.id
			response['name']=e.name
			response['date']=e.date_time
			response['venue']=e.venue
			response['type']=e.type
			response['subtype']=e.subtype
			if e.club:
				response['club']=e.club.name
			else:
				response['club']='Club'
			response['contact_name_1']=e.contact_name_1
			response['contact_number_1']=e.contact_number_1
			response['contact_name_2']=e.contact_name_2
			response['contact_number_2']=e.contact_number_2
			responsef.append(response)
		return JsonResponse(dict(events=responsef))
	return JsonResponse({'success': 0})



def download(request):
	if request.user.is_superuser:
	    db_engine = settings.DATABASES['default']['ENGINE']
	    if db_engine == 'django.db.backends.sqlite3':
	        db_path = settings.DATABASES['default']['NAME']
	        dbfile = File(open(db_path, "rb"))
	        response = HttpResponse(dbfile,content_type='application/x-sqlite3')
	        response['Content-Disposition'] = 'attachment; filename=%s' % db_path
	        response['Content-Length'] = dbfile.size
	        return response
	    else:
	        return HttpResponse("settings.DATABASES['default']['ENGINE'] is %s,<br />\
	                             only for 'django.db.backends.sqlite3' online backup is posible." % (db_engine))
	else:
		return HttpResponse("Only admin can access this url.")




def download_media(request):
	if request.user.is_superuser:
	    """
	    A django view to zip files in directory and send it as downloadable response to the browser.
	    Args:
	      @request: Django request object
	    Returns:
	      A downloadable Http response
	    """
	    file_path = settings.MEDIA_ROOT
	    path_to_zip = make_archive(file_path,"zip",file_path)
	    response = HttpResponse(FileWrapper(file(path_to_zip,'rb')), content_type='application/zip')
	    response['Content-Disposition'] = 'attachment; filename=media.zip'
	    return response
	else:
		return HttpResponse("Only admin can access this url.")