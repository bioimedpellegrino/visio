from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class DashboardView(View):

    template_name = 'core/main.html'
    
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)
