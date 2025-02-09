import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# BNB RPC URL (default to Binance Smart Chain mainnet if not provided)
BNB_RPC_URL = os.getenv("BNB_RPC_URL", "https://bsc-dataseed.binance.org/")
TBNB_RPC_URL = os.getenv("TBNB_RPC_URL", "https://data-seed-prebsc-1-s1.binance.org:8545")
TBNB_WALLET= os.getenv("TBNB_WALLET", "0x058224eE1d755ea36dd8F974fd9525501f74f4B4")

# Private key for signing transactions.
# ⚠️ WARNING: NEVER expose your real private key in production.
# Use environment variables and secure storage.
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")

AVALANCHE_RPC_URL = os.getenv("AVALANCHE_RPC_URL","https://api.avax-test.network/ext/bc/C/rpc")
AVALANCHE_WALLET = os.getenv("AVALANCHE_WALLET", "0x058224eE1d755ea36dd8F974fd9525501f74f4B4")
AVALANCHE_PRIVATE_KEY = os.getenv("AVALANCHE_PRIVATE_KEY", "")