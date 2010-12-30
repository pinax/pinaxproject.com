from datetime import datetime

from django.db import models



class Site(models.Model):
    
    name = models.CharField(
        verbose_name = "Site Name",
        max_length = 100
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="sites", blank=True)
    url = models.URLField(
        verbose_name = "URL",
        verify_exists = False
    )
    approved = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(default=datetime.now)
    when_approved = models.DateTimeField(null=True)
    contact_name = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField("contact e-mail", blank=True)
    
    def __unicode__(self):
        return "%s [%s]" % (self.name, self.url)
    
    def save(self, **kwargs):
        if self.featured:
            Site.objects.filter(featured=True).update(featured=False)
        super(Site, self).save(**kwargs)
