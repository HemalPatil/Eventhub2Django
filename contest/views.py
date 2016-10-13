from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,JsonResponse,HttpResponseNotFound
from contest.models import *
from authentication.models import *
from django.db.models import Count

# Create your views here.


def homecontest(request):
	return render(request,'contest/site/index.djt',{})


@login_required(login_url='/admin/')
def addresult(request):
	if request.method == 'POST':
		print request.FILES
		if request.FILES['classlist']:
			f = request.FILES['classlist'].read()
			f=f.split('\n')
			for row in f:
				if len(row) > 0:
					l=row.split(',')
					s=SectionScore()
					s.section=request.POST['section']
					s.email=l[0][1:-1]
					print l[1].title()
					s.is_android= l[1].title() == 'True'
					s.save()
			print request.POST['section']
	return render(request,'contest/site/upload.djt',{})


@login_required(login_url='/admin/')
def refreshresult(request):
	l=SectionScore.objects.all()
	for stu in l:
		if len(UserProfile.objects.filter(user__username=stu.email)) > 0 and stu.is_android == True and stu.is_download == False: 
			stu.is_download=True
			stu.save()
	return HttpResponseRedirect('/contest/')



# @login_required(login_url='/admin/')
# def contestcheck(request):
# 	#Check the contest details


def contestresult(request):
	l=SectionScore.objects.filter(is_download=True).values('section').annotate(dcount=Count('email'))
	print l
	return render(request,'contest/site/livepoll.djt',{'section':l})


