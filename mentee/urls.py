from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from . import views

app_name='mentee'

urlpatterns=[
	url(r'^rate$', views.Submission_view.as_view(), name='submission'),
	url(r'^index$', views.SubmissionIndex.as_view(), name='submission_index'),
	url(r'^create$',views.CreateMentee.as_view(),name='create_mentee'),
]
