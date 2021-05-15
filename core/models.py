from django.db import models


class Access(models.Model):
    
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    note = models.TextField(default=True, null=True)
    
    
def __str__(self):
    return "{} {}".format(self.created)

class Meta:
    verbose_name = "Accesso"
    verbose_name_plural = "Accessi"