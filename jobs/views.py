from django.shortcuts import render
from .models import JobPosting

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