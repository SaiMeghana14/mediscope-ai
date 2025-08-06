from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.pipeline import process_text
from backend.feedback import save_feedback
from backend.auth import get_api_key
from backend.history_store import save_history

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(request: Request, api_key: str = Depends(get_api_key)):
    data = await request.json()
    user_input = data.get("text")
    language = data.get("language", "en")
    result = process_text(user_input, language)
    save_history(user_input, result)
    return result

@app.post("/feedback")
async def feedback(request: Request):
    data = await request.json()
    save_feedback(data)
    return {"message": "Feedback saved"}
