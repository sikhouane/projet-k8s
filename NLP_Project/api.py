from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from code_exec import answer

app = FastAPI(
    title="Weather NLP Agent",
    description="Question → LLM → JSON → Code execution → Réponse",
    version="1.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)
    debug: bool = Field(False, description="Retourne le JSON + résultat tool si true")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask(req: QuestionRequest):
    try:
        response = answer(req.question, debug=req.debug)
        return {
            "question": req.question,
            "answer": response,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
