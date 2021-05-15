from django.contrib import admin
from .models import Access

class AccessAdmin(admin.ModelAdmin):
    filters = ['created']
    

admin.site.register(Access, AccessAdmin)