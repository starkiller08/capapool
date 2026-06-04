from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from candidates.models import CandidateProfile
from employers.models import EmployerProfile
from jobs.models import JobPosting
from .services import get_top_10_jobs_for_candidate, get_top_10_candidates_for_job


# Create your views here.

@login_required
def recommended_jobs(request):
	candidate_profile = CandidateProfile.objects.filter(user=request.user).first()


	if candidate_profile is None:
		messages.error(request, 'Only candidates can view recommended jobs.')
		return redirect('dashboard')

	results = get_top_10_jobs_for_candidate(candidate_profile)

	return render(request, 'recommendations/recommended_jobs.html', {
		'candidate': candidate_profile,
		'results': results
	})


@login_required
def recommended_candidates(request, job_id):
	employer_profile = EmployerProfile.objects.filter(user=request.user).first()

	if employer_profile is None:
		messages.error(request, 'Only employers can view recommended candidates.')
		return redirect('dashboard')

	# this function finds jobs by its ID, if it does not exist then a 404 page will be shown.
	job = get_object_or_404(JobPosting, id=job_id, employer=employer_profile)

	results = get_top_10_candidates_for_job(job)

	return render(request, 'recommendations/recommended_candidates.html', {
		'job': job,
		'results': results
		})