from django.contrib import admin
from .models import CandidateProfile, Skill

# Register your models here.

#admin.site.register(CandidateProfile)
#admin.site.register(Skill)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	search_fields = ['name']


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
	list_display = [
		'full_name',
		'education_level',
		'major',
		'years_of_experience',
		'preferred_work_mode',
		'preferred_location',
		'is_member',
	]

	list_filter = [
		'education_level',
		'preferred_work_mode',
		'is_member',
	]

	search_fields = [
		'full_name',
		'major',
		'work_experience',
	]

	filter_horizontal = ['skills']