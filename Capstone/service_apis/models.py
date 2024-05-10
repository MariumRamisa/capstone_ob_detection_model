from django.db import models

# Create your models here.
class ImageInfo(models.Model):
    name = models.CharField(max_length=200,unique=True,blank=False,null=False)
    total_detected_objects = models.IntegerField(blank=True,null=True)
    detected_objects = models.JSONField(blank=True,null=True)
    time = models.CharField(max_length=100,blank=False,null=False)
    date = models.DateField(blank=False,null=False,auto_now_add=True)
    def __str__(self):
        return self.name
