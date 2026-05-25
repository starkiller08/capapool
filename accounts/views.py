from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from .forms import CandidateRegisterForm, EmployerRegisterForm
from candidates.models import CandidateProfile
from employers.models import EmployerProfile

# Create your views here.

def home(request):
	return render(request, 'accounts/home.html')


def register_candidate(request):
	if request.method =="POST":
		form = CandidateRegisterForm(request.POST, request.FILES)

		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('dashboard')
	else:
		form = CandidateRegisterForm()

	return render(request, 'accounts/register.html', {
		'form': form,
		'page_title': 'Register as Candidate',
		'button_text': 'Create Candidate Account'
	})


def register_employer(request):
	if request.method == "POST":
		form = EmployerRegisterForm(request.POST)

		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('dashboard')
	else:
		form = EmployerRegisterForm()

	return render(request, 'accounts/register.html', {
		'form': form,
		'page_title': 'Register as Employer',
		'button_text': 'Create Employer Account'
	})


@login_required
def dashboard(request):
	candidate_profile = CandidateProfile.objects.filter(user=request.user).first()
	employer_profile = EmployerProfile.objects.filter(user=request.user).first()

	return render(request, 'accounts/dashboard.html', {
		'candidate_profile': candidate_profile,
		'employer_profile': employer_profile
	})


class UserLoginView(LoginView):
	template_name = 'accounts/login.html'


class UserLogoutView(LogoutView):
	next_page = 'home'