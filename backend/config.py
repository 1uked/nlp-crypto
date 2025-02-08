import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# BNB RPC URL (default to Binance Smart Chain mainnet if not provided)
BNB_RPC_URL = os.getenv("BNB_RPC_URL", "https://bsc-dataseed.binance.org/")

# Private key for signing transactions.
# ⚠️ WARNING: NEVER expose your real private key in production.
# Use environment variables and secure storage.
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
