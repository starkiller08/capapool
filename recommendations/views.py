from django.shortcuts import render, get_object_or_404
from candidates.models import CandidateProfile
from jobs.models import JobPosting
from .services import get_top_10_jobs_for_candidate, get_top_10_candidates_for_job


# Create your views here.

def recommended_jobs(request):
	candidate = CandidateProfile.objects.first()

	results = []

	if candidate is not None:
		results = get_top_10_jobs_for_candidate(candidate)

	return render(request, 'recommendations/recommended_jobs.html', {
		'candidate': candidate,
		'results': results
	})


def recommended_candidates(request, job_id):
	# this function finds jobs by its ID, if it does not exist then a 404 page will be shown.
	job = get_object_or_404(JobPosting, id=job_id)

	results = get_top_10_candidates_for_job(job)

	return render(request, 'recommendations/recommended_candidates.html', {
		'job': job,
		'results': results
		})