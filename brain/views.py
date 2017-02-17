from django.shortcuts import render
from django.views import generic,View
from . import template

class denied(View):
    def get(self,request):
        return render(request,template.denied_template)

class wait(View):
    def get(self,request):
        return render(request,template.wait_template)

def custom404(request):
    return render(request,'brain/404.html',{'error':"ERROR 404"})

def custom502(request):
    return render(request,'brain/404.html',{'error':"ERROR 502"})
