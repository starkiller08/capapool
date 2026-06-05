from jobs.models import JobPosting
from candidates.models import CandidateProfile


def calculate_job_match_score(candidate, job):
	score = 0


	candidate_skills = set(candidate.skills.values_list('name', flat=True))
	job_skills = set(job.required_skills.values_list('name', flat=True))

	if job_skills:
		matched_skills = candidate_skills.intersection(job_skills)
		skill_score = (len(matched_skills) / len(job_skills)) * 40
		score += skill_score


	if candidate.education_level == job.required_education_level:
		score += 20


	if candidate.years_of_experience >= job.required_years_of_experience:
		score += 20
	else:
		experience_ratio = candidate.years_of_experience / max(job.required_years_of_experience, 1)
		score += experience_ratio * 20


	if candidate.preferred_location and candidate.preferred_location.lower() == job.job_location.lower():
		score += 10


	if candidate.preferred_work_mode and candidate.preferred_work_mode.lower() == job.work_mode.lower():
		score += 10


	return round(score, 2)


def get_top_10_jobs_for_candidate(candidate):
	jobs = JobPosting.objects.filter(is_active=True)

	scored_jobs = []

	for job in jobs:
		score = calculate_job_match_score(candidate, job)
		scored_jobs.append({
			'job': job,
			'score': score
		})

	scored_jobs.sort(key=lambda item: item['score'], reverse=True)

	if candidate.is_member:
		return scored_jobs


	return scored_jobs[:10]


def calculate_candidate_match_score(candidate, job):
	return calculate_job_match_score(candidate, job)


def get_top_10_candidates_for_job(job):
	candidates = CandidateProfile.objects.all()

	scored_candidates = []

	for candidate in candidates:
		score = calculate_candidate_match_score(candidate, job)
		scored_candidates.append({
			'candidate': candidate,
			'score': score
		})

	scored_candidates.sort(key=lambda item: item['score'], reverse=True)

	if job.employer.is_member:
		return scored_candidates
		

	return scored_candidates[:10]

