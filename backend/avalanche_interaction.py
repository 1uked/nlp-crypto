# avalanche_interaction.py
from web3 import Web3
from config import AVALANCHE_RPC_URL, AVALANCHE_WALLET, AVALANCHE_PRIVATE_KEY

def connect_to_avalanche():
    """Connect to the Avalanche network (e.g., Fuji Testnet)."""
    web3 = Web3(Web3.HTTPProvider(AVALANCHE_RPC_URL))
    if not web3.isConnected():
        raise ConnectionError("Failed to connect to the Avalanche network")
    return web3

def get_avalanche_balance(address: str) -> float:
    """Return the balance (in AVAX) for the given address."""
    web3 = connect_to_avalanche()
    balance_wei = web3.eth.get_balance(address)
    balance_avax = web3.fromWei(balance_wei, 'ether')
    return float(balance_avax)

def send_avalanche_transaction(recipient: str, amount: float) -> str:
    """
    Send a transaction on Avalanche.
    Change 'chainId' to 43114 for mainnet; here we use 43113 for the Fuji testnet.
    """
    web3 = connect_to_avalanche()
    sender_address = AVALANCHE_WALLET
    private_key = AVALANCHE_PRIVATE_KEY

    if not sender_address or not private_key:
        raise ValueError("Sender address or private key is not set.")

    nonce = web3.eth.get_transaction_count(sender_address)
    tx = {
        'nonce': nonce,
        'to': recipient,
        'value': web3.toWei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': web3.toWei('10', 'gwei'),
        'chainId': 43113  # Use 43114 for mainnet, 43113 for Fuji testnet.
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return web3.toHex(tx_hash)
