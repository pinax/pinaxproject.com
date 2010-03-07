import os

from datetime import datetime

from django.db import models

from downloads.verlib import NormalizedVersion as V



class Release(models.Model):
    
    version = models.CharField(max_length=10)
    stable = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ["-timestamp"]
    
    def __unicode__(self):
        return self.version
    
    @classmethod
    def latest_stable(cls):
        return cls._default_manager.filter(stable=True)[0]
    
    @classmethod
    def latest_development(cls):
        stable = cls.latest_stable()
        dev = cls._default_manager.filter(stable=False)[0]
        if V(dev.version) > V(stable.version):
            return dev
        else:
            return None


class ReleaseFile(models.Model):
    
    release = models.ForeignKey(Release)
    # @@@ needs to work with existing download system
    file = models.FileField(upload_to="downloads")
    md5_hash = models.CharField(max_length=32)
    sha1_hash = models.CharField(max_length=40)
    
    def file_type(self):
        return self.file.name.rsplit(".")[-1]
    
    def download_url(self):
        filename = os.path.basename(self.file.name)
        return "http://downloads.pinaxproject.com/%s" % filename
