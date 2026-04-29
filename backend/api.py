from fastapi import FastAPI
from pydantic import BaseModel
from rag_app import chat_with_video, summarize_video
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (IMPORTANT for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    video_url: str
    question: str

class SummaryRequest(BaseModel):
    video_url: str


@app.get("/")
def home():
    return {"status": "API running"}


@app.post("/chat")
def chat(req: ChatRequest):
    return {"answer": chat_with_video(req.video_url, req.question)}


@app.post("/summary")
def summary(req: SummaryRequest):
    return {"summary": summarize_video(req.video_url)}
