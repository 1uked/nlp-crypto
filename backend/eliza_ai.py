# eliza_ai.py
import os
import json
import datetime
from openai import OpenAI
from bnb_interaction import get_bnb_balance, send_transaction
from avalanche_interaction import get_avalanche_balance, send_avalanche_transaction
import scheduler  # For scheduling payments

# Set your OpenAI API key (make sure it’s set in your environment)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_")
client = OpenAI(api_key=OPENAI_API_KEY)

def parse_intent(message: str, history: list) -> dict:
    """
    Use OpenAI to parse the user message into a precise command.
    
    The system prompt explains that you are a blockchain assistant who can:
      1. Check wallet balances (command: "balance") with an optional "chain" field.
      2. Send transactions immediately (command: "send") with an optional "chain" field.
      3. Schedule a payment (command: "schedule_payment")—provide a payment object (with "address" and "amount")
         and a "scheduled_time" in ISO format or relative format. If the user specifies a relative time (like 'in 1 minute'),
         convert it to an absolute ISO datetime using the current time.
      4. Chain multiple commands (command: "chain")—return an array of commands.
      5. Chat normally (command: "chat")
      
    Output only valid JSON with no extra commentary.
    """
    # Get the current UTC time in ISO format with a trailing 'Z'
    current_time = datetime.datetime.utcnow().isoformat() + "Z"
    conversation_context = "\n".join([f"{m.role}: {m.text}" for m in history])
    
    system_prompt = f"""
You are a blockchain assistant with the following capabilities:
1. Check the balance of a wallet. Respond with command "balance" and provide the wallet address.
2. Send a transaction immediately. Respond with command "send" and provide the recipient address and amount.
3. Schedule a payment. Respond with command "schedule_payment", providing a payment object (with "address" and "amount") and a "scheduled_time" in ISO format or as a relative string (starting with 'in '). If the user specifies a relative time (e.g., 'in 1 minute'), convert it to an absolute ISO datetime using the current time.
4. Chain multiple commands. Respond with command "chain" and include an array of commands.
5. For general conversation, respond with command "chat" and a message.

For cross-chain operations, include an optional "chain" field in your JSON output. Use "bnb" for Binance Smart Chain and "avalanche" for Avalanche. For example:
For sending a transaction on Avalanche:
    {{"command": "send", "chain": "avalanche", "address": "<recipient_address>", "amount": "<amount>"}}
For checking balance on Avalanche:
    {{"command": "balance", "chain": "avalanche", "address": "<address>"}}

Current UTC time is: {current_time}

Conversation history:
{conversation_context}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0,
        )
        result = response.choices[0].message.content.strip()
        intent = json.loads(result)
    except Exception as e:
        intent = {"command": "chat", "message": message}
    return intent

def process_chain(commands: list) -> str:
    """Process a chain of commands sequentially."""
    responses = []
    for cmd in commands:
        c = cmd.get("command")
        chain = cmd.get("chain", "bnb")  # Default to BNB if not provided.
        if c == "send":
            try:
                amount = float(cmd.get("amount"))
                if chain.lower() == "avalanche":
                    tx_hash = send_avalanche_transaction(cmd.get("address"), amount)
                else:
                    tx_hash = send_transaction(cmd.get("address"), amount)
                responses.append(f"Sent {amount} BNB/AVAX to {cmd.get('address')}. TX Hash: {tx_hash}")
            except Exception as e:
                responses.append(f"Error sending payment: {e}")
        elif c == "balance":
            try:
                if chain.lower() == "avalanche":
                    balance = get_avalanche_balance(cmd.get("address"))
                else:
                    balance = get_bnb_balance(cmd.get("address"))
                responses.append(f"Balance of {cmd.get('address')} on {chain} is {balance}.")
            except Exception as e:
                responses.append(f"Error retrieving balance: {e}")
        # Add additional command handling as needed.
    return "\n".join(responses)

def process_message(message: str, history: list) -> str:
    """Process the input message by parsing its intent and executing the corresponding command."""
    intent = parse_intent(message, history)
    command = intent.get("command", "chat")
    chain = intent.get("chain", "bnb")  # Default chain is BNB.
    
    if command == "balance":
        address = intent.get("address")
        if not address:
            return "No valid address provided for balance inquiry."
        try:
            if chain.lower() == "avalanche":
                balance = get_avalanche_balance(address)
            else:
                balance = get_bnb_balance(address)
            return f"The balance of {address} on {chain.upper()} is {balance}."
        except Exception as e:
            return f"Error retrieving balance: {e}"
    
    elif command == "send":
        to_address = intent.get("address")
        amount = intent.get("amount")
        if not to_address or not amount:
            return "Invalid send command parameters. Please provide both an address and an amount."
        try:
            amount = float(amount)
            if chain.lower() == "avalanche":
                tx_hash = send_avalanche_transaction(to_address, amount)
            else:
                tx_hash = send_transaction(to_address, amount)
            return f"Transaction sent on {chain.upper()}! TX Hash: {tx_hash}"
        except Exception as e:
            return f"Error sending transaction: {e}"
    
    elif command == "schedule_payment":
        payment = intent.get("payment", {})
        scheduled_time = intent.get("scheduled_time")
        if not payment.get("address") or not payment.get("amount") or not scheduled_time:
            return "Invalid scheduling command. Please provide payment details and a scheduled time."
        try:
            # Schedule the payment using our scheduler module.
            scheduler.schedule_payment(payment, scheduled_time)
            return f"Payment scheduled for {scheduled_time} to {payment.get('address')} on {chain.upper()}."
        except Exception as e:
            return f"Error scheduling payment: {e}"
    
    elif command == "chain":
        commands = intent.get("commands", [])
        return process_chain(commands)
    
    elif command == "chat":
        chat_message = intent.get("message", message)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": chat_message}],
                max_tokens=500,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating chat response: {e}"
    
    else:
        return "Sorry, I couldn't understand your command."
