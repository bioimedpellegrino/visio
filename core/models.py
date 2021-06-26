from django.db import models


class Access(models.Model):
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default=True, null=True)
    recognized = models.ForeignKey('TRecognized', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.created)

    class Meta:
        verbose_name = "Accesso"
        verbose_name_plural = "Accessi" 

class TCamera(models.Model):

    id = models.AutoField(primary_key=True)
    camera_id = models.IntegerField(blank=True, null=True)
    descr = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} - {}".format(self.camera_id, self.descr)

    class Meta:
        verbose_name = "Pi Camera"
        verbose_name_plural = "Pi Cameras"


class TImage(models.Model):

    id = models.AutoField(primary_key=True)
    face_num = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    camera = models.ForeignKey(TCamera, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return "{} - {} - {}".format(self.face_num, self.timestamp, self.camera.id)

    class Meta:
        verbose_name = "TImage"
        verbose_name_plural = "TImages"
    

class TRecognized(models.Model):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/recognized")

    def __str__(self):
        return "{} {} . Time: {}".format(self.first_name, self.last_name, self.timestamp)

    class Meta:
        verbose_name = "TRecognized"
        verbose_name_plural = "TRecognized"
