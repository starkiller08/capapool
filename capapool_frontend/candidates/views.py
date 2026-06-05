from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from employers.models import EmployerProfile
from .models import CandidateProfile
from .forms import CandidateProfileForm

from django.db.models import Q
from difflib import SequenceMatcher as sm

# Create your views here.


def is_fuzzy_match(search_text, target_text):
    if not search_text or not target_text:
        return False

    search_text = search_text.lower()
    target_text = target_text.lower()

    if search_text in target_text:
        return True

    similarity = sm(None, search_text, target_text).ratio()

    return similarity >= 0.65


def candidate_list(request):
	# shows all candidate profiles
	candidates = CandidateProfile.objects.all().order_by('-created_at')

	return render(request, 'candidates/candidate_list.html', {
		'candidates': candidates
	})


def candidate_search(request):
    query = request.GET.get('q', '').strip()
    skill = request.GET.get('skill', '').strip()
    education = request.GET.get('education', '').strip()
    experience = request.GET.get('experience', '').strip()
    preferred_location = request.GET.get('preferred_location', '').strip()
    preferred_work_mode = request.GET.get('preferred_work_mode', '').strip()

    candidates = CandidateProfile.objects.all()

    # Keyword search across candidate profile fields
    if query:
        candidates = candidates.filter(
            Q(full_name__icontains=query) |
            Q(contact_email__icontains=query) |
            Q(major__icontains=query) |
            Q(work_experience__icontains=query) |
            Q(preferred_location__icontains=query) |
            Q(preferred_work_mode__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()

        # If normal search returns nothing, try simple fuzzy search
        if not candidates.exists():
            all_candidates = CandidateProfile.objects.all().distinct()
            fuzzy_candidate_ids = []

            for candidate in all_candidates:
                skill_names = ' '.join(skill.name for skill in candidate.skills.all())

                searchable_text = ' '.join([
                    candidate.full_name,
                    candidate.contact_email,
                    candidate.major,
                    candidate.work_experience,
                    candidate.preferred_location,
                    candidate.preferred_work_mode,
                    skill_names,
                ])

                if is_fuzzy_match(query, searchable_text):
                    fuzzy_candidate_ids.append(candidate.id)

            candidates = CandidateProfile.objects.filter(id__in=fuzzy_candidate_ids)

    # Filters
    if skill:
        candidates = candidates.filter(skills__name__icontains=skill)

    if education:
        candidates = candidates.filter(education_level=education)

    if experience:
        candidates = candidates.filter(years_of_experience__gte=experience)

    if preferred_location:
        candidates = candidates.filter(preferred_location__icontains=preferred_location)

    if preferred_work_mode:
        candidates = candidates.filter(preferred_work_mode=preferred_work_mode)

    candidates = candidates.distinct().order_by('-created_at')

    return render(request, 'candidates/candidate_search.html', {
        'candidates': candidates,
        'query': query,
        'skill': skill,
        'education': education,
        'experience': experience,
        'preferred_location': preferred_location,
        'preferred_work_mode': preferred_work_mode,
        'education_choices': CandidateProfile.education_choices,
        'work_mode_choices': CandidateProfile.work_mode_choices,
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