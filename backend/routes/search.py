from flask import Blueprint, request, jsonify, session
from models import Candidate, Job, Employer
from database import db
import re

search_bp = Blueprint('search', __name__)


# Fuzzy matching helpers 

def fuzzy_score(query, text):
    """
    Returns a 0-100 fuzzy match score between query and text.
    Combines three signals:
      1. Exact substring match  → 100
      2. All query chars appear in order (subsequence) → 60
      3. Bigram overlap (handles typos like 'sofware enginer') → 0-50
    """
    if not query or not text:
        return 0
    q = query.lower().strip()
    t = text.lower().strip()

    # 1. Exact substring
    if q in t:
        return 100

    # 2. Subsequence check (handles abbreviations / partials)
    qi = 0
    for ch in t:
        if qi < len(q) and ch == q[qi]:
            qi += 1
    if qi == len(q):
        return 65

    # 3. Bigram similarity (handles transpositions and typos)
    def bigrams(s):
        return set(s[i:i+2] for i in range(len(s) - 1))

    q_bi = bigrams(q)
    t_bi = bigrams(t)
    if not q_bi:
        return 0
    overlap = len(q_bi & t_bi)
    sim = (2 * overlap) / (len(q_bi) + len(t_bi)) if (q_bi or t_bi) else 0
    return int(sim * 50)   # up to 50 points for bigram similarity


def fuzzy_match(query, text, threshold=30):
    """Returns True if fuzzy_score meets the threshold."""
    return fuzzy_score(query, text) >= threshold


def best_fuzzy_score(query, texts):
    """Returns the highest fuzzy score across a list of text fields."""
    return max((fuzzy_score(query, t) for t in texts if t), default=0)


# ── Salary parsing helper ──────────────────────────────────────────────────

def parse_salary(salary_str):
    """
    Extracts min and max salary from strings like:
      '$70,000 - $90,000'  →  (70000, 90000)
      '$65,000'            →  (65000, 65000)
      'Negotiable'         →  (None, None)
    """
    if not salary_str:
        return None, None
    numbers = re.findall(r'[\d,]+', salary_str.replace(',', ''))
    nums = [int(n.replace(',', '')) for n in re.findall(r'\d[\d,]*', salary_str)]
    if len(nums) >= 2:
        return min(nums), max(nums)
    elif len(nums) == 1:
        return nums[0], nums[0]
    return None, None


def salary_in_range(salary_str, min_sal, max_sal):
    """Returns True if the job salary overlaps with the requested range."""
    job_min, job_max = parse_salary(salary_str)
    if job_min is None:
        return False   # can't parse → exclude when filtering by salary
    # overlap check: job range overlaps with requested range
    return job_max >= min_sal and job_min <= max_sal


# ── Routes ─────────────────────────────────────────────────────────────────

@search_bp.route('/candidates', methods=['GET'])
def search_candidates():
    """Employer searches for candidates by keywords/skills with fuzzy matching."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    keyword  = request.args.get('keyword', '').strip()
    location = request.args.get('location', '').lower().strip()
    work_mode = request.args.get('work_mode', '').lower().strip()

    candidates = Candidate.query.all()
    results = []

    for c in candidates:
        if not c.full_name:
            continue

        matched_keywords = []
        score = 0

        if keyword:
            kw = keyword.lower()

            # fuzzy match each skill individually
            if c.skills:
                for skill in [s.strip() for s in c.skills.split(',')]:
                    fs = fuzzy_score(kw, skill.lower())
                    if fs >= 30:
                        matched_keywords.append(skill)
                        score += int(fs * 0.25)   # up to 25 pts per skill

            # fuzzy match job title
            if c.job_title:
                fs = fuzzy_score(kw, c.job_title.lower())
                if fs >= 30:
                    score += int(fs * 0.15)

            # fuzzy match bio
            if c.bio:
                fs = fuzzy_score(kw, c.bio.lower())
                if fs >= 40:
                    score += int(fs * 0.05)

        # hard filters (must match or skip)
        if location and c.location:
            if not fuzzy_match(location, c.location.lower(), threshold=40):
                continue
        elif location and not c.location:
            continue

        if work_mode and c.work_mode:
            if work_mode not in c.work_mode.lower():
                continue
        elif work_mode and not c.work_mode:
            continue

        if not keyword:
            score = 50

        if score > 0 or not keyword:
            candidate_data = c.to_dict()
            candidate_data['match_score'] = min(score, 100)
            candidate_data['matched_keywords'] = matched_keywords
            results.append(candidate_data)

    results.sort(key=lambda x: x['match_score'], reverse=True)
    return jsonify({'candidates': results}), 200


@search_bp.route('/jobs', methods=['GET'])
def search_jobs():
    """Candidate searches for jobs with fuzzy matching + salary range filter."""
    keyword   = request.args.get('keyword', '').strip()
    location  = request.args.get('location', '').lower().strip()
    work_mode = request.args.get('work_mode', '').lower().strip()
    sal_min   = request.args.get('salary_min', type=int)
    sal_max   = request.args.get('salary_max', type=int)

    jobs = Job.query.filter_by(is_active=True).all()
    results = []

    for job in jobs:
        score = 0
        matched = []

        if keyword:
            kw = keyword.lower()

            # fuzzy match title
            fs_title = fuzzy_score(kw, job.job_title.lower() if job.job_title else '')
            if fs_title >= 30:
                score += int(fs_title * 0.35)
                matched.append(job.job_title)

            # fuzzy match each required skill
            if job.required_skills:
                for skill in [s.strip() for s in job.required_skills.split(',')]:
                    fs = fuzzy_score(kw, skill.lower())
                    if fs >= 30:
                        score += int(fs * 0.20)
                        matched.append(skill)

            # fuzzy match description
            if job.job_description:
                fs_desc = fuzzy_score(kw, job.job_description.lower())
                if fs_desc >= 40:
                    score += int(fs_desc * 0.05)

        # location filter — fuzzy so "Brisbane" matches "Brisbane, QLD"
        if location and job.location:
            if not fuzzy_match(location, job.location.lower(), threshold=40):
                continue
        elif location and not job.location:
            continue

        # work mode filter — exact (remote/hybrid/on-site are short fixed words)
        if work_mode and job.work_mode:
            if work_mode not in job.work_mode.lower():
                continue
        elif work_mode and not job.work_mode:
            continue

        # salary range filter
        if sal_min is not None or sal_max is not None:
            mn = sal_min if sal_min is not None else 0
            mx = sal_max if sal_max is not None else 99999999
            if not salary_in_range(job.salary, mn, mx):
                continue

        if not keyword:
            score = 50

        if score > 0 or not keyword:
            job_data = job.to_dict()
            employer = db.session.get(Employer, job.employer_id)
            if employer:
                job_data['company_name'] = employer.company_name
            job_data['match_score'] = min(score, 100)
            job_data['matched_keywords'] = list(set(matched))
            results.append(job_data)

    results.sort(key=lambda x: x['match_score'], reverse=True)
    return jsonify({'jobs': results}), 200


@search_bp.route('/keywords-from-job', methods=['GET'])
def get_keywords_from_job():
    """Employer gets keywords extracted from their job posting."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401

    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'job_id is required'}), 400

    job = db.session.get(Job, job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    keywords = []
    if job.required_skills:
        keywords = [s.strip() for s in job.required_skills.split(',')]

    return jsonify({'keywords': keywords}), 200, 200
