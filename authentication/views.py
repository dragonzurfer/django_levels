from django.contrib.auth import logout,authenticate, login
from django.shortcuts import render
from django.urls import reverse
from django.views import generic,View
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.utils.decorators import method_decorator  #used to apply @login_required to function within class check @method_moderator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UserRegisterForm
from django.template import loader
from .models import Profile
from brain.models import *
from django.contrib.auth.models import User
import datetime
# Create your views here.
profile_page_template='authentication/profile_page.html'
signup_template='authentication/signup.html'

class UserRegistrationView(View):
    form_class=UserRegisterForm
    template_name=signup_template

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)
        if(form.is_valid()):
            user=form.save(commit=False)
            username=form.cleaned_data.get('username')
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                username_error='Username'+username+' Taken! choose another one'
                return render(request,self.template_name,{'form':form,'error':username_error})
            if len(username)<=2:
                too_short='username too short min(3)!'
                return render(request,self.template_name,{'form':form,'error':too_short})
            if User.objects.filter(email=email).exists():
                email_exist='user with email'+email+' exists'
                return render(request,self.template_name,{'form':form,'error':email_exist})
            if len(password)<=5:
                pass_short='password too short min(6)!'
                return render(request,self.template_name,{'form':form,'error':pass_short})

            user.set_password(password)
            user.save()
            user=authenticate(username=username,password=password)
            if(user is not None):
                if user.is_active:
                    login(request,user)
                    return redirect('brain:contest_index')
        return render(request,self.template_name,{'form':form})

class profile_page(View):
    def get(self,request,profile_id):
        profile=get_object_or_404(Profile,id=profile_id)
        contestant=Contestant.objects.filter(profile_id=profile_id)
        submissions=list()
        for c in contestant:
            s=Submission.objects.filter(contestant=c).order_by('time')
            submissions.append(s)
        return render(request,profile_page_template,{'profile':profile,'submissions':submissions,
                    'contestant':contestant})

class self_profile_page(LoginRequiredMixin,View):
    def get(self,request):
        profile=get_object_or_404(Profile,user=self.request.user)
        contestant=Contestant.objects.filter(profile_id=profile.id)
        submissions=list()
        for c in contestant:
            s=Submission.objects.filter(contestant=c).order_by('time')
            submissions.append(s)
        return render(request,profile_page_template,{'profile':profile,'submissions':submissions,
                    'contestant':contestant})

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('brain:contest_index'))
    else:
        return render(request,'authentication/signup.html',{'error':"Invalid Credentials"})

def logout_view(request):
    logout(request)
    return redirect('brain:contest_index')

