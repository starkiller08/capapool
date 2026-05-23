from django.shortcuts import render, redirect, get_object_or_404
from .models import CandidateProfile
from .forms import CandidateProfileForm

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


def create_candidate_profile(request):
	if request.method == 'POST':
		form = CandidateProfileForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			return redirect('candidate_list')
	else:
		form = CandidateProfileForm()

	return render(request, 'candidates/candidate_form.html', {
		'form': form,
		'page_title': 'Create Candidate Profile',
		'button_text': 'Create Profile'
	})


def edit_candidate_profile(request, candidate_id):
	candidate = get_object_or_404(CandidateProfile, id=candidate_id)

	if request.method == 'POST':
		form = CandidateProfileForm(request.POST, request.FILES, instance=candidate)

		if form.is_valid():
			form.save()
			return redirect('candidate_list')
	else:
		form = CandidateProfileForm(instance=candidate)

	return render(request, 'candidates/candidate_form.html', {
		'form': form,
		'page_title': 'Edit Candidate Profile',
		'button_text': 'Save Changes'
	})