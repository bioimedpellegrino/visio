from django.shortcuts import render
from django.views.generic import View
from django.db.models import Count
from .models import *

# Create your views here.


class DashboardView(View):

    template_name = 'core/main.html'
    
    def get(self, request, *args, **kwargs):
        accessi = TImage.objects.all()
        counter = 0
        for accesso in accessi:
            counter += accesso.face_num
        
        result = {'counter' : counter}
        return render(request, self.template_name, result)


class ActivateDeactivateCamera(View):
     
     template_name = 'core/main.html'
     
     
     def get(self, request, *args, **kwargs):
        accessi = TImage.objects.all()
        camera = TCamera.objects.get(pk=1)
        camera.is_active = not camera.is_active
        camera.save()
        counter = 0
        for accesso in accessi:
            counter += accesso.face_num
        
        result = {'counter' : counter, 'is_active': camera.is_active }
        return render(request, self.template_name, result)

      
     def post(self, request, *args, **kwargs):
         camera = TCamera.objects.get(pk=1)
         camera.is_active = not camera.is_active
         camera.save()

         accessi = TImage.objects.all()
         counter = 0
         for accesso in accessi:
             counter += accesso.face_num
         
         result = {'counter' : counter, 'is_active': camera.is_active}
         return render(request, self.template_name, result)

         
