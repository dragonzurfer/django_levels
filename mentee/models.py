from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Mentor(models.Model):
    user=models.OneToOneField(User)

    def __str__(self):
        return self.user.username

class Mentee(models.Model):
    name=models.CharField(max_length=200,unique=True)
    rank = models.IntegerField(default=0)
    mentor = models.ForeignKey(Mentor)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return None  # reverse('auth:index')


class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_number = models.IntegerField(default=0)

    def __str__(self):
        return self.task_name


class Submission(models.Model):
    time = models.DateTimeField(default=timezone.now)
    mentee = models.ForeignKey(Mentee)
    req_score = models.IntegerField(default=0)
    improv_score = models.IntegerField(default=0)
    time_score = models.IntegerField(default=0)
    task = models.ForeignKey(Task)
    url = models.CharField(max_length=1000)

    def __str__(self):
        return self.mentee.name
