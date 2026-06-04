from django.contrib import admin
from .models import CandidateProfile, Skill

# Register your models here.

admin.site.register(CandidateProfile)
admin.site.register(Skill)