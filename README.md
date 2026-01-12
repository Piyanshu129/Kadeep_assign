# InternHub AI Platform

> **AI-powered internship matching platform with skill gap analysis, resume generation, and ATS scoring**

InternHub AI is a comprehensive platform that uses artificial intelligence to match student profiles with internship opportunities. It provides detailed analysis, identifies skill gaps, generates tailored resumes, and calculates ATS (Applicant Tracking System) confidence scores.

## ✨ Features

- **🎯 Smart Matching**: AI-powered analysis of student profiles against internship descriptions
- **📊 Match Scoring**: Comprehensive scoring system (0-100) based on skills, experience, and education
- **📚 Skill Gap Analysis**: Identifies missing skills with prioritization and learning resources
- **💪 Strength Identification**: Highlights student's key strengths for each role
- **💡 Actionable Recommendations**: Personalized advice for improving applications
- **📄 Resume Generation**: Creates ATS-optimized resumes tailored to job descriptions
- **🎯 ATS Confidence Score**: Calculates likelihood of passing automated screening systems
- **🔍 Keyword Analysis**: Detailed breakdown of keyword matching and relevance

## 🏗️ Architecture

### Technology Stack

- **Backend**: FastAPI (Python)
- **AI Engine**: Local llama.cpp (Qwen2.5-7B-Instruct-AWQ)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Styling**: Modern CSS with glassmorphism and gradients

### Components

1. **AI Engine** (`ai_engine.py`): Core LLM integration with carefully designed prompts
2. **ATS Scorer** (`ats_scorer.py`): Deterministic scoring algorithm for keyword matching
3. **API Server** (`api.py`): FastAPI backend with REST endpoints
4. **CLI Interface** (`cli.py`): Command-line tool for quick testing
5. **Web Interface** (`static/`): Modern, responsive web UI

## 🚀 Setup

### Prerequisites

- Python 3.8+
- llama.cpp server running on `http://localhost:2525` (see `Piyanshu/llama-server`)

### Installation

```bash
# Navigate to project directory
cd Piyanshu/kdep

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The application uses environment variables for configuration (see `config.py`):

```bash
# llama.cpp API settings
export LLAMA_CPP_BASE_URL="http://localhost:2525/v1"
export LLAMA_CPP_API_KEY="token-abc123"
export LLAMA_CPP_MODEL="Qwen/Qwen2.5-7B-Instruct-AWQ"

# API server settings
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

## 📖 Usage

### 1. Web Interface (Recommended)

Start the API server:

```bash
python api.py
```

Open your browser to `http://localhost:8000`

The web interface provides:
- Interactive forms for student profiles and internship descriptions
- Real-time AI analysis with loading indicators
- Beautiful visualization of results
- Downloadable tailored resumes

### 2. CLI Interface

**Interactive Mode:**
```bash
python cli.py match --interactive
```

**File-based Mode:**
```bash
python cli.py match --profile examples/sample_profile.json --internship examples/sample_internship.json
```

The CLI provides:
- Rich formatted output with colors and tables
- Progress indicators during AI processing
- Option to save generated resumes

### 3. API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Single Match:**
```bash
curl -X POST http://localhost:8000/match \
  -H "Content-Type: application/json" \
  -d '{
    "student_profile": {
      "name": "Alice Johnson",
      "education": "BS Computer Science",
      "skills": ["Python", "JavaScript"],
      "interests": ["Web Development"]
    },
    "internship": {
      "title": "Software Engineering Intern",
      "company": "TechCorp",
      "description": "...",
      "requirements": ["Python", "JavaScript"],
      "responsibilities": ["Develop features"]
    }
  }'
```

**Batch Match:**
```bash
curl -X POST http://localhost:8000/batch-match \
  -H "Content-Type: application/json" \
  -d '{
    "student_profile": {...},
    "internships": [{...}, {...}]
  }'
```

## 🧠 How It Works

### 1. AI-Powered Analysis

The system uses carefully designed prompts to leverage the llama.cpp server for:

- **Match Analysis**: Compares student profile with internship requirements
- **Skill Gap Identification**: Identifies missing skills and suggests learning paths
- **Recommendation Generation**: Provides actionable advice
- **Resume Tailoring**: Creates ATS-optimized resumes based on job descriptions

### 2. ATS Scoring Algorithm

The deterministic scoring system evaluates:

- **Skill Match (40%)**: Percentage of required skills the student possesses
- **Experience Match (25%)**: Relevance of previous experience to the role
- **Education Match (15%)**: Alignment of educational background
- **Keyword Density (20%)**: Overall keyword matching across all fields

### 3. Prompt Design

Each AI task uses specialized prompts:

```python
# Example: Match Analysis Prompt
system_prompt = """You are an expert career counselor and internship matching specialist. 
Analyze the student profile against the internship description and provide a comprehensive 
match assessment. Be honest, constructive, and specific in your analysis."""
```

The prompts are designed to:
- Provide clear context and role definition
- Request specific, structured outputs
- Encourage honest and constructive feedback
- Generate actionable insights

## 📊 Example Output

```
Match Score: 85.3%
ATS Score: 82.7%

Match Summary:
Alice is a strong candidate for this Software Engineering Intern position. Her skills 
in Python, JavaScript, and React align well with the requirements. Her previous 
internship experience and relevant projects demonstrate practical application of these 
skills. The main area for improvement is gaining experience with Docker and CI/CD.

Strengths:
✓ Strong Python and JavaScript programming skills
✓ Relevant project experience in web development
✓ Previous internship experience
✓ AWS certification shows cloud knowledge

Skill Gaps:
- Docker (High Priority)
  • Docker Documentation and Tutorials
  • Docker for Beginners course on Udemy
  
- CI/CD Pipelines (Medium Priority)
  • GitHub Actions documentation
  • Jenkins tutorial series
```

## 🎨 Design Philosophy

The web interface follows modern design principles:

- **Glassmorphism**: Translucent cards with backdrop blur
- **Vibrant Gradients**: Eye-catching color schemes
- **Smooth Animations**: Micro-interactions for better UX
- **Responsive Design**: Works on all screen sizes
- **Accessibility**: Semantic HTML and proper ARIA labels

## 🔧 Core Concepts

### 1. Separation of Concerns

- **AI Engine**: Handles all LLM interactions
- **ATS Scorer**: Provides deterministic scoring
- **API Layer**: Exposes functionality via REST
- **Interfaces**: Multiple ways to interact (Web, CLI, API)

### 2. Prompt Engineering

Prompts are designed with:
- Clear role definitions
- Specific output formats (JSON for structured data)
- Context-rich inputs
- Fallback handling for parsing errors

### 3. User Experience

- **Progressive Disclosure**: Show results incrementally
- **Visual Feedback**: Loading states and animations
- **Error Handling**: Graceful degradation and helpful messages
- **Multiple Interfaces**: Choose based on use case

## 📁 Project Structure

```
kdep/
├── api.py                  # FastAPI server
├── ai_engine.py           # AI/LLM integration
├── ats_scorer.py          # ATS scoring algorithm
├── cli.py                 # CLI interface
├── config.py              # Configuration
├── models.py              # Pydantic data models
├── requirements.txt       # Python dependencies
├── static/
│   ├── index.html        # Web interface
│   ├── style.css         # Styling
│   └── app.js            # Frontend logic
└── examples/
    ├── sample_profile.json
    └── sample_internship.json
```

## 🧪 Testing

Test with sample data:

```bash
# CLI test
python cli.py match -p examples/sample_profile.json -i examples/sample_internship.json

# API test
python api.py  # Start server in one terminal
curl -X POST http://localhost:8000/match ...  # Test in another
```

## 🚦 Troubleshooting

**Issue**: "LLM API call failed"
- **Solution**: Ensure llama.cpp server is running on `http://localhost:2525`
- Check: `curl http://localhost:2525/v1/models`

**Issue**: "Module not found"
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**Issue**: Web interface not loading
- **Solution**: Make sure API server is running: `python api.py`

## 📝 License

This project is part of the InternHub platform internship assignment.

## 🤝 Contributing

This is an assignment project. For questions or improvements, contact the development team.

---

**Built with ❤️ using llama.cpp, FastAPI, and modern web technologies**
