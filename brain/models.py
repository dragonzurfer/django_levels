from __future__ import unicode_literals
from django.db import models
from authentication.models import Profile
from django.utils import timezone

class Contest(models.Model):
	name=models.CharField(max_length=30)
	description=models.TextField(max_length=10000)
	start=models.DateTimeField(default=timezone.now)
	end=models.DateTimeField()
	startmode=models.BooleanField(default=False)
	level_ordered=models.BooleanField(default=False)
	def __str__(self):
		return self.name

class Moderator(models.Model):
	profile=models.ForeignKey(Profile)
	isowner=models.BooleanField(default=False)
	contest=models.ForeignKey(Contest)

	def __str__(self):
		return self.profile.user.username

class Contestant(models.Model):
	profile=models.ForeignKey(Profile)
	contest=models.ForeignKey(Contest)
	points=models.IntegerField(default=0)
	level_number=models.IntegerField(default=1)

	def __str__(self):
		return self.profile.user.username


class Level(models.Model):
	name=models.CharField(max_length=50)
	contest=models.ForeignKey(Contest)
	number=models.IntegerField()
	points=models.IntegerField()

	def __str__(self):
		return self.name

class Question(models.Model):
	name=models.CharField(max_length=50)
	description=models.TextField(max_length=20000)
	author=models.ForeignKey(Moderator)
	level=models.ForeignKey(Level)
	answer=models.TextField(max_length=50000)
	def __str__(self):
		return self.name

class Submission(models.Model):
	time=models.DateTimeField(default=timezone.now)
	contestant=models.ForeignKey(Contestant)
	question=models.ForeignKey(Question)

	def __str__(self):
		return self.contestant.profile.user.username
