from datetime import datetime

from django.db import models

from biblion.models import Post



class FeaturedPost(models.Model):
    
    post = models.ForeignKey(Post)
    timestamp = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ["-timestamp"]
