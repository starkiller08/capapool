from django.shortcuts import render
from .models import CandidateProfile

# Create your views here.

def candidate_list(request):
	# shows all candidate profiles
	candidates = CandidateProfile.objects.all().order_by('-created_at')

	return render(request, 'candidates/candidate_list.html', {
		'candidates': candidates
	})


def candidate_search(request):
	# get filter values from the url
	skill = request.GET.get('skill', '')
	education = request.GET.get('education', '')
	experience = request.GET.get('experience', '')

	candidates = CandidateProfile.objects.all()

	# filter by skill name
	if skill:
		candidates = candidates.filter(skills__name__icontains=skill)

	# filter by exact education level
	if education:
		candidates = candidates.filter(education_level=education)

	# filter by minimum years of experience
	if experience:
		candidates = candidates.filter(years_of_experience__gte=experience)

	# distinct() avoids duplicate candidates if multiple skills match
	candidates = candidates.distinct()

	return render(request, 'candidates/candidate_search.html', {
		'candidates': candidates,
		'skill': skill,
		'education': education,
		'experience': experience
	})