"""
AI Engine for InternHub - Handles LLM interactions for matching, analysis, and resume generation
"""

import json
from typing import Dict, List
from openai import OpenAI
from models import StudentProfile, InternshipDescription, SkillGap, MatchResult
from ats_scorer import calculate_ats_score
from config import VLLM_BASE_URL, VLLM_API_KEY, VLLM_MODEL, MAX_TOKENS, TEMPERATURE


class AIEngine:
    """AI Engine using local vLLM for internship matching"""

    def __init__(self):
        self.client = OpenAI(base_url=VLLM_BASE_URL, api_key=VLLM_API_KEY)

    def _call_llm(self, system_prompt: str, user_prompt: str) -> str:
        """Make a call to the vLLM API"""
        try:
            response = self.client.chat.completions.create(
                model=VLLM_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API call failed: {str(e)}")

    def analyze_match(
        self, student: StudentProfile, internship: InternshipDescription
    ) -> str:
        """Generate match summary using LLM"""
        system_prompt = """You are an expert career counselor and internship matching specialist. 
Analyze the student profile against the internship description and provide a comprehensive match assessment.
Be honest, constructive, and specific in your analysis."""

        user_prompt = f"""
Student Profile:
- Name: {student.name}
- Education: {student.education}
- Skills: {", ".join(student.skills)}
- Interests: {", ".join(student.interests)}
- Experience: {student.experience or "No prior experience"}
- Projects: {", ".join(student.projects or ["None listed"])}

Internship:
- Title: {internship.title}
- Company: {internship.company}
- Description: {internship.description}
- Requirements: {", ".join(internship.requirements)}
- Responsibilities: {", ".join(internship.responsibilities)}

Provide a 3-4 sentence match summary that:
1. Highlights the overall fit
2. Mentions key strengths
3. Notes any concerns
4. Gives an honest assessment
"""
        return self._call_llm(system_prompt, user_prompt)

    def identify_skill_gaps(
        self, student: StudentProfile, internship: InternshipDescription
    ) -> List[SkillGap]:
        """Identify skill gaps and provide learning recommendations"""
        system_prompt = """You are a technical skills advisor. Identify missing or weak skills 
and provide specific, actionable learning resources. Return your response as a JSON array."""

        user_prompt = f"""
Student Skills: {", ".join(student.skills)}
Required Skills: {", ".join(internship.requirements)}
Preferred Skills: {", ".join(internship.preferred_qualifications or [])}

Identify the top 3-5 skill gaps and for each provide:
1. The skill name
2. Importance level (High/Medium/Low)
3. 2-3 specific learning resources (courses, books, platforms)

Return ONLY a JSON array in this format:
[
  {{
    "skill": "Python",
    "importance": "High",
    "learning_resources": ["Coursera Python for Everybody", "Real Python tutorials", "LeetCode practice"]
  }}
]
"""
        response = self._call_llm(system_prompt, user_prompt)

        # Parse JSON response
        try:
            # Extract JSON from response (in case there's extra text)
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                gaps_data = json.loads(json_str)
                return [SkillGap(**gap) for gap in gaps_data]
            else:
                # Fallback if JSON parsing fails
                return []
        except:
            return []

    def generate_recommendations(
        self,
        student: StudentProfile,
        internship: InternshipDescription,
        skill_gaps: List[SkillGap],
    ) -> str:
        """Generate actionable recommendations"""
        system_prompt = """You are a career advisor providing actionable recommendations 
for internship applications. Be specific, encouraging, and practical."""

        gaps_text = "\n".join(
            [f"- {gap.skill} ({gap.importance} priority)" for gap in skill_gaps]
        )

        user_prompt = f"""
Student: {student.name}
Internship: {internship.title} at {internship.company}

Identified Skill Gaps:
{gaps_text}

Student Strengths:
- Skills: {", ".join(student.skills)}
- Projects: {", ".join(student.projects or ["None"])}

Provide 4-5 specific, actionable recommendations for this student to:
1. Improve their application
2. Address skill gaps
3. Highlight their strengths
4. Prepare for the interview

Keep it concise and practical.
"""
        return self._call_llm(system_prompt, user_prompt)

    def generate_tailored_resume(
        self, student: StudentProfile, internship: InternshipDescription
    ) -> str:
        """Generate ATS-optimized resume tailored to the job description"""
        system_prompt = """You are an expert resume writer specializing in ATS-optimized resumes.
Create a professional resume that highlights relevant skills and experiences for the specific role.
Use clear formatting with sections: Summary, Education, Skills, Experience, Projects."""

        user_prompt = f"""
Create an ATS-optimized resume for:

Student Information:
- Name: {student.name}
- Email: {student.email or "student@email.com"}
- Education: {student.education}
- Skills: {", ".join(student.skills)}
- Experience: {student.experience or "Seeking first internship opportunity"}
- Projects: {", ".join(student.projects or [])}
- Certifications: {", ".join(student.certifications or [])}

Target Internship:
- Title: {internship.title}
- Company: {internship.company}
- Key Requirements: {", ".join(internship.requirements[:5])}
- Responsibilities: {", ".join(internship.responsibilities[:3])}

Create a resume that:
1. Uses keywords from the job description
2. Highlights relevant skills prominently
3. Tailors the summary to this specific role
4. Emphasizes matching experiences and projects
5. Is ATS-friendly (clear sections, no tables/graphics)

Format as plain text with clear section headers.
"""
        return self._call_llm(system_prompt, user_prompt)

    def identify_strengths(
        self, student: StudentProfile, internship: InternshipDescription
    ) -> List[str]:
        """Identify student's key strengths for this role"""
        system_prompt = """Identify the top 3-5 strengths this student has for the internship.
Return ONLY a JSON array of strings."""

        user_prompt = f"""
Student Skills: {", ".join(student.skills)}
Student Projects: {", ".join(student.projects or [])}
Student Experience: {student.experience or "None"}

Internship Requirements: {", ".join(internship.requirements)}
Internship Responsibilities: {", ".join(internship.responsibilities)}

Return ONLY a JSON array of 3-5 key strengths, like:
["Strong Python programming skills", "Relevant project experience in web development"]
"""
        response = self._call_llm(system_prompt, user_prompt)

        try:
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end > start:
                return json.loads(response[start:end])
            else:
                return ["Relevant technical skills", "Strong educational background"]
        except:
            return ["Relevant technical skills", "Strong educational background"]

    def generate_complete_match(
        self, student: StudentProfile, internship: InternshipDescription
    ) -> MatchResult:
        """Generate complete matching result with all components"""

        # Calculate ATS score first (deterministic)
        ats_result = calculate_ats_score(student, internship)

        # Generate AI-powered analyses
        match_summary = self.analyze_match(student, internship)
        skill_gaps = self.identify_skill_gaps(student, internship)
        strengths = self.identify_strengths(student, internship)
        recommendations = self.generate_recommendations(student, internship, skill_gaps)
        tailored_resume = self.generate_tailored_resume(student, internship)

        return MatchResult(
            match_summary=match_summary,
            match_score=ats_result["overall_score"],
            skill_gaps=skill_gaps,
            strengths=strengths,
            recommendations=recommendations,
            tailored_resume=tailored_resume,
            ats_confidence_score=ats_result["overall_score"],
            keyword_analysis=ats_result,
        )
