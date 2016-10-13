from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    collegeName = models.CharField(max_length=128,default="NIT")
    signUpDate = models.DateField(auto_now=True)
    ipaddress = models.URLField(max_length=25)
    lastLoginDate = models.DateTimeField(blank=True)
    mobile_id=models.CharField(max_length=200)
    loggedIn=models.BooleanField(default=False)
    def __unicode__(self):
    	return self.user.username