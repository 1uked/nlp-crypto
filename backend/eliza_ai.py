# eliza_ai.py
import os
import json
from openai import OpenAI
from bnb_interaction import get_bnb_balance, send_transaction

# Set your OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_")
client = OpenAI(api_key=OPENAI_API_KEY)

def parse_intent(message: str, history: list) -> dict:
    # Use attribute access (m.role and m.text) since m is a Pydantic model instance.
    conversation_context = "\n".join([f"{m.role}: {m.text}" for m in history])
    prompt = f"""
You are a command parser for a blockchain assistant. The conversation history is:
{conversation_context}

Interpret the user's message and determine if it is a blockchain command or just general conversation.
The commands are as follows:
1. "balance": Query the BNB balance. Expect an "address" parameter.
2. "send": Send a transaction. Expect an "address" and an "amount" parameter.
3. "chat": General conversation.

Return a valid JSON with the following structure (with no additional text):
For a balance query:
    {{"command": "balance", "address": "<BNB_address>"}}
For a send transaction:
    {{"command": "send", "address": "<recipient_address>", "amount": "<amount>"}}
For general chat:
    {{"command": "chat", "message": "<the message>"}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=200,
            temperature=0,
        )
        result = response.choices[0].message.content.strip()
        intent = json.loads(result)
    except Exception as e:
        # Fallback: assume a general chat if something goes wrong
        intent = {"command": "chat", "message": message}
    return intent

def process_message(message: str, history: list) -> str:
    intent = parse_intent(message, history)
    command = intent.get("command", "chat")
    
    if command == "balance":
        address = intent.get("address")
        if not address:
            return "No valid address provided for balance inquiry."
        try:
            balance = get_bnb_balance(address)
            return f"The balance of {address} is {balance} BNB."
        except Exception as e:
            return f"Error retrieving balance: {e}"
    
    elif command == "send":
        to_address = intent.get("address")
        amount = intent.get("amount")
        if not to_address or not amount:
            return "Invalid send command parameters. Please provide both an address and an amount."
        try:
            amount = float(amount)
            tx_hash = send_transaction(to_address, amount)
            # Return the transaction hash so the frontend can show a clickable link.
            return f"Transaction sent! TX Hash: {tx_hash}"
        except Exception as e:
            return f"Error sending transaction: {e}"
    
    elif command == "chat":
        chat_message = intent.get("message", message)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": chat_message}
                ],
                max_tokens=500,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating chat response: {e}"
    
    else:
        return "Sorry, I couldn't understand your command."
