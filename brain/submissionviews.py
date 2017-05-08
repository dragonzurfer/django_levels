from .models import *
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic,View
from django.utils import timezone
from . import compileviews as cviews
from django.urls import reverse
from . import template

def CleanAnswer(answer):
    newAnswer=answer.replace(" ","")
    return newAnswer.lower()

"""
class SubmissionAction(LoginRequiredMixin,UserPassesTestMixin,View):
    can_get_points=False
    can_get_partial_points=False

    def post(self,request,pk):
        youranswer=self.request.POST.get('answer')
        youranswer=CleanAnswer(youranswer)
        myanswerlist=self.question.answer.split(";")
        if youranswer in  myanswerlist:
            if self.can_get_points:
                cnt=self.contestant[0]
                if self.can_get_partial_points:
                    cnt.profile.points += (self.level.points/5)
                    cnt.points += (self.level.points/5)
                else:
                    cnt.profile.points += self.level.points
                    cnt.points+=self.level.points
                cnt.profile.save()
                if cnt.level_number==self.level.number and self.can_get_partial_points is False:
                    cnt.level_number+=1
                cnt.save()
            if self.contestant.exists():
                submission=Submission(contestant=self.contestant[0],question=self.question,time=timezone.now())
                submission.save()
            return HttpResponse("<div style='color:green;'>Correct Answer</div>")

        return HttpResponse("<div style='color:red;'>Wrong Answer</div>")

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['pk'])
        self.level=self.question.level
        contest=self.level.contest
        self.contestant=Contestant.objects.filter(profile__user=self.request.user,contest=contest)
        submission=Submission.objects.filter(contestant=self.contestant,question=self.question)
        levelsubmission=Submission.objects.filter(contestant=self.contestant,question__level=self.level)
        if self.request.user.username==admin:
            return True
        elif Moderator.objects.filter(profile__user=self.request.user,contest=contest).exists():
            return True
        elif contest.end<timezone.now():
            return True
        elif submission.exists():
            self.can_get_points=False
            return True
        elif self.contestant.exists():
            if self.contestant[0].level_number>=self.level.number and contest.startmode:
                self.can_get_points=True
                if levelsubmission.exists():
                    self.can_get_partial_points = True
                return True
            else:
                return False
        else:
            return False
"""

class SubmissionAction(LoginRequiredMixin,UserPassesTestMixin,View):
    can_get_points=False
    can_get_partial_points=False
    mod=False
    owner=False
    showall=False
    def post(self,request,pk):
        youranswer=self.request.POST.get('answer')
        yourcode=self.request.POST.get('code')
        myanswerlist=self.question.answer.split(";")
        language=self.request.POST.get('language')
        if yourcode is None:#if no code was given
            youranswer=CleanAnswer(youranswer)
        else:
            youranswer=cviews.compile(yourcode,language)
            if youranswer=='ERROR IN CODE':
                return render(self.request,template.denied_template,{'error':'compilation error'})
            youranswer=youranswer['output']#hackerearth return an extra \n for each output
            cnt=0
            for i in myanswerlist:
                i=i+"\n"
                i=i.replace('\r','')#'enter' in a textariea adds a '\r\n' instead of just '\n' to the answer
                myanswerlist[cnt]=i
                cnt+=1
        if youranswer in  myanswerlist:
            level_set=Level.objects.filter(contest__id=self.contest.id).order_by('number')#prepare for returning to contest detail page
            if self.can_get_points:
                cnt=self.contestant[0]
                if self.can_get_partial_points:
                    cnt.profile.points += (self.level.points / 5)
                    cnt.points += (self.level.points / 5)
                else:
                    cnt.profile.points += self.level.points
                    cnt.points += self.level.points
                cnt.profile.save()
                if cnt.level_number == self.level.number and self.can_get_partial_points is False:
                    cnt.level_number += 1
                cnt.save()
                if self.contestant.exists():
                    submission=Submission(contestant=self.contestant[0],question=self.question,time=timezone.now())
                    submission.save()
                #redirect to contest detail saying Level Up
                return render(self.request,template.contest_detail_template,{'level_up':True,'contestant':self.contestant[0],'showall':self.showall,'contest':self.contest,'level_set':level_set,'mod':self.mod,'owner':self.owner})
            if self.contestant.exists():
                return render(self.request,template.contest_detail_template,{'contestant':self.contestant[0],'showall':self.showall,'contest':self.contest,'level_set':level_set,'mod':self.mod,'owner':self.owner})
            else:
                return render(self.request,template.contest_detail_template,{'showall':self.showall,'contest':self.contest,'level_set':level_set,'mod':self.mod,'owner':self.owner})
        return HttpResponse("<div style='color:red;'>Wrong Answer</div>")

    def get_login_url(self):
        return u'/denied'

    def test_func(self):
        self.question=get_object_or_404(Question,id=self.kwargs['pk'])
        self.level=self.question.level
        self.contest=self.level.contest
        moderator=Moderator.objects.filter(profile__user=self.request.user,contest=self.contest)
        self.contestant=Contestant.objects.filter(profile__user=self.request.user,contest=self.contest)
        submission=Submission.objects.filter(contestant=self.contestant,question=self.question)
        levelsubmission = Submission.objects.filter(contestant=self.contestant, question__level=self.level)
        if self.request.user.is_superuser:# CHECK 1.ADMIN (OWNER,MOD)
            self.owner=True
            self.mod=True
            return True
        elif moderator.exists():            #CHECK 2.MODERATOR (MOD)
            self.mod=True
            if moderator[0].isowner:        #Show owners options
                self.owner=True
            return True
        elif self.contest.end<timezone.now():#CHECK 3 CONTEST IS OVER
            self.showall=True               #LET USER SEE ALL LEVELS
            return True
        elif submission.exists():            #CHECK 4 SUBMITION EXISTS (DONT GIVE POINTS TO USER )
            self.can_get_points=False
            return True
        elif self.contestant.exists():      #CHECK 5 CONTESTANT EXISTS
            if self.contestant[0].level_number >= self.level.number and self.contest.startmode:
                self.can_get_points = True
                if levelsubmission.exists():
                    self.can_get_partial_points = True
                return True
            else:
                return False
        else:
            return False
