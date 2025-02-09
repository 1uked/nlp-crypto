# eliza_ai.py

import os
import json
import datetime

# Make sure you have installed the OpenAI Python library:
#    pip install openai
import openai

from bnb_interaction import get_bnb_balance, send_transaction
from avax_interaction import get_avax_balance, send_avax_transaction
import scheduler  # Your module for scheduling payments

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_")  # Set your OpenAI key in the environment
openai.api_key = OPENAI_API_KEY

# Stores name–address mappings for easy lookup
saved_addresses = {}

def parse_intent(message: str, history: list) -> dict:
    """
    Uses an LLM to parse a user message into a JSON command object.

    The system prompt describes the possible commands:
      - "balance": Check a wallet address balance on BNB or Avalanche.
      - "send": Send a transaction on BNB or Avalanche.
      - "schedule_payment": Schedule a future transaction (time + address + amount).
      - "chain": Chain multiple commands in sequence.
      - "chat": Normal conversation.
      - "save": Save an address under a given name.

    The "chain" field may appear in the JSON to specify "bnb" or "avalanche".
    """
    current_time = datetime.datetime.utcnow().isoformat() + "Z"
    conversation_context = "\n".join(f"{m.role}: {m.text}" for m in history)

    system_prompt = f"""
You are a blockchain assistant with the following capabilities:
1. "balance": Return the balance of the provided address. Include a "chain" field ("bnb" or "avalanche").
2. "send": Send a transaction. Include "chain", "address", and "amount".
3. "schedule_payment": Provide "payment" (with "address" & "amount") plus "scheduled_time" (ISO or relative).
4. "chain": Return an array of commands to be processed in order.
5. "chat": For normal conversation, return "chat" and a message.
6. "save": Save a name–address pair (both required).

Use valid JSON only, with no extra text. Example for sending on Avalanche:
{{"command": "send", "chain": "avalanche", "address": "0x123", "amount": "0.5"}}

Current UTC time: {current_time}

Conversation history:
{conversation_context}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or any other model you're using
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0,
        )
        result = response.choices[0].message.content.strip()
        intent = json.loads(result)
    except Exception:
        # Fallback to simple chat if JSON parsing fails
        intent = {"command": "chat", "message": message}

    return intent


def process_chain(commands: list) -> str:
    """Process a list of commands (for 'command': 'chain')."""
    responses = []

    for cmd in commands:
        c = cmd.get("command")
        chain = cmd.get("chain", "bnb").lower()

        if c == "send":
            try:
                amount = float(cmd.get("amount", 0))
                address = cmd.get("address", "")
                if chain == "avalanche":
                    tx_hash = send_avax_transaction(address, amount)
                    responses.append(f"Sent {amount} AVAX to {address}. TX hash: {tx_hash}")
                else:
                    tx_hash = send_transaction(address, amount)
                    responses.append(f"Sent {amount} BNB to {address}. TX hash: {tx_hash}")
            except Exception as e:
                responses.append(f"Error sending payment: {e}")

        elif c == "balance":
            try:
                address = cmd.get("address", "")
                if chain == "avalanche":
                    balance = get_avax_balance(address)
                    responses.append(f"Balance of {address} on Avalanche: {balance}")
                else:
                    balance = get_bnb_balance(address)
                    responses.append(f"Balance of {address} on BNB: {balance}")
            except Exception as e:
                responses.append(f"Error retrieving balance: {e}")

        elif c == "schedule_payment":
            try:
                payment = cmd.get("payment", {})
                scheduled_time = cmd.get("scheduled_time")
                if payment and scheduled_time:
                    # Here you'd decide which chain to use inside scheduler, if needed
                    scheduler.schedule_payment(payment, scheduled_time, chain=chain)
                    responses.append(f"Scheduled payment of {payment.get('amount')} to {payment.get('address')} at {scheduled_time} on {chain}.")
                else:
                    responses.append("Invalid schedule command.")
            except Exception as e:
                responses.append(f"Error scheduling payment: {e}")

        elif c == "save":
            try:
                address = cmd.get("address")
                name = cmd.get("name")
                if address and name:
                    saved_addresses[name] = address
                    responses.append(f"Saved name '{name}' with address '{address}'.")
                else:
                    responses.append("Invalid save command: address or name missing.")
            except Exception as e:
                responses.append(f"Error saving address: {e}")

        elif c == "chat":
            responses.append(cmd.get("message", ""))

        else:
            responses.append("Unknown command in chain.")

    return "\n".join(responses)


def process_message(message: str, history: list) -> str:
    """Process a user message, parse its intent, execute the corresponding command, return a response."""
    intent = parse_intent(message, history)
    command = intent.get("command", "chat")
    chain = intent.get("chain", "bnb").lower()

    # 1. Check balance
    if command == "balance":
        address = intent.get("address")
        if not address:
            return "No valid address provided."
        try:
            if chain == "avalanche":
                balance = get_avax_balance(address)
                return f"Balance of {address} on Avalanche: {balance}"
            else:
                balance = get_bnb_balance(address)
                return f"Balance of {address} on BNB: {balance}"
        except Exception as e:
            return f"Error retrieving balance: {e}"

    # 2. Send transaction
    elif command == "send":
        address = intent.get("address")
        amount = intent.get("amount")
        if not address or not amount:
            return "Invalid send command. Provide 'address' and 'amount'."
        try:
            amount = float(amount)
            if chain == "avalanche":
                tx_hash = send_avax_transaction(address, amount)
                return f"Sent {amount} AVAX to {address}. Tx hash: {tx_hash}"
            else:
                tx_hash = send_transaction(address, amount)
                return f"Sent {amount} BNB to {address}. Tx hash: {tx_hash}"
        except Exception as e:
            return f"Error sending transaction: {e}"

    # 3. Schedule a payment
    elif command == "schedule_payment":
        payment = intent.get("payment", {})
        scheduled_time = intent.get("scheduled_time")
        if not (payment.get("address") and payment.get("amount") and scheduled_time):
            return "Missing payment details or scheduled time."
        try:
            # You might pass `chain` to your scheduler if you handle cross-chain scheduling.
            scheduler.schedule_payment(payment, scheduled_time, chain=chain)
            return f"Payment scheduled for {scheduled_time} on {chain} to {payment.get('address')}."
        except Exception as e:
            return f"Error scheduling payment: {e}"

    # 4. Chain multiple commands
    elif command == "chain":
        commands = intent.get("commands", [])
        return process_chain(commands)

    # 5. Save name–address
    elif command == "save":
        address = intent.get("address")
        name = intent.get("name")
        if not (address and name):
            return "Provide both 'address' and 'name' to save."
        saved_addresses[name] = address
        return f"Saved name '{name}' with address '{address}'."

    # 6. General chat fallback
    else:  # "chat"
        chat_message = intent.get("message", message)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": chat_message}],
                max_tokens=500,
                temperature=0.5,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating chat response: {e}"
