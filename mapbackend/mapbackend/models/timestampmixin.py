from django.contrib.gis.db import models


class TimeStampMixin(models.Model):
    """Simple abstract Model class that adds "created" and "modified"-columns."""    
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
