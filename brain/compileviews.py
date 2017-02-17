from .models import *
from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic,View
from django.utils import timezone
from django.db.models import Sum
import requests

RUN_URL = u'http://api.hackerearth.com/code/run/'
CLIENT_SECRET = '1c100833313afc6f52908596859c1d762b82c362'
languages=['C', 'CPP', 'CPP11', 'CLOJURE', 'CSHARP', 'JAVA', 'JAVASCRIPT', 'HASKELL', 'PERL', 'PHP', 'PYTHON', 'RUBY']

def compile(code,lang,input_for_code=""):
	if lang in languages:
		if input_for_code:
			data = {
    		'client_secret': CLIENT_SECRET,
    		'async': 0,
    		'source': code,
    		'input':input_for_code,
    		'lang': lang,
    		'time_limit': 5,
    		'memory_limit': 262144,
			}
		else:
			data = {
    		'client_secret': CLIENT_SECRET,
    		'async': 0,
    		'source': code,
    		'lang': lang,
    		'time_limit': 5,
    		'memory_limit': 262144,
			}
		result={}
		r = requests.post(RUN_URL, data=data)
		r=r.json()
		compileStatus=r['compile_status']

		if compileStatus=='OK':
			rs=r['run_status']
			time=rs['time_used']
			youranswer=rs['output']
			youranswer_html=rs['output_html']
			result={'time':time,'output_html':youranswer_html,'output':youranswer}
			return result
		else:
			return "ERROR IN CODE"
