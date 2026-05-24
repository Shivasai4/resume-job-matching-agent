import numpy as np
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from app.config import settings
from app.embedding.embedder import Embedder
from app.observability.langfuse_setup import langfuse_handler   
import logging

logger = logging.getLogger(__name__)


class ResumeMatcher:
    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.llm = ChatOllama(model=settings.llm_model, temperature=0.1)

    def cosine_similarity(self, a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def match(self, job_description: str, resumes: list[str]) -> list[dict]:
        jd_embedding = self.embedder.embed(job_description)
        results = []
        for idx, resume_text in enumerate(resumes):
            resume_embedding = self.embedder.embed(resume_text)
            score = self.cosine_similarity(jd_embedding, resume_embedding)
            percent_score = round(score * 100, 1)   # 0-100 scale 
            results.append({
                "resume_index": idx,
                "score": percent_score,   # now 0-100
                "text": resume_text
            })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def generate_explanation(self, job_description: str, resume_text: str, score: float) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert recruiter. Explain why this candidate is a good match for the job. "
                       "Focus on skills, experience, and education alignment. Be concise, max 3 sentences."),
            ("human", "Job description:\n{job}\n\nCandidate resume:\n{resume}\n\nMatch score: {score:.2f}")
        ])
        chain = prompt | self.llm
        try:
            # ---- THIS is where the Langfuse callback is passed ----
            result = chain.invoke(
                {"job": job_description, "resume": resume_text, "score": score},
                config={"callbacks": [langfuse_handler] if langfuse_handler else []}
            )
            explanation = result.content
            logger.info("Explanation generated successfully")
            return explanation
        except Exception as e:
            logger.error(f"LLM explanation failed: {e}")
            return f"Match score: {score:.2f}. (Explanation unavailable due to error)"