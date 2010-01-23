from datetime import datetime

from django.db import models



class Site(models.Model):
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="sites")
    url = models.URLField(verify_exists=False)
    approved = models.BooleanField()
    created = models.DateTimeField(default=datetime.now)
    when_approved = models.DateTimeField(null=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
