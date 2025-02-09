# ElizaOS Backend

## Overview
The backend of ElizaOS is responsible for handling user interactions, processing natural language inputs, and interacting with the BNB blockchain. It is built using **FastAPI** and integrates with OpenAI's API for intelligent command parsing and chatbot responses.

## Features
- **Natural Language Processing**: Uses OpenAI's API to interpret user commands and determine intent.
- **BNB Blockchain Interaction**: Retrieves balances and sends transactions via Web3.py.
- **FastAPI-based API**: Handles requests for chat and blockchain operations.

## Installation
### Prerequisites
- Python 3.8+
- `pip` package manager
- OpenAI API Key
- BNB RPC URL & Private Key

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ElizaOS.git
   cd ElizaOS/backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file:
   ```ini
   BNB_RPC_URL="https://bsc-dataseed.binance.org/"
   PRIVATE_KEY="your_private_key_here"
   OPENAI_API_KEY="your_openai_api_key_here"
   ```

## Running the Backend
Start the FastAPI server:
```bash
uvicorn server:app --reload
```

The server will be available at: [http://localhost:8000](http://localhost:8000)

## API Endpoints
### 1. Chat Endpoint
**POST** `/chat`
- **Request Body:**
  ```json
  {"message": "Check my balance for 0xAddress"}
  ```
- **Response:**
  ```json
  {"reply": "The balance of 0xAddress is 2.5 BNB."}
  ```

### 2. Get BNB Balance
**GET** `/bnb/balance?address=<BNB_ADDRESS>`
- **Response:**
  ```json
  {"address": "0xYourAddress", "balance": 2.5}
  ```

### 3. Send Transaction
**POST** `/bnb/transaction?address=<TO_ADDRESS>&amount=<AMOUNT>`
- **Response:**
  ```json
  {"tx_hash": "0x1234abcd..."}
  ```

## Testing
Use `curl` or Postman to send requests, or test with:
```bash
pytest tests/
```

## Curl conmands

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the balance of you mother"}'
```

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What is the balance of 0xYourBNBAddressHere?"}'
```

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Please send 0.01 BNB to 0xRecipientAddress"}'
```



