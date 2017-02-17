from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from . import views
from . import submissionviews as subviews
from . import rankviews as rviews
from . import compileviews as cviews
from . import questionviews as qviews
from . import levelviews as lviews
from . import contestviews as contviews
from . import modviews as mviews
from . import views as t
app_name='brain'

urlpatterns=[
	url(r'^contest/getusers/(?P<contest_id>[0-9]+)$', contviews.GetUsers.as_view(), name='get_users'),
	url(r'^edit/(?P<pk>[0-9]+)$',qviews.DescriptionEdit.as_view(),name='edit_question'),
	url(r'^code/submit/(?P<pk>[0-9]+)$',qviews.CodeSubmit,name='code_submit'),
	url(r'^discussion/(?P<question_id>[0-9]+)$',qviews.discussion.as_view(),name='discussion'),
	url(r'^$',contviews.ContestIndex.as_view(),name='contest_index'),
	url(r'^submit/(?P<pk>[0-9]+)$',subviews.SubmissionAction.as_view(),name='question_submit'),
	url(r'^denied/',views.denied.as_view(),name='denied'),
	url(r'^wait/',views.wait.as_view(),name='wait'),
	url(r'^moderators/(?P<contest_id>[0-9]+)$',mviews.ModeratorList.as_view(),name='mod_list'),
	url(r'^passownership/(?P<contest_id>[0-9]+)$',mviews.PassOwnership.as_view(),name='pass_ownership'),
	url(r'^addmod/(?P<contest_id>[0-9]+)$',mviews.CreateModerator.as_view(),name='mod_create'),
	url(r'^removemod/(?P<contest_id>[0-9]+)$',mviews.RemoveModerator.as_view(),name='mod_remove'),
	url(r'^contest/index$',contviews.ContestIndex.as_view(),name='contest_index'),
	url(r'^create/contest$',contviews.ContestCreate.as_view(),name='contest_create'),
	url(r'^order/level/(?P<contest_id>[0-9]+)$',lviews.LevelOrder.as_view(),name='level_order'),
	url(r'^create/level/(?P<contest_id>[0-9]+)$',lviews.LevelCreate.as_view(),name='level_create'),
	url(r'^create/question/(?P<level_id>[0-9]+)$',qviews.QuestionCreate.as_view(),name='question_create'),
	url(r'^register/(?P<contest_id>[0-9]+)$',contviews.ContestRegistration.as_view(),name='contest_register'),
	url(r'^contest/(?P<contest_id>[0-9]+)$',contviews.ContestDetail.as_view(),name='contest_detail'),
	url(r'^level/(?P<level_id>[0-9]+)$',lviews.LevelDetail.as_view(),name='level_detail'),
	url(r'^question/(?P<question_id>[0-9]+)$',qviews.QuestionDetail.as_view(),name='question_detail'),
	url(r'^contest/(?P<pk>[0-9]+)/update$',contviews.ContestUpdate.as_view(),name='contest_update'),
	url(r'^level/(?P<pk>[0-9]+)/update$',lviews.LevelUpdate.as_view(),name='level_update'),
	url(r'^question/(?P<pk>[0-9]+)/update$',qviews.QuestionUpdate.as_view(),name='question_update'),
	url(r'^contest/(?P<pk>[0-9]+)/delete$',contviews.ContestDelete.as_view(),name='contest_delete'),
	url(r'^level/(?P<pk>[0-9]+)/delete$',lviews.LevelDelete.as_view(),name='level_delete'),
	url(r'^question/(?P<pk>[0-9]+)/delete$',qviews.QuestionDelete.as_view(),name='question_delete'),
	url(r'^ranklist/(?P<contest_id>[0-9]+)$',rviews.RanklistOfContest.as_view(),name='contest_rank'),
	url(r'^rank$',rviews.GlobalRanklist.as_view(),name='global_rank')
]

handler404='views.custom404'
handler502='views.custom502'
