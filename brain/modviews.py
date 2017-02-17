from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from .forms import *
from authentication.models import *
from django.urls import reverse
from django.views import generic,View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination.mixins import PaginationMixin
from django.utils import timezone
from . import template

class CreateModerator(LoginRequiredMixin,UserPassesTestMixin,View):

    def get(self,request,contest_id):
        return render(self.request,template.add_mod_template,{'contest_id':contest_id})

    def post(self,request,contest_id):
        username=self.request.POST.get('username')
        contest_id=self.kwargs['contest_id']
        if not User.objects.filter(username=username).exists():
            return render(self.request,template.add_mod_template,{'error':"username does not exists",'contest_id':contest_id})
        if Moderator.objects.filter(profile__user__username=username,contest__id=contest_id).exists():
            return render(self.request,template.add_mod_template,{'error':"Moderator exists for this Contest",'contest_id':contest_id})
        user=get_object_or_404(Profile,user__username=username)
        contest=get_object_or_404(Contest,id=contest_id)
        mod=Moderator(profile=user,contest=contest)
        mod.save()
        return HttpResponseRedirect(reverse('brain:mod_list',args=(contest_id,),current_app=self.request.resolver_match.namespace))

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        if Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['contest_id']).exists():
            return True
        else:
            return False

class RemoveModerator(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,contest_id):
        return render(self.request,template.pass_ownership_template,{'contest_id':contest_id})

    def post(self,redirect,contest_id):
        username=self.request.POST.get('username')
        if not User.objects.filter(username=username).exists():
            return render(self.request,template.add_mod_template,{'error':"username does not exists",'contest_id':contest_id})
        check=Moderator.objects.filter(profile__user__username=username,contest__id=contest_id)
        if not check.exists():
            return render(self.request,template.add_mod_template,{'error':"User is not moderator",'contest_id':contest_id})
        moderator=check[0]
        moderator.delete()
        return HttpResponseRedirect(reverse('brain:mod_list',args=(contest_id,),current_app=self.request.resolver_match.namespace))
    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        moderator=Moderator.objects.filter(contest_id=self.kwargs['contest_id'],profile__user=self.request.user)
        if moderator.exists():
            moderator=moderator[0]
            if moderator.isowner:
                return True
            else:
                return False

class ModeratorList(LoginRequiredMixin,UserPassesTestMixin,View):
    owner=False
    mod=False
    def get(self,request,contest_id):
        moderators=Moderator.objects.filter(contest__id=contest_id)
        return render(self.request,template.moderators_list_template,{'moderators':moderators,'contest_id':contest_id,'mod':self.mod,'owner':self.owner})

    def test_func(self):
        check=Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['contest_id'])
        if self.request.user.is_superuser:
            self.mod=True
            self.owner=True
            return True
        elif check.exists():
            self.mod=True
            if check[0].isowner:
                self.owner=True
            return True
        else:
            return False

class PassOwnership(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,contest_id):
        return render(self.request,template.pass_ownership_template,{'contest_id':contest_id})

    def post(self,request,contest_id):
        username=self.request.POST['username']
        if not User.objects.filter(username=username).exists():
            return render(self.request,template.add_mod_template,{'contest_id':contest_id,'error':'username does not exist'})
        moderator=Moderator.objects.filter(contest_id=self.kwargs['contest_id'],profile__user__username=username)
        if moderator.exists():
            moderator=moderator[0]
            moderator.isowner=True
            moderator.save()
            if not self.request.user.is_superuser:
                remove=get_object_or_404(Moderator,contest_id=self.kwargs['contest_id'],profile__user=self.request.user)
                remove.isowner=False
                remove.save()
            return HttpResponseRedirect(reverse('brain:mod_list',args=(contest_id,),current_app=self.request.resolver_match.namespace))
        return render(self.request,template.add_mod_template,{'contest_id':contest_id,'error':'user is not in moderators list'})

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        moderator=Moderator.objects.filter(contest_id=self.kwargs['contest_id'],profile__user=self.request.user)
        if moderator.exists():
            moderator=moderator[0]
            if moderator.isowner:
                return True
            else:
                return False
        else:
            return False
