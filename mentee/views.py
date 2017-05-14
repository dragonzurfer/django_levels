from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect
from .models import Mentor,Submission,Mentee,Task
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
from . import forms
import requests
import json
import bot

def getMentorsMentees(mentor_name=None):
    text=""
    if mentor_name is not None:
        try:
            mentees_of_mentor=Mentee.objects.filter(mentor__user__username=mentor_name)
        except:
            return "ERROR"
        if mentees_of_mentor.exists():
            text+=str(mentor_name)+"\n-----------------\n"
            i=1
            for mentee in mentees_of_mentor:
                text+=str(i)+" ."+str(mentee.name)+"\n"
                i+=1
        else:
            text="username not found"
            return text
    else:
        mentor_list=Mentor.objects.all()
        if not mentor_list.exists():
            return "EMPTY"
        for mentor in mentor_list:
            mentees_of_mentor=Mentee.objects.filter(mentor=mentor)
            i=1
            for mentee in mentees_of_mentor:
                text+=str(i)+" ."+str(mentee.name)+"\n"
                i+=1
    return text

def getSubmission(task_number=None,mentor_name=None):
    text=""
    if task_number and mentor_name:
        try:
            submissions=Submission.objects.filter(task__task_number=task_number,mentee__mentor__user__username=mentor_name)
        except:
            return "ERROR"
        if submissions.exists():
            for sub in submissions:
                text+="\n"+str(sub.mentee.name)+"("+str(sub.req_score)+","+str(sub.improv_score)+","+str(sub.time_score)+")\n"
                text+="link:"+str(sub.url)
                text+="\n \n"+str(mentor.user.username)+"\n-----------------\n"
        else:
            return "EMPTY"
    elif task_number:
        try:
            submissions=Submission.objects.filter(task__task_number=task_number)
        except:
            return "ERROR"
        if submissions.exists():
            for sub in submissions:
                text+="\n"+str(sub.mentee.mentor)+"--rated-->"+str(sub.mentee.name)+"("+str(sub.req_score)+","+str(sub.improv_score)+","+str(sub.time_score)+")\n"
                text+="link:"+str(sub.url)
        else:
            return "EMPTY"
    else:
        text="error"
    return text

url=bot.bot_url

def test(request):
    payload = json.loads(request.body.decode('utf-8'))
    chat_id = payload['message']['chat']['id']
    msg = payload['message'].get('text')  # command
    slice_msg=msg.split()
    cmd = msg.split()[0]
    text=cmd
    if cmd == "/mentee":
        if len(slice_msg)==2:
            text=getMentorsMentees(slice_msg[1])
        else:
            text=getMentorsMentees()
    elif cmd == "/task":
        if len(slice_msg)==2:
            text=getSubmission(slice_msg[1])
        elif len(slice_msg)==3:
            text=getSubmission(slice_msg[1],slice_msg[2])
        requests.post(url,data={'chat_id':chat_id,'text':text})
    return HttpResponse(200)

chat_id=bot.group_chat_id
const=0.00008267195
class Submission_view(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name=template.submission
    form_class=forms.SubmissionForm

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(self.request.POST)
        if(form.is_valid()):
            time=form.cleaned_data['time']
            req_score=form.cleaned_data['req_score']
            improv_score=form.cleaned_data['improv_score']
            mentee=form.cleaned_data['mentee']
            time_score=form.cleaned_data['time_score']
            task=form.cleaned_data['task']
            url_sub=form.cleaned_data['url']
            url_check=url_sub[0:4]
            if url_check!="http":
                return render(request,self.template_name,{'form':form})
            if Submission.objects.filter(mentee=mentee,task=task):
                return HttpResponse("<h1>BRO! YOU ALREADY FILLED IT FOR THIS GUY</h1>")
            else:
                if Mentee.objects.filter(name=mentee,mentor__user=self.request.user):
                    if improv_score <= 10 and req_score <= 10 and improv_score >= 0 and req_score >=0:
                        form.save()
                        saved_sub=Submission.objects.filter(mentee=mentee,task=task)
                        seconds=(task.deadline-timezone.now()).total_seconds()
                        seconds=int(seconds)
                        time_score=int(seconds*const)
                        if time_score <-50:
                            time_score=-50
                        saved_sub.update(time_score=time_score)
                        text=str(self.request.user.username)+'--rated-->'+str(mentee)+':task '+str(task.task_number)+'('+str(time_score)+','+str(req_score)+','+str(improv_score)+')'+' \n  link:'+str(url_sub)
                        #r=requests.post(url,data={'chat_id':chat_id,'text':text})
                    else:
                        return render(request,self.template_name,{'form':form})
                else:
                    return HttpResponse("<h1>BRO! NOT YOUR MENTEE</h1>")
            return HttpResponse("<h1>'K'ool'</h1>")
        return render(request,self.template_name,{'form':form})

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        if Mentor.objects.filter(user=self.request.user):
            return True
        else:
            return False

class SubmissionIndex(PaginationMixin,generic.ListView):
    template_name=template.submission_index_template
    queryset=Submission.objects.order_by('task__task_number')
    context_object_name='submission_list'
    paginate_by =100

    def get_context_data(self, **kwargs):
        context = super(SubmissionIndex, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class CreateMentee(LoginRequiredMixin,UserPassesTestMixin,View):
    template_name=template.create_mentee

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        mentee_list=str(self.request.POST.get('mentee_list'))
        mentee_list=mentee_list.replace(' ','').replace('\r', '').replace('\n', '')
        mentor_mentees=mentee_list.split(":")
        mentor_mentees.pop(-1)
        for ml in mentor_mentees:
            mentees=ml.replace(' ','').replace('\r', '').replace('\n', '').split(',')
            mentor=""
            try:
                mentor=mentees.pop(0)
            except:
                pass
            registered=""
            if Mentor.objects.filter(user__username=mentor):
                for mentee in mentees:
                    mentor=get_object_or_404(Mentor,user__username=mentor)
                    mentee_object=Mentee.objects.filter(name=mentee)

                    if mentee_object and mentee_object[0].mentor!=mentor:
                        text=str(self.request.user.username)+' reassigned '+str(mentee)+' to '+str(mentor.user.username)
                        #r=requests.post(url,data={'chat_id':chat_id,'text':text})
                        mentee_object.update(mentor=mentor)
                    elif mentee_object:
                        return HttpResponse("<h1>"+mentee+" is already a mentee")
                    else:
                        m=Mentee(name=mentee,mentor=mentor)
                        m.save()
                        text=str(self.request.user.username)+' made '+str(mentor.user.username)+' mentor to '+str(mentee)
                        #r=requests.post(url,data={'chat_id':chat_id,'text':text})
                        registered=registered+'<br>'
            else:
                return HttpResponse("<h1>"+mentor+" is not mentor")
        return HttpResponse("<h1>'k'ool</h1>")

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        if self.request.user.is_superuser:
            if Mentor.objects.filter(user=self.request.user):
                return True
            else:
                m=Mentor(user=self.request.user)
                m.save()
            return True
        else:
            return False

def calc_sum_for_submission(submission):
    total_score=int(submission.req_score)+int(submission.time_score)+int(submission.improv_score)
    return total_score

import elo_rating

class EloRating(LoginRequiredMixin,UserPassesTestMixin,View):
    recalculate=False
    def get(self,request):
        if self.recalculate:
            get_tasks=Task.objects.all()
            mentee_list=Mentee.objects.all()
            matrix=[]
            for task in get_tasks:
                task_score_list=[]
                for mentee in mentee_list:
                    mentee_submission_for_task=Submission.objects.filter(task=task,mentee=mentee)
                    if mentee_submission_for_task.exists():
                        sum_score=calc_sum_for_submission(mentee_submission_for_task[0])
                        task_score_list.append(sum_score)
                    else:
                        task_score_list.append(0)
                matrix.append(task_score_list)
            print matrix
            new_rating=elo_rating.elo_rating(matrix)
            print new_rating
            index=0
            for mentee in mentee_list:
                if mentee.rank!=new_rating[index]:
                    mentee.rank=new_rating[index]
                    mentee.save()
                index+=1
        return HttpResponse(200)

    def get_login_url(self):
        return u"/denied"

    def test_func(self):
        if self.request.user.is_superuser:
            self.recalculate=True
            return True
        else:
            return False
