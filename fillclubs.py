import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventapp.settings')
from evm.models import Club

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

for c in CLUB_CHOICES:
    temp=Club()
    temp.name=c[0]
    temp.alias=c[1]
    temp.save()
