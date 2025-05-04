from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
from rag_python import get_sdu_bot_response

app = FastAPI(
    title="Qysqa Bot API from Samsa Team",
    description="API для чат-бота с знаниями о курсах",
    version="1.0.0"
)

class Question(BaseModel):
    text: str

class Response(BaseModel):
    answer: str
    cost: float

@app.post("/ask", response_model=Response)
async def ask_question(question: Question):
    try:
        answer, cost = get_sdu_bot_response(question.text)
        return Response(answer=answer, cost=cost)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в Qysqa Bot API. Используйте /ask для отправки вопросов."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082) 