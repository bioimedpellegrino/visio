from django.contrib import admin
from .models import *

admin.site.register(Person)
admin.site.register(Entity)
admin.site.register(Camera)
admin.site.register(VisioRecognition)
admin.site.register(ImageData)
