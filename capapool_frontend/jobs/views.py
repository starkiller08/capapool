from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from employers.models import EmployerProfile
from .models import JobPosting
from .forms import JobPostingForm

from django.db.models import Q
from difflib import SequenceMatcher as sm
# Create your views here.

def job_list(request):
	# show all active jobs, newest first
	jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')

	return render(request, 'jobs/job_list.html', {
		'jobs': jobs
	})


def is_fuzzy_match(search_text, target_text):
	if not search_text or not target_text:
		return False

	search_text = search_text.lower()
	target_text = target_text.lower()

	if search_text in target_text:
		return True

	similarity = sm(None, search_text, target_text).ratio()

	return similarity >= 0.65


def job_search(request):
	# get the search word from the URL, example: /jobs/search/?q=python
	query = request.GET.get('q', '').strip()
	location = request.GET.get('location', '').strip()
	work_mode = request.GET.get('work_mode', '').strip()
	education = request.GET.get('education', '').strip()
	experience = request.GET.get('experience', '').strip()

	jobs = JobPosting.objects.filter(is_active=True)

	if query:
		# search will be from job description
		jobs = jobs.filter(
			Q(job_title__icontains=query) |
			Q(job_description__icontains=query) |
			Q(job_location__icontains=query) |
			Q(work_mode__icontains=query) |            
			Q(employer__company_name__icontains=query) |           
			Q(employer__company_description__icontains=query) |            
			Q(required_skills__name__icontains=query)
		).distinct()        

		# If normal search returns nothing, try simple fuzzy search        
		if not jobs.exists():
			all_jobs = JobPosting.objects.filter(is_active=True).distinct()
			fuzzy_job_ids = []

			for job in all_jobs:
				skill_names = ' '.join(skill.name for skill in job.required_skills.all())

				searchable_text = ' '.join([
					job.job_title,
					job.job_description,
					job.job_location,
					job.work_mode,
					job.employer.company_name,
					job.employer.company_description,
					skill_names,
				])

				if is_fuzzy_match(query, searchable_text):
					fuzzy_job_ids.append(job.id)

			jobs = JobPosting.objects.filter(id__in=fuzzy_job_ids)    
	

	# Filters    
	if location:
		jobs = jobs.filter(job_location__icontains=location)


	if work_mode:
		jobs = jobs.filter(work_mode=work_mode)


	if education:
		jobs = jobs.filter(required_education_level=education)


	if experience:
		jobs = jobs.filter(required_years_of_experience__lte=experience)    


	jobs = jobs.distinct().order_by('-created_at')


	return render(request, 'jobs/job_search.html', {
		'jobs': jobs,
		'query': query,
		'location': location,
		'work_mode': work_mode,
		'education': education,
		'experience': experience,
		'work_mode_choices': JobPosting.work_mode_choices,
		'education_choices': JobPosting.education_choices,
	})

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