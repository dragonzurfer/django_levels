from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Contest)
admin.site.register(Level)
admin.site.register(Question)
admin.site.register(Moderator)
admin.site.register(Contestant)
admin.site.register(Submission)