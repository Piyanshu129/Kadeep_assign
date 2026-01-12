"""
FastAPI Backend for InternHub AI Platform
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import MatchRequest, MatchResult
from ai_engine import AIEngine
import os

app = FastAPI(
    title="InternHub AI Platform",
    description="AI-powered internship matching platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Engine
ai_engine = AIEngine()

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface"""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return """
    <html>
        <body>
            <h1>InternHub AI Platform</h1>
            <p>API is running. Visit <a href="/docs">/docs</a> for API documentation.</p>
        </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "InternHub AI Platform"}


@app.post("/match", response_model=MatchResult)
async def match_internship(request: MatchRequest):
    """
    Main matching endpoint
    Analyzes student profile against internship and returns comprehensive results
    """
    try:
        result = ai_engine.generate_complete_match(
            request.student_profile, request.internship
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")


@app.post("/batch-match")
async def batch_match(student_profile: dict, internships: list):
    """
    Batch matching endpoint
    Match one student against multiple internships
    """
    try:
        from models import StudentProfile, InternshipDescription

        student = StudentProfile(**student_profile)
        results = []

        for internship_data in internships:
            internship = InternshipDescription(**internship_data)
            result = ai_engine.generate_complete_match(student, internship)
            results.append(
                {
                    "internship_title": internship.title,
                    "company": internship.company,
                    "match_score": result.match_score,
                    "ats_score": result.ats_confidence_score,
                    "summary": result.match_summary,
                }
            )

        # Sort by match score
        results.sort(key=lambda x: x["match_score"], reverse=True)
        return {"matches": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch matching failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT

    print(f"🚀 Starting InternHub AI Platform on http://{API_HOST}:{API_PORT}")
    print(f"📚 API Documentation: http://{API_HOST}:{API_PORT}/docs")

    uvicorn.run(app, host=API_HOST, port=API_PORT)
