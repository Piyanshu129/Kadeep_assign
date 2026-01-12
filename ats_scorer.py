"""
ATS (Applicant Tracking System) Scoring Engine
Analyzes resume-job description match using keyword extraction and relevance scoring
"""

import re
from typing import Dict, List, Set
from models import StudentProfile, InternshipDescription
from config import ATS_WEIGHTS


def extract_keywords(text: str) -> Set[str]:
    """Extract meaningful keywords from text"""
    # Convert to lowercase and split
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())

    # Common stop words to exclude
    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "this",
        "that",
        "from",
        "will",
        "are",
        "have",
        "has",
        "been",
        "were",
        "was",
        "can",
        "our",
        "you",
        "your",
        "about",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "between",
        "under",
        "again",
        "further",
        "then",
        "once",
    }

    return {word for word in words if word not in stop_words}


def calculate_skill_match_score(
    student: StudentProfile, internship: InternshipDescription
) -> float:
    """Calculate skill match percentage"""
    student_skills = {skill.lower() for skill in student.skills}
    required_skills = {skill.lower() for skill in internship.requirements}

    if not required_skills:
        return 100.0

    matched_skills = student_skills.intersection(required_skills)
    return (len(matched_skills) / len(required_skills)) * 100


def calculate_experience_match(
    student: StudentProfile, internship: InternshipDescription
) -> float:
    """Calculate experience relevance score"""
    if not student.experience:
        return 30.0  # Base score for no experience

    # Extract keywords from experience and job description
    exp_keywords = extract_keywords(student.experience)
    job_keywords = extract_keywords(
        internship.description + " " + " ".join(internship.responsibilities)
    )

    if not job_keywords:
        return 50.0

    matched = exp_keywords.intersection(job_keywords)
    score = (len(matched) / len(job_keywords)) * 100

    # Cap at 100 and ensure minimum of 30
    return min(max(score, 30.0), 100.0)


def calculate_education_match(
    student: StudentProfile, internship: InternshipDescription
) -> float:
    """Calculate education relevance score"""
    education_lower = student.education.lower()
    job_text = (
        internship.description + " " + " ".join(internship.requirements)
    ).lower()

    # Check for degree level mentions
    degree_keywords = [
        "bachelor",
        "master",
        "phd",
        "undergraduate",
        "graduate",
        "degree",
    ]
    has_degree_mention = any(keyword in education_lower for keyword in degree_keywords)

    # Check for major/field relevance
    edu_keywords = extract_keywords(education_lower)
    job_keywords = extract_keywords(job_text)

    field_match = len(edu_keywords.intersection(job_keywords)) > 0

    if has_degree_mention and field_match:
        return 100.0
    elif has_degree_mention or field_match:
        return 70.0
    else:
        return 50.0


def calculate_keyword_density(
    student: StudentProfile, internship: InternshipDescription
) -> float:
    """Calculate keyword density score"""
    # Combine all student information
    student_text = " ".join(
        [
            " ".join(student.skills),
            student.education,
            student.experience or "",
            " ".join(student.projects or []),
            " ".join(student.certifications or []),
        ]
    )

    student_keywords = extract_keywords(student_text)

    # Extract job keywords
    job_text = " ".join(
        [
            internship.description,
            " ".join(internship.requirements),
            " ".join(internship.responsibilities),
            " ".join(internship.preferred_qualifications or []),
        ]
    )

    job_keywords = extract_keywords(job_text)

    if not job_keywords:
        return 50.0

    matched = student_keywords.intersection(job_keywords)
    density = (len(matched) / len(job_keywords)) * 100

    return min(density, 100.0)


def calculate_ats_score(
    student: StudentProfile, internship: InternshipDescription
) -> Dict:
    """
    Calculate comprehensive ATS score
    Returns dict with overall score and component breakdown
    """
    # Calculate individual components
    skill_score = calculate_skill_match_score(student, internship)
    experience_score = calculate_experience_match(student, internship)
    education_score = calculate_education_match(student, internship)
    keyword_score = calculate_keyword_density(student, internship)

    # Weighted overall score
    overall_score = (
        skill_score * ATS_WEIGHTS["skill_match"]
        + experience_score * ATS_WEIGHTS["experience_match"]
        + education_score * ATS_WEIGHTS["education_match"]
        + keyword_score * ATS_WEIGHTS["keyword_density"]
    )

    return {
        "overall_score": round(overall_score, 2),
        "breakdown": {
            "skill_match": round(skill_score, 2),
            "experience_match": round(experience_score, 2),
            "education_match": round(education_score, 2),
            "keyword_density": round(keyword_score, 2),
        },
        "matched_skills": list(
            {skill.lower() for skill in student.skills}.intersection(
                {skill.lower() for skill in internship.requirements}
            )
        ),
        "missing_skills": list(
            {skill.lower() for skill in internship.requirements}.difference(
                {skill.lower() for skill in student.skills}
            )
        ),
    }
