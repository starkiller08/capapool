from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from candidates.models import CandidateProfile
from employers.models import EmployerProfile


class CandidateRegisterForm(UserCreationForm):
	email = forms.EmailField()
	full_name = forms.CharField(max_length=150)
	phone_number = forms.CharField(max_length=30, required=False)
	education_level = forms.ChoiceField(choices=CandidateProfile.education_choices)
	major = forms.CharField(max_length=100)
	years_of_experience = forms.IntegerField(min_value=0)
	skills = forms.ModelMultipleChoiceField(queryset=CandidateProfile.skills.field.related_model.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
	resume = forms.FileField(required=False)
	preferred_location = forms.CharField(max_length=100, required=False)
	preferred_work_mode = forms.CharField(max_length=30, required=False)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def save(self):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		user.save()

		candidate = CandidateProfile.objects.create(
			user = user,
			full_name = self.cleaned_data['full_name'],
			phone_number = self.cleaned_data['phone_number'],
			education_level = self.cleaned_data['education_level'],
			major = self.cleaned_data['major'],
			years_of_experience = self.cleaned_data['years_of_experience'],
			resume = self.cleaned_data.get('resume'),
			preferred_location = self.cleaned_data['preferred_location'],
			preferred_work_mode = self.cleaned_data['preferred_work_mode']
		)

		candidate.skills.set(self.cleaned_data['skills'])

		return user


class EmployerRegisterForm(UserCreationForm):
	email = forms.EmailField()
	company_name = forms.CharField(max_length=150)
	company_description = forms.CharField(widget=forms.Textarea, required=False)
	phone_number = forms.CharField(max_length=30, required=False)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def save(self):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		user.save()

		EmployerProfile.objects.create(
			user = user,
			company_name = self.cleaned_data['company_name'],
			company_description = self.cleaned_data['company_description'],
			phone_number = self.cleaned_data['phone_number']
		)

		return user