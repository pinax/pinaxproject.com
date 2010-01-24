from datetime import datetime

from django.db import models



class Quote(models.Model):
    
    text = models.TextField()
    author = models.CharField(max_length=100)
    added = models.DateTimeField(default=datetime.now)
    featured = models.BooleanField(default=False)
    
    def save(self, **kwargs):
        if self.featured:
            Quote.objects.filter(featured=True).update(featured=False)
        super(Site, self).save(**kwargs)
