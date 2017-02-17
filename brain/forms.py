from django import forms
from .models import Level,Question

class LevelForm(forms.ModelForm):
    class Meta:
        model=Level
        fields=['name','points']

class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        fields=['name','author']
