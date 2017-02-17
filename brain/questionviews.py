from .models import *
from .forms import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic,View
from django.utils import timezone
from .submissionviews import CleanAnswer
from django.urls import reverse
from . import template

class DescriptionEdit(LoginRequiredMixin,UserPassesTestMixin,UpdateView):

    def get(self,request,pk):
        old_description=self.question.description
        return render(request,template.markdowneditor_template,{'old_description':old_description,'question':self.question})

    def post(self,request,pk):
        content=request.POST.get('content')
        self.question.description=content
        self.question.save()
        return HttpResponseRedirect(reverse('brain:question_detail',args=(self.question.id,),current_app=request.resolver_match.namespace))

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['pk'])
        print self.question
        level=self.question.level
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=level.contest).exists():
            return True
        else:
            return False

def CodeSubmit(request,pk):
    return render(request,template.code_submit_template,{'pk':pk})

class discussion(LoginRequiredMixin,UserPassesTestMixin,View):
    def get(self,request,question_id):
        return render(request,template.discussion_template)

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['question_id'])
        contest=self.question.level.contest
        contestant=Contestant.objects.filter(profile__user=self.request.user,contest=contest)
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=contest).exists():
            return True
        elif contest.end<timezone.now():
            return True
        elif contestant.exists():
            if contestant[0].level_number>=self.question.level.number and contest.startmode:
                return True
            else:
                return False
        else:
            return False

class QuestionCreate(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name=template.question_form_template
    form_class=QuestionForm

    def get(self,request,level_id):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form,'level':self.level})

    def post(self,request,level_id):
        form=self.form_class(self.request.POST)
        if(form.is_valid()):
            name=form.cleaned_data['name']
            author=form.cleaned_data['author']
            #answer=form.cleaned_data['answer']
            #answer=CleanAnswer(answer)
            #description=form.cleaned_data['description']
            self.level.question_set.create(name=name,author=author)
            self.level.save()
            return HttpResponseRedirect(reverse('brain:level_detail',args=(self.level.id,),current_app=request.resolver_match.namespace))
        return render(request,self.template_name,{'form':form})

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        self.level=get_object_or_404(Level,id=self.kwargs['level_id'])
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=self.level.contest).exists():
            if self.level.contest.startmode:
                return False
            return True
        else:
            return False

class QuestionDelete(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
    model=Question
    question=""
    def get_success_url(self):
        return reverse_lazy('brain:level_detail',args=(self.question.level.id,))

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['pk'])
        level=self.question.level
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=level.contest).exists():
            if level.contest.startmode:
                return False
            return True
        else:
            return False

class QuestionDetail(LoginRequiredMixin,UserPassesTestMixin,View):

    mod=False
    def get(self,request,question_id):
        return render(self.request,template.question_detail_template,{'question':self.question,'mod':self.mod})

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['question_id'])
        contest=self.question.level.contest
        contestant=Contestant.objects.filter(profile__user=self.request.user,contest=contest)
        if self.request.user.is_superuser:
            self.mod=True
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=contest).exists():
            self.mod=True
            return True
        elif contest.end<timezone.now():
            return True
        elif contestant.exists():
            if contestant[0].level_number>=self.question.level.number and contest.startmode:
                return True
            else:
                return False
        else:
            return False


class QuestionUpdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Question
    template_name=template.question_update_template
    fields=['name','answer','author']

    def get_success_url(self):
        answer=CleanAnswer(self.object.answer)
        self.object.answer=answer
        self.object.save()
        return reverse_lazy('brain:level_detail',args=(self.question.level.id,))

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['pk'])
        level=self.question.level
        if self.request.user.is_superuser:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=level.contest).exists():
            return True
        else:
            return False
