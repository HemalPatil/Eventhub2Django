from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from contest import views

urlpatterns = patterns('',
	url(r'^$',views.homecontest),
	url(r'addresult/',views.addresult),
	url(r'refreshresult/',views.refreshresult),
	url(r'getresult/',views.contestresult),
)