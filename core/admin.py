from django.contrib import admin
from .models import *

class AccessAdmin(admin.ModelAdmin):
    filters = ['created']
    
class TCameraAdmin(admin.ModelAdmin):
    pass

class TImageAdmin(admin.ModelAdmin):
    pass

class TRecognizedAdmin(admin.ModelAdmin):
    pass

admin.site.register(TCamera, TCameraAdmin)
admin.site.register(TImage, TImageAdmin)
admin.site.register(Access, AccessAdmin)
admin.site.register(TRecognized, TRecognizedAdmin)
