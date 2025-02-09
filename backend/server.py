# server.py
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from eliza_ai import process_message
from bnb_interaction import get_bnb_balance, send_transaction

app = FastAPI(title="ElizaOS Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your trusted domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for an individual message
class Message(BaseModel):
    role: str
    text: str

# ChatRequest now carries both the new message and the conversation history.
class ChatRequest(BaseModel):
    message: str
    history: List[Message] = []

# ChatResponse returns the processed reply.
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        reply = process_message(request.message, request.history)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bnb/balance")
async def balance(address: str = Query(..., description="BNB address to check balance for")):
    try:
        balance = get_bnb_balance(address)
        return {"address": address, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bnb/transaction")
async def transaction(
    address: str = Query(..., description="Recipient address"),
    amount: float = Query(..., description="Amount in BNB")
):
    try:
        tx_hash = send_transaction(address, amount)
        return {"tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
