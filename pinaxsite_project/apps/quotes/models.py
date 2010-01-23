from datetime import datetime

from django.db import models



class Quote(models.Model):
    
    text = models.TextField()
    author = models.CharField(max_length=100)
    added = models.DateTimeField(default=datetime.now)
