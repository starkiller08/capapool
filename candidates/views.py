from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from employers.models import EmployerProfile
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


@login_required
def my_candidate_profile(request):
	candidate_profile = CandidateProfile.objects.filter(user=request.user).first()

	if candidate_profile is None:
		messages.error(request, 'You do not have a candidate profile yet.')
		return redirect('dashboard')

	return render(request, 'candidates/my_candidate_profile.html', {
		'candidate': candidate_profile
	})


@login_required
def create_candidate_profile(request):
	employer_profile = EmployerProfile.objects.filter(user=request.user).first()

	if employer_profile is not None:
		messages.error(request, 'Employer accounts cannot create candidate profiles.')
		return redirect('dashboard')

	existing_profile = CandidateProfile.objects.filter(user=request.user).first()

	if existing_profile is not None:
		messages.info(request, 'You already have a candidate profile.')
		return redirect('my_candidate_profile')

	if request.method == 'POST':
		form = CandidateProfileForm(request.POST, request.FILES)

		if form.is_valid():
			candidate = form.save(commit=False)
			candidate.user = request.user
			candidate.save()
			form.save_m2m()

			messages.success(request, 'Candidate profile created successfully.')
			return redirect('my_candidate_profile')
	else:
		form = CandidateProfileForm()

	return render(request, 'candidates/candidate_form.html', {
		'form': form,
		'page_title': 'Create Candidate Profile',
		'button_text': 'Create Profile'
	})



@login_required
def edit_candidate_profile(request, candidate_id):
    if request.user.is_staff:
        candidate_profile = get_object_or_404(CandidateProfile, id=candidate_id)
    else:
        candidate_profile = get_object_or_404(
            CandidateProfile,
            id=candidate_id,
            user=request.user
        )

    if request.method == 'POST':
        form = CandidateProfileForm(
            request.POST,
            request.FILES,
            instance=candidate_profile
        )

        if form.is_valid():
            form.save()
            return redirect('candidate_list')
    else:
        form = CandidateProfileForm(instance=candidate_profile)

    return render(request, 'candidates/candidate_form.html', {
        'form': form,
        'page_title': 'Edit Candidate Profile',
        'button_text': 'Save Changes'
    })


@login_required
def edit_my_candidate_profile(request):
	candidate_profile = CandidateProfile.objects.filter(user=request.user).first()
	
	#candidate = get_object_or_404(CandidateProfile, id=candidate_id)
	if candidate_profile is None:
		messages.error(request, 'You need to create a candidate profile first.')
		return redirect('create_candidate_profile')


	if request.method == 'POST':
		form = CandidateProfileForm(request.POST, request.FILES, instance=candidate_profile)

		if form.is_valid():
			form.save()
			messages.success(request, 'Candidate profile updated successfully.')
			return redirect('my_candidate_profile')
	else:
		form = CandidateProfileForm(instance=candidate_profile)

	return render(request, 'candidates/candidate_form.html', {
		'form': form,
		'page_title': 'Edit My Candidate Profile',
		'button_text': 'Save Changes'
	})