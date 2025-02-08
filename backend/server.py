from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from eliza_ai import process_message
from bnb_interaction import get_bnb_balance, send_dummy_transaction

app = FastAPI(title="ElizaOS Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. For production, specify your trusted domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model for the chat request
class ChatRequest(BaseModel):
    message: str

# Data model for the chat response
class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint for processing chat messages.
    """
    try:
        reply = process_message(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/bnb/balance")
async def balance(address: str = Query(..., description="BNB address to check balance for")):
    """
    Endpoint to get the BNB balance for a given address.
    """
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
    """
    Endpoint to send a dummy transaction (for demonstration purposes).
    **Note:** Use with caution on mainnet. Prefer a testnet or simulation environment.
    """
    try:
        tx_hash = send_dummy_transaction(address, amount)
        return {"tx_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Running the app using uvicorn (for development)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
