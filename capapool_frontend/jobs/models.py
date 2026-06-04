from django.db import models
from employers.models import EmployerProfile
from candidates.models import Skill

# Create your models here.

class JobPosting(models.Model):
	education_choices = [
		('high_school', 'High School'),
		('diploma', 'Diploma'),
		('bachelor', 'Bachelor'),
		('master', 'Master'),
		('phd', 'PhD'),
	]

	work_mode_choices = [
		('remote', 'Remote'),
		('onsite', 'On-site'),
		('hybrid', 'Hybrid'),
	]

	employer = models.ForeignKey(
		EmployerProfile,
		on_delete=models.CASCADE,
		related_name='job_postings'
	)

	job_title = models.CharField(max_length=150)
	job_description = models.TextField()
	required_education_level = models.CharField(max_length=50, choices=education_choices)
	required_skills = models.ManyToManyField(Skill, blank=True)
	required_years_of_experience = models.PositiveIntegerField(default=0)
	work_mode = models.CharField(max_length=30, choices=work_mode_choices)
	job_location = models.CharField(max_length=100)

	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.job_title