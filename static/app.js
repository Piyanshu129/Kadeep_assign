// InternHub AI - Frontend JavaScript

const API_BASE_URL = window.location.origin;

// DOM Elements
const matchForm = document.getElementById('matchForm');
const matchBtn = document.getElementById('matchBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const downloadResumeBtn = document.getElementById('downloadResumeBtn');

// Event Listeners
matchBtn.addEventListener('click', handleMatch);
downloadResumeBtn.addEventListener('click', downloadResume);

let currentResume = '';
let currentStudentName = '';
let currentCompany = '';

async function handleMatch() {
    // Collect form data
    const studentProfile = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim() || null,
        education: document.getElementById('education').value.trim(),
        skills: document.getElementById('skills').value.split(',').map(s => s.trim()).filter(s => s),
        interests: document.getElementById('interests').value.split(',').map(s => s.trim()).filter(s => s),
        experience: document.getElementById('experience').value.trim() || null,
        projects: document.getElementById('projects').value ?
            document.getElementById('projects').value.split(',').map(s => s.trim()).filter(s => s) : null
    };

    const internship = {
        title: document.getElementById('jobTitle').value.trim(),
        company: document.getElementById('company').value.trim(),
        description: document.getElementById('description').value.trim(),
        requirements: document.getElementById('requirements').value.split(',').map(s => s.trim()).filter(s => s),
        responsibilities: document.getElementById('responsibilities').value.split(',').map(s => s.trim()).filter(s => s),
        location: document.getElementById('location').value.trim() || null
    };

    // Validate
    if (!studentProfile.name || !studentProfile.education || studentProfile.skills.length === 0) {
        alert('Please fill in all required student profile fields');
        return;
    }

    if (!internship.title || !internship.company || !internship.description ||
        internship.requirements.length === 0 || internship.responsibilities.length === 0) {
        alert('Please fill in all required internship fields');
        return;
    }

    // Store for resume download
    currentStudentName = studentProfile.name;
    currentCompany = internship.company;

    // Show loading
    resultsSection.classList.add('hidden');
    loadingSection.classList.remove('hidden');
    matchBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/match`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_profile: studentProfile,
                internship: internship
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Matching failed');
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}\n\nMake sure the vLLM server is running on http://localhost:2525`);
    } finally {
        loadingSection.classList.add('hidden');
        matchBtn.disabled = false;
    }
}

function displayResults(result) {
    // Scores
    document.getElementById('matchScore').textContent = `${result.match_score.toFixed(1)}%`;
    document.getElementById('atsScore').textContent = `${result.ats_confidence_score.toFixed(1)}%`;

    // Match Summary
    document.getElementById('matchSummary').textContent = result.match_summary;

    // Strengths
    const strengthsList = document.getElementById('strengthsList');
    strengthsList.innerHTML = '';
    result.strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });

    // Skill Gaps
    const skillGapsList = document.getElementById('skillGapsList');
    skillGapsList.innerHTML = '';
    result.skill_gaps.forEach(gap => {
        const gapItem = document.createElement('div');
        gapItem.className = 'skill-gap-item';

        const priorityClass = `priority-${gap.importance.toLowerCase()}`;

        gapItem.innerHTML = `
            <div class="skill-gap-header">
                <span class="skill-name">${gap.skill}</span>
                <span class="skill-priority ${priorityClass}">${gap.importance}</span>
            </div>
            <div class="learning-resources">
                <strong>Learning Resources:</strong>
                <ul>
                    ${gap.learning_resources.map(resource => `<li>${resource}</li>`).join('')}
                </ul>
            </div>
        `;

        skillGapsList.appendChild(gapItem);
    });

    // Recommendations
    document.getElementById('recommendations').textContent = result.recommendations;

    // Resume
    currentResume = result.tailored_resume;
    document.getElementById('resumeContent').textContent = currentResume;

    // ATS Breakdown
    if (result.keyword_analysis && result.keyword_analysis.breakdown) {
        const breakdown = result.keyword_analysis.breakdown;
        const atsBreakdown = document.getElementById('atsBreakdown');
        atsBreakdown.innerHTML = '';

        const metrics = [
            { label: 'Skill Match', value: breakdown.skill_match },
            { label: 'Experience Match', value: breakdown.experience_match },
            { label: 'Education Match', value: breakdown.education_match },
            { label: 'Keyword Density', value: breakdown.keyword_density }
        ];

        metrics.forEach(metric => {
            const metricDiv = document.createElement('div');
            metricDiv.className = 'ats-metric';
            metricDiv.innerHTML = `
                <span class="metric-label">${metric.label}</span>
                <div class="metric-bar-container">
                    <div class="metric-bar" style="width: ${metric.value}%"></div>
                </div>
                <span class="metric-value">${metric.value.toFixed(1)}%</span>
            `;
            atsBreakdown.appendChild(metricDiv);
        });
    }

    // Show results
    resultsSection.classList.remove('hidden');

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function downloadResume() {
    if (!currentResume) {
        alert('No resume to download');
        return;
    }

    const filename = `resume_${currentStudentName.replace(/\s+/g, '_')}_${currentCompany.replace(/\s+/g, '_')}.txt`;

    const blob = new Blob([currentResume], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Add smooth animations on page load
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});
