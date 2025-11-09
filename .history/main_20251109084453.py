from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Allow CORS so React frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Response model
class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat: ChatRequest):
    """
    Placeholder AI response. Later replace this with your AI model inference.
    """
    user_msg = chat.message.strip()

    # Simple placeholder logic: echo + basic suggestions
    ai_reply = f"Analyzing your request for '{user_msg}'... This is a placeholder response."
    
    return ChatResponse(reply=ai_reply)

# Root endpoint to test server
@app.get("/")
async def root():
    return {"status": "TW-KON AI backend running"}
