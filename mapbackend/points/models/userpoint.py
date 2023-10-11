from mapbackend.models import TimeStampMixin
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User

class UserPoint(TimeStampMixin):
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  label_text = models.CharField(max_length=255)
  position = models.PointField(geography=True, default=Point(24.9384, 60.1699))


  def __str__(self):
    return f"Point at ({self.position.x}, {self.position.y}), \"{self.label_text}\" "
