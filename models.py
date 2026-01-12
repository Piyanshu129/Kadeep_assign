"""
Data models for InternHub AI Platform
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class StudentProfile(BaseModel):
    """Student profile with skills, interests, education, and experience"""

    name: str = Field(..., description="Student's full name")
    email: Optional[str] = Field(None, description="Student's email")
    skills: List[str] = Field(..., description="List of technical and soft skills")
    interests: List[str] = Field(..., description="Areas of interest")
    education: str = Field(..., description="Current education level and major")
    experience: Optional[str] = Field(
        None, description="Previous work/internship experience"
    )
    projects: Optional[List[str]] = Field(None, description="Notable projects")
    certifications: Optional[List[str]] = Field(
        None, description="Relevant certifications"
    )


class InternshipDescription(BaseModel):
    """Internship job description"""

    title: str = Field(..., description="Internship title")
    company: str = Field(..., description="Company name")
    description: str = Field(..., description="Detailed job description")
    requirements: List[str] = Field(
        ..., description="Required skills and qualifications"
    )
    responsibilities: List[str] = Field(..., description="Key responsibilities")
    preferred_qualifications: Optional[List[str]] = Field(
        None, description="Nice-to-have qualifications"
    )
    duration: Optional[str] = Field(None, description="Internship duration")
    location: Optional[str] = Field(None, description="Location or remote")


class SkillGap(BaseModel):
    """Identified skill gap with learning recommendation"""

    skill: str = Field(..., description="Missing or weak skill")
    importance: str = Field(..., description="High/Medium/Low importance")
    learning_resources: List[str] = Field(..., description="Suggested learning paths")


class MatchResult(BaseModel):
    """Complete matching result"""

    match_summary: str = Field(..., description="Overall match assessment")
    match_score: float = Field(
        ..., ge=0, le=100, description="Match percentage (0-100)"
    )
    skill_gaps: List[SkillGap] = Field(..., description="Identified skill gaps")
    strengths: List[str] = Field(..., description="Student's strengths for this role")
    recommendations: str = Field(..., description="Actionable recommendations")
    tailored_resume: str = Field(..., description="ATS-optimized resume content")
    ats_confidence_score: float = Field(
        ..., ge=0, le=100, description="ATS confidence score (0-100)"
    )
    keyword_analysis: Dict[str, Any] = Field(
        ..., description="Keyword matching details"
    )


class MatchRequest(BaseModel):
    """API request for matching"""

    student_profile: StudentProfile
    internship: InternshipDescription
