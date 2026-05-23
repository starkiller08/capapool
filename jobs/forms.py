from django import forms
from .models import JobPosting


class JobPostingForm(forms.ModelForm):
	class Meta:
		model = JobPosting

		fields = [
			'employer',
			'job_title',
			'job_description',
			'required_education_level',
			'required_skills',
			'required_years_of_experience',
			'work_mode',
			'job_location',
			'is_active',
		]


		widgets = {
			'job_description': forms.Textarea(attrs={
				'rows': 5,
				'placeholder': 'Enter the job description here...'
				}),
			'required_skills': forms.CheckboxSelectMultiple(),
		}