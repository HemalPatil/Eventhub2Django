from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToCover
import time
import datetime
import notification
# Create your models here.



def get_image_path(instance, filename):
    return '{0}{1}'.format(instance.event.alias,filename[filename.rfind("."):])

class Club(models.Model):
    name=models.CharField(max_length=128)
    alias=models.CharField(max_length=128)
    def __unicode__(self):
        return self.name



class Event(models.Model):
    TYPE_CHOICES = (
        ('event', 'event'),
        ('workshop', 'workshop'),
        ('lecture', 'lecture'),
        ('attraction', 'attraction'),
    )
    SUBTYPE_CHOICES = (
        ('general', 'general'),
        ('club', 'club'),
        ('IG', 'IG'),
        ('online', 'online'),
        ('Branch', 'Branch'),
    )
    CLUB_CHOICES = (
        ('DND', 'DND'),
        ('music', 'music'),
        ('quiz', 'quiz'),
        ('DLD', 'DLD'),
        ('Painting','Painting'),
        ('LND','LND'),
        ('PGC','PGC'),
        ('Science and Hobbies','Science and Hobbies'),
        ('EA-HAM','EA-HAM'),
        ('Value Education','Value Education'),
        ('Innovation','Innovation'),
        ('Film','Film'),
        ('ISE','ISE'),
        ('ISTE','ISTE'),
        ('Youth Red Cross','Youth Red Cross'),
        ('FISA','FISA'),
        ('Magazine','Magazine'),
        ('HoneyBee','HoneyBee'),
        ('SpicMacay','SpicMacay'),
        ('Radio','Radio'),
        ('Branch','Branch'),
        ('CSEA','CSEA'),
        ('CHEA','CHEA'),
        ('ECEA','ECEA'),
        ('MEA','MEA'),
        ('EEEA','EEEA'),
        ('CEA','CEA'),
        ('MBA','MBA'),
        ('META','META'),
        ('BIOTECH','BIOTECH'),
    )


    type = models.CharField(max_length=128,choices=TYPE_CHOICES, default='event')
    subtype = models.CharField(max_length=128,choices=SUBTYPE_CHOICES, default='general')
    # club = models.CharField(max_length=128,choices=CLUB_CHOICES, default='general')
    club = models.ForeignKey(Club, related_name='events',blank=True,null=True)
    name = models.CharField(max_length=128, unique=True)
    date_time = models.DateTimeField()
    created_on=models.DateTimeField(auto_now=True)
    contact_name_1 = models.CharField(max_length=128)
    contact_number_1 = models.CharField(max_length=10)
    contact_name_2 = models.CharField(max_length=128)
    contact_number_2 = models.CharField(max_length=10)
    venue = models.CharField(max_length=128)
    alias = models.CharField(max_length=128,unique=True)
    addedby=models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
		return self.name




class Content(models.Model):
    event = models.OneToOneField(Event, related_name='content')
    # image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    image = ProcessedImageField(upload_to=get_image_path, blank=True, null=True,processors=[ResizeToCover(300, 300)])#(width,height)
    description = models.TextField(max_length=500)
    addedby=models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
		return self.event.name


class UserEvents(models.Model):
    event=models.ForeignKey(Event, related_name='event')
    user=models.ForeignKey(User,related_name='user')
    def __unicode__(self):
        return self.user.username+" : "+self.event.name

class EventRatings(models.Model):
    user=models.ForeignKey(User,related_name='userfeedback')
    event=models.ForeignKey(Event,related_name='eventfeedback')
    rating=models.IntegerField(default=0)
    feedback=models.TextField(max_length=300)
    def __unicode__(self):
        return self.user.username+" : "+self.event.name

class Notification(models.Model):
    event=models.ForeignKey(Event,related_name='notifevent')
    message=models.TextField(max_length=100)
    addedon=models.DateTimeField(auto_now=True)
    addedby=models.ForeignKey(User, null=True, blank=True)
    def __unicode__(self):
        return self.event.name+" : "+self.message[:20]


      
class UserFollow(models.Model):
    user=models.ForeignKey(User,related_name='followuser')
    club=models.ForeignKey(Club,related_name='followclub')
    follow=models.BooleanField(default=True)
    def __unicode__(self):
        return self.club.name+" : "+self.user.username
