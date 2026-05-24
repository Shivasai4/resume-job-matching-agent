from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from app.models.schemas import MatchSingleResponse
from app.matcher.matcher import ResumeMatcher
from app.embedding.embedder import Embedder
from app.parser.resume_parser import parse_resume
from app.utils.logging_config import setup_logging
from app.observability.langfuse_setup import init_langfuse
import logging
import tempfile
from pathlib import Path

setup_logging()
logger = logging.getLogger(__name__)
init_langfuse()

app = FastAPI(title="Resume Matcher")
embedder = Embedder()
matcher = ResumeMatcher(embedder)

@app.post("/match-single", response_model=MatchSingleResponse)
async def match_single_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    logger.info("Received single resume match request")
    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as tmp:
        content = await resume_file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        # Parse resume text from file
        resume_text = parse_resume(tmp_path)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Empty resume")
        # Compute match (single resume in a list)
        results = matcher.match(job_description, [resume_text])
        if not results:
            raise HTTPException(status_code=500, detail="Scoring failed")
        top = results[0]
        explanation = matcher.generate_explanation(job_description, resume_text, top["score"])
        return MatchSingleResponse(
            score=top["score"],
            explanation=explanation,
            resume_text=resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        )
    except Exception as e:
        logger.error(f"Match failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if tmp_path.exists():
            tmp_path.unlink()