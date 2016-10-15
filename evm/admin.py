from django.contrib import admin
from .models import Event, Content, UserEvents, EventRatings, Notification, Club, UserFollow
from authentication.models import UserProfile
import notification
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.conf import settings



# Register your models here.




class EventAdmin(admin.ModelAdmin):
	exclude = ('addedby',)

	def get_queryset(self,request):
		print "Check"
		queryset = super(EventAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			print "Super user"
			return queryset
		else:
			print "Normal"
			return queryset.filter(addedby=request.user)    
	
	def save_model(self, request, obj, form, change):
		print form.changed_data
		if getattr(obj, 'addedby', None) is None:
			print "None"
			obj.addedby = request.user
			obj.save()
		if 'date_time' in form.changed_data or 'venue' in form.changed_data:
			users = UserEvents.objects.values_list('user__userprofile__mobile_id', flat=True).filter(event = obj)
			print "list is------------------------ ",users
			ids = users
			# ids = ["APA91bGzrX6HEgdPg4XCI-30TE9gTg9YeUFayr7xb8KDDl6WbyzXBJhfNIzeadptI_pjcfRTMVpjdAVZraHIC9m6t_-9o6lEPp-hb13RyBBtN5MJmNzk-6bAme8OHI0TcTFH4yRu4nhD"]
			if len(ids) > 0:
				notification.send_notification(obj,ids)

			try:
				image_url = settings.BASE_URL+obj.content.image.url
				ids=UserProfile.objects.values_list('mobile_id',flat=True)
				# sending the event details via notification to all the users
				# notification.send_event(obj.event, image_url, ids)
			except Content.DoesNotExist, e:
				print "first time event creation"
				pass
			

		return super(EventAdmin, self).save_model(request, obj, form, change)
	def response_add(self, request, obj, post_url_continue=None):
		content=Content()
		content.event=obj
		content.description="Stay tuned for event details"
		content.addedby=request.user
		content.save()
		# code to send notifications when adding an event to be added here!
		return HttpResponseRedirect("/admin/evm/content/"+str(content.id)+"/")


class ContentAdmin(admin.ModelAdmin):
	exclude=('addedby',)
	def render_change_form(self, request, context, *args, **kwargs):
		if not request.user.is_superuser:
			context['adminform'].form.fields['event'].queryset = Event.objects.filter(addedby=request.user)
		return super(ContentAdmin, self).render_change_form(request, context, args, kwargs)         
	def get_queryset(self,request):
		print "Check"
		queryset = super(ContentAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			print "Super user"
			return queryset
		else:
			print "Normal"
			return queryset.filter(addedby=request.user)
	def save_model(self, request, obj, form, change):
		notification.send_notification_custom(obj.event,["APA91bFWMbep-aUAoZoNnYoygmGFbm0Bvhj9O-6qO83lDbHSEiSYNchWQl-rlo0Ho8MKJriracata6si-pUKlZR-QyzI_uvNzEujqD9IshuG4UlhUXGquBK-SDNr3p5TcCMGTZrxVKQQccY4KvFzmDRnACY5ustNLw"],"New event "+obj.event.name +" by " + obj.event.club.name)
		if getattr(obj, 'addedby', None) is None:
			print "None"
			obj.addedby = request.user
			obj.save()
		clubc=obj.event.club
		print "club is -> ",clubc
		ids = UserFollow.objects.values_list('user__userprofile__mobile_id', flat=True).filter(club = clubc)
		if len(ids) > 0:
			print 'follow list is', ids
			message="A new event '"+obj.event.name+"' has been added by "+clubc.name+". Check it out!"
			# custom notification for those users who are following the club
			notification.send_notification_custom(obj.event,ids,message)
		image_url = settings.BASE_URL+obj.image.url
		ids=UserProfile.objects.values_list('mobile_id',flat=True)
		# sending the event details via notification to all the users
		# notification.send_event(obj.event, image_url, ids)
		return super(ContentAdmin, self).save_model(request, obj, form, change)



class NotificationAdmin(admin.ModelAdmin):
	exclude=('addedby',)
	def render_change_form(self, request, context, *args, **kwargs):
		if not request.user.is_superuser:
			context['adminform'].form.fields['event'].queryset = Event.objects.filter(addedby=request.user)
		return super(NotificationAdmin, self).render_change_form(request, context, args, kwargs)    

	def get_queryset(self,request):
		print "Check"
		queryset = super(NotificationAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			print "Super user"
			return queryset
		else:
			print "Normal"
			return queryset.filter(addedby=request.user)     
	def save_model(self, request, obj, form, change):
		if getattr(obj, 'addedby', None) is None:
			print "None"
			obj.addedby = request.user
			obj.save()
		if obj.event.name == 'all':
			users = UserProfile.objects.values_list('mobile_id',flat=True)
		else:
			users = UserEvents.objects.values_list('user__userprofile__mobile_id', flat=True).filter(event = obj.event)
		print "list is------------------------ ",users
		ids = users
			# ids = ["APA91bGzrX6HEgdPg4XCI-30TE9gTg9YeUFayr7xb8KDDl6WbyzXBJhfNIzeadptI_pjcfRTMVpjdAVZraHIC9m6t_-9o6lEPp-hb13RyBBtN5MJmNzk-6bAme8OHI0TcTFH4yRu4nhD"]
		if len(ids) > 0:
			notification.send_notification_custom(obj.event,ids,obj.message)
		return super(NotificationAdmin, self).save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(UserEvents)
admin.site.register(EventRatings)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Club)
admin.site.register(UserFollow)
