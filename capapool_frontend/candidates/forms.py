from django import forms
from .models import CandidateProfile


class CandidateProfileForm(forms.ModelForm):
	skills = forms.CharField(required=False, label='skills', help_text='Enter skills separated by commas, e.g. Python, Django, etc.')

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
			#'skills': forms.CheckboxSelectMultiple(),
		}


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			current_skills = self.instance.skills.all()
			skill_names = []

			for skill in current_skills:
				skill_names.append(skill.name)

			self.fields['skills'].initial = ', '.join(skill_names)


	def save(self, commit=True):
		candidate = super().save(commit=False)


		if commit:
			candidate.save()

            # Clear old skills first, then add the updated skills
			candidate.skills.clear()

			skills_text = self.cleaned_data.get('skills', '')

			if skills_text:
				skill_names = skills_text.split(',')

				for skill_name in skill_names:
					clean_skill_name = skill_name.strip()

					if clean_skill_name:
						skill, created = Skill.objects.get_or_create(
							name=clean_skill_name
						)
						candidate.skills.add(skill)

		return candidate