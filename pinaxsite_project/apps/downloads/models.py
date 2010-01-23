from datetime import datetime

from django.db import models



class Release(models.Model):
    
    version = models.CharField(max_length=10)
    stable = models.BooleanField()
    timestamp = models.DateTimeField(default=datetime.now)


class ReleaseFile(models.Model):
    
    file = models.FileField()
    md5_hash = models.CharField(max_length=32)
    sha1_hash = models.CharField(max_length=40)
