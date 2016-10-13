from django.shortcuts import render
from django.contrib.auth.models import User
from authentication.models import UserProfile
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from contest.models import *
# Create your views here.


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

@csrf_exempt
def _login(request):
	if request.method=="POST":
		username=request.POST.get('email',False)
		email = request.POST['email']
		password = request.POST['password']
		# mobile_id=request.POST['id']
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				user.lastLoginDate=datetime.now()
				# user.userprofile.mobile_id=mobile_id
				user.userprofile.loggedIn=True
				user.save()
				return JsonResponse({'success':1,'message':'Success','email': email,'id':user.id})
			else:
				return JsonResponse({'success':0,'message':'Inactive'}) 
		else:
			return JsonResponse({'success':0,'message':'Email/Password incorrect'})


@csrf_exempt
def _logout(request):
	if request.method == "POST":
		userid=request.POST['id']
		user = User.objects.get(id=userid)
		if user is not None:
			user.userprofile.loggedIn=False
			user.save()
			return JsonResponse({'success':1})
		else:
			return JsonResponse({'success':0, 'message': "Invalid userid"})
	return JsonResponse({'success': 0, 'message': 'Invalid method'})


@csrf_exempt
def register(request):	
	registered = False
	response={}
	if request.method == "POST":
		method=request.POST['method']
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		mobile_id=request.POST['mobile_id']
		print profile_form
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.mobile_id=mobile_id
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()
			registered = True
			response['success']=1
		else:
			print user_form.errors, profile_form.errors
			response['success']=0
	return JsonResponse(response)

@csrf_exempt
def registergoogle(request):
	print('google sign-in register method called')
	registered = False
	flag=0
	response={}
	response['success']=0
	if request.method == "POST":
		method=request.POST['method']
		profile=UserProfile()
		name=request.POST['name']
		email=request.POST['email']
		print(email)
		password=""
		if method == 'normal':
			password=request.POST['password']
		#mobile_id=request.POST['mobile_id']	# we are doing only google sign in registration
		try:
			user=User.objects.get(username=email)
		except User.DoesNotExist:
			user=User()
			flag=1
		if flag == 1:
			user.first_name=name
			user.username=email
			user.password=password
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile.user = user
			#profile.mobile_id=mobile_id
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()
			registered = True
			response['success']=1
			response['email']=email
			response['id']=user.id
		else:
			#user.userprofile.mobile_id=mobile_id
			user.first_name=name
			#user.userprofile.save()
			user.save()
			response['success']=1
			response['message']="User is already present"
			response['email']=user.username
			response['id']=user.id
		if len(SectionScore.objects.filter(email=user.username)) > 0:
			s=SectionScore.objects.filter(email=user.username)[0]
			s.is_download=True
			s.save()
	return JsonResponse(response)

@csrf_exempt
def registerfcm(request):
	print('fcm token register method called')	
	registered = False
	flag=0
	response={}
	response['success']=0
	if request.method == "POST":
		profile=UserProfile()
		email=request.POST['email']
		mobile_id=request.POST['mobile_id']	# we are doing fcm token registration
		print(mobile_id)
		try:
			user = User.objects.get(username = email)
		except User.DoesNotExist:
			flag = 1
		if flag == 0:
			user.userprofile.mobile_id=mobile_id
			user.userprofile.save()
			response['success']=1
			response['message']="FCM token registered"
			response['email']=user.username
			response['id']=user.id
		if len(SectionScore.objects.filter(email=user.username)) > 0:
			s=SectionScore.objects.filter(email=user.username)[0]
			s.is_download=True
			s.save()
	return JsonResponse(response)

@csrf_exempt
def register_webapp(request):
	'''
	Input
	==================================
	name
	email
	'''
	registered = False
	flag=0
	response={}
	response['success']=0
	if request.method == "POST":
		profile=UserProfile()
		name=request.POST['name']
		email=request.POST['email']
		password=""
		mobile_id="Not avaliable"
		try:
			user=User.objects.get(username=email)
		except User.DoesNotExist:
			user=User()
			flag=1
		if flag == 1:
			user.first_name=name
			user.username=email
			user.password=password
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile.user = user
			profile.mobile_id=mobile_id
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			profile.save()
			registered = True
			response['success']=1
			response['email']=email
			response['id']=user.id
		else:
			response['success']=1
			response['message']="User is already present"
			response['email']=user.username
			response['id']=user.id
		user = authenticate(username=email, password=password)
		login(request, user)
		user.lastLoginDate=datetime.now()
		user.userprofile.loggedIn=True
		user.save()
		if len(SectionScore.objects.filter(email=user.username)) > 0:
			s=SectionScore.objects.filter(email=user.username)[0]
			s.is_download=True
			s.save()
	return JsonResponse(response)

def logout_webapp(request):
	logout(request)
	return JsonResponse({'success': 1, 'message': 'Logout done'})
