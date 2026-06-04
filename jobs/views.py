from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from employers.models import EmployerProfile
from .models import JobPosting
from .forms import JobPostingForm

# Create your views here.

def job_list(request):
	# show all active jobs, newest first
	jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')

	return render(request, 'jobs/job_list.html', {
		'jobs': jobs
	})


def job_search(request):
	# get the search word from the URL, example: /jobs/search/?q=python
	query = request.GET.get('q', '')
	jobs = JobPosting.objects.filter(is_active=True)

	if query:
		# search will be from job description
		jobs = jobs.filter(job_description__icontains=query)

	return render(request, 'jobs/job_search.html', {
		'jobs': jobs,
		'query': query
	})


@login_required
def create_job(request):
	employer_profile = EmployerProfile.objects.filter(user=request.user).first()
	
	if employer_profile is None:
		messages.error(request, 'Only employers can create job postings.')
		return redirect('dashboard')

	if request.method == 'POST':
		form = JobPostingForm(request.POST)

		if form.is_valid():
			job = form.save(commit=False)
			job.employer = employer_profile
			job.save()
			form.save_m2m()
			return redirect('job_list')

			messages.success(request, 'Job posting created successfully.')
			return redirect('my_jobs')
	else:
		form = JobPostingForm()

	return render(request, 'jobs/create_job.html', {
		'form': form
	})


@login_required
def my_jobs(request):
	employer_profile = EmployerProfile.objects.filter(user=request.user).first()

	if employer_profile is None:
		messages.error(request, 'Only employers can view their own job postings.')
		return redirect('dashboard')

	jobs = JobPosting.objects.filter(employer=employer_profile).order_by('-created_at')

	return render(request, 'jobs/my_jobs.html', {
		'jobs': jobs,
		'employer_profile': employer_profile
	})

@login_required
def edit_job(request, job_id):
	employer_profile = EmployerProfile.objects.filter(user=request.user).first()

	if employer_profile is None:
		messages.error(request, 'Only employers can edit job postings.')
		return redirect('dashboard')

	job = get_object_or_404(JobPosting, id=job_id, employer=employer_profile)

	if request.method == 'POST':
		form = JobPostingForm(request.POST, instance=job)

		if form.is_valid():
			form.save()
			messages.success(request, 'Job posting updated successfully.')
			return redirect('my_jobs')
	else:
		form = JobPostingForm(instance=job)

	return render(request, 'jobs/edit_job.html', {
		'form': form,
		'job': job
	})