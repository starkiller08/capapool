from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skill(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name


class CandidateProfile(models.Model):
	education_choices = [
		('high_school', 'High School'),
		('diploma', 'Diploma'),
		('bachelor', 'Bachelor'),
		('master', 'Master'),
		('phd', 'PhD'),
	]


	user = models.OneToOneField(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=150)
	contact_email = models.EmailField()
	phone_number = models.CharField(max_length=30, blank=True)
	education_level = models.CharField(max_length=50, choices=education_choices)
	major = models.CharField(max_length=100)
	years_of_experience = models.PositiveIntegerField(default=0)
	skills = models.ManyToManyField(Skill, blank=True)
	resume = models.FileField(upload_to='resume/', blank=True, null=True)
	preferred_location = models.CharField(max_length=100, blank=True)
	preferred_work_mode = models.CharField(max_length=30, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.full_name