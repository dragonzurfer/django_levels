from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect
from .models import Mentor,Submission,Mentee
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
            url=form.cleaned_data['url']
            url=url[0:4]
            if url!="http":
                return render(request,self.template_name,{'form':form})
            if Submission.objects.filter(mentee=mentee,task=task):
                return HttpResponse("<h1>BRO! YOU ALREADY FILLED IT FOR THIS GUY</h1>")
            else:
                if Mentee.objects.filter(name=mentee,mentor__user=self.request.user):
                    if improv_score <= 10 and time_score <= 10 and req_score <= 10 and improv_score >= 0 and time_score >=0 and req_score >=0:
                        form.save()
                    else:
                        return render(request,self.template_name,{'form':form})
                else:
                    return HttpResponse("<h1>BRO! NOT YOUR MENTEE</h1>")
            return HttpResponse("<h1>'K'ool</h1>")
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
    queryset=Submission.objects.order_by('task')
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
                        mentee_object.update(mentor=mentor)
                    elif mentee_object:
                        return HttpResponse("<h1>"+mentee+" is already a mentee")
                    else:
                        m=Mentee(name=mentee,mentor=mentor)
                        m.save()
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
