from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eventapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','evm.views.homepage'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'authentication.views.index'),
    url(r'^login/', 'authentication.views._login'),
    url(r'^register_google/', 'authentication.views.registergoogle'),
    url(r'^register_fcm/', 'authentication.views.registerfcm'),
    url(r'^eventhublogin/auth/webapp/', 'authentication.views.register_webapp'),
    url(r'^eventhublogin/logoutuser', 'authentication.views.logout_webapp'),
    # url(r'^loginuser/', 'authentication.views._loginuser'),
    # url(r'^dashboard/', 'authentication.views.dashboard'),
    # url(r'^logout/', 'authentication.views._logout'),
    url(r'^getevent/', 'evm.views.getEvent'),
    url(r'^geteventd/', 'evm.views.get_list_date'),
    url(r'^geteventu/', 'evm.views.get_list_upcoming'),
    url(r'^geteventp/', 'evm.views.get_list_previous'),
    url(r'^iamgoing/', 'evm.views.iamgoing'),
    url(r'^iamnotgoing/', 'evm.views.iamnotgoing'),
    url(r'^getmyevents/', 'evm.views.getMyEvents'),
    url(r'^addfeedback/', 'evm.views.addfeedback'),
    url(r'^geteventusers/', 'evm.views.getuserlist'),
    url(r'^backup/', 'evm.views.download'),
    url(r'^mediabackup/', 'evm.views.download_media'),
    url(r'^sendfeedback/', 'evm.views.sendfeedback'),
    url(r'^followclub/', 'evm.views.addfollowing'),
    url(r'^addevent/', 'evm.views.addevent'),
    url(r'^delevent/', 'evm.views.delevent'),
    url(r'^updateevent/', 'evm.views.updateevent'),
    url(r'^sendnotification/', 'evm.views.sendnotification'),
    url(r'^refresh/', 'evm.views.app_refresh_events'),
    url(r'^contest/',include('contest.urls')),
    url(r'^eventhub/',include('webapp.urls')),
    url(r'^syncclubs/', 'evm.views.syncclubs'),
    url(r'^syncevents/', 'evm.views.syncevents')

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
