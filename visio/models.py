from turtle import mode
from django.db import models

class Camera(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=True, blank=True, default='Visio standard camera')
    desc = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Videocamera"
        verbose_name_plural = "Videocamere"
        
        
class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=True, blank=True, default="")
    desc = models.TextField(null=True, blank=True)
    site = models.CharField(max_length=2048, null=True, blank=True)
    camera = models.ForeignKey(Camera, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


