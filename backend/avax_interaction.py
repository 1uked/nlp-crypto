#!/usr/bin/env python3

from web3 import Web3
from config import AVALANCHE_RPC_URL,AVALANCHE_WALLET,AVALANCHE_PRIVATE_KEY

# Configuration
CHAIN_ID = 43113  # 43114 for Avalanche Mainnet

def connect_to_avax() -> Web3:
    web3 = Web3(Web3.HTTPProvider(AVALANCHE_RPC_URL))
    if not web3.is_connected():
        raise ConnectionError(f"Failed to connect to Avalanche at {AVALANCHE_RPC_URL}")
    return web3

def get_avax_balance(address: str) -> float:
    web3 = connect_to_avax()
    balance_wei = web3.eth.get_balance(address)
    return float(web3.from_wei(balance_wei, 'ether'))

def send_avax_transaction(recipient: str, amount: float) -> str:
    web3 = connect_to_avax()
    nonce = web3.eth.get_transaction_count(AVALANCHE_WALLET)
    tx = {
        'nonce': nonce,
        'to': recipient,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('25', 'gwei'),
        'chainId': CHAIN_ID
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=AVALANCHE_PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return web3.to_hex(tx_hash)

if __name__ == "__main__":
    balance = get_avax_balance(AVALANCHE_WALLET)
    print(f"Balance for {AVALANCHE_WALLET}: {balance} AVAX")

    # Example transaction (uncomment to send):
    # tx_hash = send_avax_transaction("0xRecipientAddress", 0.01)
    # print(f"Transaction sent: {tx_hash}")
