from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='mentee'

urlpatterns=[
	url(r'^rate$', views.Submission_view.as_view(), name='submission'),
	url(r'^index$', views.SubmissionIndex.as_view(), name='submission_index'),
	url(r'^create$',views.CreateMentee.as_view(),name='create_mentee'),
	url(r'^induction',csrf_exempt(views.test),name='inductions'),
	url(r'^uPdAtE$', views.EloRating.as_view(), name='elo_rating'),
	url(r'^rating$', views.Rating.as_view(), name='rating'),
]
