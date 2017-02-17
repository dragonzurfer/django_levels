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
from django.http import JsonResponse

class ContestRegistration(LoginRequiredMixin,UserPassesTestMixin,View):
    contest=""
    def get(self,request,contest_id):
        return render(self.request,template.contest_register_template,{'contest':self.contest})

    def post(self,request,contest_id):
        profile=get_object_or_404(Profile,user=self.request.user)
        contestant=Contestant(contest=self.contest,profile=profile)
        contestant.save()
        return HttpResponseRedirect(reverse('brain:contest_detail',args=(contest_id,),current_app=self.request.resolver_match.namespace))

    def test_func(self):
        self.contest=get_object_or_404(Contest,id=self.kwargs['contest_id'])#CHECK 1 ADMIN
        if Moderator.objects.filter(profile__user=self.request.user,contest=self.contest).exists():
            return False#CHECK 2 MODERATOR
        elif Contestant.objects.filter(profile__user=self.request.user,contest=self.contest).exists():
            return False # CHECK 3 ALREADY A CONTESTANT
        else:
            return True


class ContestIndex(PaginationMixin,generic.ListView):
    template_name=template.contest_index_template
    queryset=Contest.objects.order_by('-start')
    context_object_name='contest_list'
    paginate_by =3

    def get_context_data(self, **kwargs):
        context = super(ContestIndex, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ContestCreate(LoginRequiredMixin,PermissionRequiredMixin,generic.CreateView):
    model=Contest
    fields=['name','description','start','end']
    success_url=reverse_lazy('brain:contest_index')
    permission_required='brain.add_contest'

    def get_login_url(self):
        return u"/denied"



class ContestDetail(LoginRequiredMixin,UserPassesTestMixin,View):
    wait=False
    mod=False
    owner=False
    currentlevel=0
    showall=False
    def get(self,request,contest_id):
        level_set=Level.objects.filter(contest__id=contest_id).order_by('number')
        contestant=Contestant.objects.filter(contest=self.contest,profile__user=self.request.user)
        if contestant.exists():
            contestant=contestant[0]
        return render(self.request,template.contest_detail_template,{'contestant':contestant,'showall':self.showall,'contest':self.contest,'level_set':level_set,'mod':self.mod,'owner':self.owner})

    def get_login_url(self):
        if self.wait:
            return u'/wait'
        return u'/register/'+self.kwargs['contest_id']

    def test_func(self):
        moderator=Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['contest_id'])
        self.contest=get_object_or_404(Contest,id=self.kwargs['contest_id'])
        contestant=Contestant.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['contest_id'])
        if self.request.user.is_superuser:#CHECK 1 ADMIN
            self.mod=True
            self.owner=True
            return True
        elif moderator.exists():                       #CHECK 2 MODERATOR
            self.mod=True
            if moderator[0].isowner:                    #CHECK OWNERSHIP
                self.owner=True
            return True
        elif self.contest.startmode:                    #CHECK 3 startmode
            if self.contest.end<timezone.now():
                self.showall=True
                return True
            elif contestant.exists():                  #CHECK 4 CONTESTANT
                if self.contest.start>timezone.now():#CHECK 5 START
                    self.wait=True
                    return False
                else:
                    self.currentlevel=contestant[0].level_number
                    return True
        elif not contestant.exists():                  #CHECK 6 NOT A CONTESTANT (REGISTER)
            return False
        else:
            self.wait=True                            #ELSE WAIT FOR IT
            return False


class ContestUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Contest
    fields=['name','description','start','end','startmode']
    success_url=reverse_lazy('brain:contest_index')
    template_name=template.contest_update_template

    def form_valid(self, form):
        if self.object.level_ordered:
            return super(ContestUpdate, self).form_valid(form)
        else:
            return HttpResponseRedirect(reverse('brain:level_order',args=(self.object.pk,),current_app=self.request.resolver_match.namespace))

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        if self.request.user.is_superuser:#CHECK 1 ADMIN
            return True
        check=Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['pk'])
        if check.exists():#CHECK IF MODERATOR EXIST
            if check[0].isowner:#CHECK IF IS OWNER
                contest=get_object_or_404(Contest,id=self.kwargs['pk'])
                if contest.startmode:#CHECK IF CONTEST IN STARTMODE
                    return False
                return True
            return False
        else:
            return False

class ContestDelete(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    model=Contest
    success_url=reverse_lazy('brain:contest_index')

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        check=Moderator.objects.filter(profile__user=self.request.user,contest__id=self.kwargs['pk'])

        if self.request.user.is_superuser:
            return True
        elif check.exists():
            if check[0].isowner:
                contest=get_object_or_404(Contest,id=self.kwargs['pk'])
                if contest.startmode:
                    return False
                return True
            return False
        else:
            return False

class GetUsers(View):

    def get(self, request, contest_id):
        contestant = Contestant.objects.filter(contest__id=contest_id).count()
        data = {'count': contestant}
        return JsonResponse(data)
