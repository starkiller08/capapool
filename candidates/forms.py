from django import forms
from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
	class Meta:
		model = CandidateProfile

		fields = [
			'user',
			'full_name',
			'contact_email',
			'phone_number',
			'education_level',
			'major',
			'years_of_experience',
			'resume',
			'preferred_location',
			'preferred_work_mode',
		]


		widgets = {
			'skills': forms.CheckboxSelectMultiple(),
		}