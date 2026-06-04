from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EmployerProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	company_name = models.CharField(max_length=150)
	company_description = models.TextField(blank=True)
	contact_email = models.EmailField()
	phone_number = models.CharField(max_length=30, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.company_name