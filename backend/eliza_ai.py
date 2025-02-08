import os
import json
import openai
from openai import OpenAI
from bnb_interaction import get_bnb_balance, send_dummy_transaction

# Set your OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv(OPENAI_API_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def parse_intent(message: str) -> dict:
    """
    Use OpenAI to parse the user message and determine the intended command.
    
    The prompt instructs the model to decide whether the user is asking to:
      - Query a balance ("balance")
      - Send a transaction ("send")
      - Engage in general conversation ("chat")
    
    The expected output is a JSON object that includes:
      - "command": one of "balance", "send", or "chat"
      - For "balance": an "address" field.
      - For "send": an "address" and "amount" field.
      - For "chat": a "message" field (the conversation prompt).
    """
    prompt = f"""
You are a command parser for a blockchain assistant. Interpret the user's message and determine if it is a blockchain command or just a general conversation.
The commands are as follows:
1. "balance": Query the BNB balance. Expect an "address" parameter.
2. "send": Send a transaction. Expect an "address" and an "amount" parameter.
3. "chat": General conversation.
    
Return a valid JSON with the following structure (without any additional text):
For a balance query:
    {{"command": "balance", "address": "<BNB_address>"}}
For a send transaction:
    {{"command": "send", "address": "<recipient_address>", "amount": "<amount>"}}
For general chat:
    {{"command": "chat", "message": "<the message>"}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
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
        # Fallback: if something goes wrong, assume it's a general chat
        intent = {"command": "chat", "message": message}
    return intent

def process_message(message: str) -> str:
    """
    Process the input message by first determining the intent using OpenAI's NLP,
    then executing the corresponding blockchain command or general chat response.
    """
    intent = parse_intent(message)
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
            tx_hash = send_dummy_transaction(to_address, amount)
            return f"Transaction sent! TX Hash: {tx_hash}"
        except Exception as e:
            return f"Error sending transaction: {e}"
    
    elif command == "chat":
        chat_message = intent.get("message", message)
        try:
            # For general conversation, delegate to OpenAI
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=chat_message,
                max_tokens=150,
                temperature=0.7,
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            return f"Error generating chat response: {e}"
    
    else:
        return "Sorry, I couldn't understand your command."
