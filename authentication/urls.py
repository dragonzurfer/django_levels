from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
app_name='auth'

urlpatterns = [
    #
    url(r'^$', views.UserRegistrationView.as_view(), name='authorize'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'^profile/(?P<profile_id>[0-9]+)$',views.profile_page.as_view(),name="profile_page"),
    url(r'^myprofile$',views.self_profile_page.as_view(),name="self_profile_page")
    ]