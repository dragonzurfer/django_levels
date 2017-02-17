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

class LevelOrder(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,contest_id):
        return render(self.request,template.level_order_template,{'level_set':self.level_set,'contest_id':self.contest.id})

    def post(self,request,contest_id):
        query=self.request.POST.getlist('level_order')
        neworder=query[0].split(',')
        newordertemps = neworder
        [newordertemp.encode('utf-8') for newordertemp in newordertemps]
        queryCount = len(newordertemp)
        cnt=0
        if self.checkLevelOrder(newordertemp, queryCount) is False:
            return u'/denied'
        for lvl in self.level_set:
            lvl.number=neworder[cnt]
            cnt+=1
            lvl.save()
        self.contest.startmode=True
        self.contest.level_ordered=True
        self.contest.save()
        return HttpResponseRedirect(reverse('brain:contest_detail',args=(self.contest.id,),current_app=request.resolver_match.namespace))
    def checkLevelOrder(self, newOrder, queryCount):
        for i in range(1, queryCount, 1):
            if(i not in newOrder):
                return False
        return True
    def get_login_url(self):
        return u'/denied'
    def test_func(self):
        self.contest=get_object_or_404(Contest,pk=self.kwargs['contest_id'])
        self.level_set=Level.objects.filter(contest=self.contest).order_by('number')
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['contest_id']).exists():
            if self.contest.startmode:
                return False
            return True
        else:
            return False


class LevelUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Level
    fields=['name','points']
    template_name =template.level_update_template

    def get_success_url(self):
        return reverse_lazy('brain:level_detail',args=(self.kwargs['pk']))

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        level=get_object_or_404(Level,id=self.kwargs['pk'])
        if self.request.user.is_superuser :
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=level.contest).exists():
            if level.contest.startmode:
                return False
            return True
        else:
            return False

class LevelDelete(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name=template.level_delete_template
    def get(self,request,pk):
        return render(request,self.template_name,{'contest':self.contest})

    def post(self,request,pk):
        delete_level =get_object_or_404(Level,pk=self.request.POST.get('level'))
        delete_level.delete()
        self.contest.level_ordered=False
        self.contest.save()
        return HttpResponseRedirect(reverse('brain:contest_detail',args=(self.contest.id,),current_app=request.resolver_match.namespace))

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        self.contest = get_object_or_404(Contest, pk=self.kwargs['pk'])
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=self.contest).exists():
            if self.contest.startmode:
                return False
            return True
        else:
            return False

class LevelDetail(LoginRequiredMixin,UserPassesTestMixin,View):
    mod=False
    def get(self,request,level_id):
        return render(self.request,template.level_detail_template,{'level':self.level,'mod':self.mod})

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        level=get_object_or_404(Level,id=self.kwargs['level_id'])
        self.level=level
        contest=get_object_or_404(Contest,id=level.contest.id)
        contestant=Contestant.objects.filter(profile__user=self.request.user,contest=level.contest)

        if self.request.user.is_superuser:
            self.mod=True
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=level.contest).exists():
            self.mod=True
            return True
        elif contest.end<timezone.now():
            return True
        elif contestant.exists():
            if contestant[0].level_number>=level.number and contest.startmode:
                return True
        else:
            return False

class LevelCreate(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name=template.level_form_template
    form_class=LevelForm
    contest=""
    def get(self,request,contest_id):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form,'contest':self.contest})

    def post(self,request,contest_id):
        form=self.form_class(self.request.POST)
        if(form.is_valid()):
            level_name=form.cleaned_data['name']
            points=form.cleaned_data['points']
            level_number=0
            self.contest.level_set.create(name=level_name,points=points,number=level_number)
            self.contest.level_ordered=False
            self.contest.save()
            return HttpResponseRedirect(reverse('brain:contest_detail',args=(self.contest.id,),current_app=request.resolver_match.namespace))
        return render(request,self.template_name,{'form':form})

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        self.contest=get_object_or_404(Contest,pk=self.kwargs['contest_id'])
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['contest_id']).exists():
            if self.contest.startmode:
                return False
            return True
        else:
            return False
