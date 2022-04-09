from turtle import mode
from django.db import models

class Camera(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=True, blank=True, default='Visio standard camera')
    desc = models.TextField(null=True, blank=True)
    user_selection = models.CharField(max_length=200, null=True, blank=True, default="")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Videocamera"
        verbose_name_plural = "Videocamere"
        
        
class Entity(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, null=True, blank=True, default="")
    desc = models.TextField(null=True, blank=True)
    site = models.CharField(max_length=2048, null=True, blank=True)
    camera = models.ForeignKey(Camera, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Person(models.Model):
    """
    """ 
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=1024, null=True, default="")
    last_name = models.CharField(max_length=1024, null=True, default="")
    birth_date = models.DateField(null=True, blank=True)
    face_image = models.FileField(upload_to="picture/portraits")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class VisioRecognition(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.CASCADE)
    age = models.CharField(max_length=1024, null=True, blank=True, default="")
    gender = models.CharField(max_length=10, null=True, blank=True, default="")
    emotion = models.CharField(max_length=1024, null=True, blank=True, default="")

class ImageData(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    face_num = models.PositiveIntegerField(default=0, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to="pictures/acquisition")
    entity = models.ForeignKey(Entity, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Metadati"
        verbose_name_plural = "Immagini - Metadati"
