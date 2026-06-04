from django import forms
from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
	class Meta:
		model = CandidateProfile

		fields = [
			'full_name',
			'contact_email',
			'phone_number',
			'education_level',
			'major',
			'years_of_experience',
			'work_experience',
			'skills',
			'resume',
			'preferred_location',
			'preferred_work_mode',
		]


		widgets = {
			'work_experience': forms.Textarea(attrs={
				'rows': 4,
				'placeholder': 'Briefly describe your past work experience....'
			}),
			'skills': forms.CheckboxSelectMultiple(),
		}