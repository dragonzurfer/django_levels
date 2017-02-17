from .models import *
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic,View
from django.utils import timezone
from django.db.models import Sum
from . import template

class RanklistOfContest(generic.ListView):
    template_name='brain/ranklist.html'
    model=Contestant
    context_object_name='contestants'
    paginate_by=10
    userrank=0

    def get_context_data(self, **kwargs):
        context = super(RanklistOfContest, self).get_context_data(**kwargs)
        n=self.request.GET.get('page') 
        if n is not None:
            context['mul']=(int(n)-1)*int(self.paginate_by)
        else:
            context['mul']=0
        contest=get_object_or_404(Contest,id=self.kwargs['contest_id'])
        context['contest']=contest
        context['userrank']=self.userrank
        return context
    #qs-queryset cid-contestant id from orm dictionary
    def get_queryset(self):
        contestants=list()
        find=False
        userContestant=Contestant.objects.filter(profile__user=self.request.user)
        qs =Submission.objects.filter(question__level__contest__id=self.kwargs['contest_id'])
        contest_id=self.kwargs['contest_id']
        qs=qs.values('contestant_id',).annotate(time=Sum('time')).order_by('-contestant__points','time')
        
        if self.request.user.is_authenticated and userContestant.exists():
            find=True

        counter=0
        for i in qs:
            counter+=1
            cid=i.get('contestant_id')
            if find and cid==userContestant[0].id:
                self.userrank=counter
            instance=Contestant.objects.filter(id=cid)
            contestants.append(instance[0])
        print contestants
        return contestants

class GlobalRanklist(generic.ListView):
    template_name='brain/globalranklist.html'
    model=Contestant
    context_object_name='contestants'
    paginate_by=20
    userrank=0
    
    def get_context_data(self, **kwargs):
        context = super(GlobalRanklist, self).get_context_data(**kwargs)
        n=self.request.GET.get('page') 
        if n is not None:
            context['mul']=(int(n)-1)*int(self.paginate_by)
        else:
            context['mul']=0
        context['userrank']=self.userrank
        return context
    #qs-queryset cid=contestant id from orm dictionary
    def get_queryset(self):
        contestants=list()
        find=False
        if self.request.user.is_authenticated():
            userContestant=Contestant.objects.filter(profile__user=self.request.user)
            if userContestant.exists():
                find=True

        qs =Submission.objects.all()
        qs=qs.values('contestant_id',).annotate(time=Sum('time')).order_by('-contestant__points','time')

        counter=0
        for i in qs:
            counter+=1
            cid=i.get('contestant_id')
            if find and cid==userContestant[0].id:
                self.userrank=counter
            instance=Contestant.objects.filter(id=cid)
            contestants.append(instance[0])

        return contestants