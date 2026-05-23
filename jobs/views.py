from django.shortcuts import render, redirect
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


def create_job(request):
	if request.method == 'POST':
		form = JobPostingForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('job_list')
	else:
		form = JobPostingForm()

	return render(request, 'jobs/create_job.html', {
		'form': form
	})