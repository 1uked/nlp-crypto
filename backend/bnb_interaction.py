from web3 import Web3
from config import BNB_RPC_URL, PRIVATE_KEY

# Initialize the Web3 connection using the provided RPC URL
web3 = Web3(Web3.HTTPProvider(BNB_RPC_URL))

if not web3.is_connected():
    raise ConnectionError("Unable to connect to the BNB RPC endpoint.")

# Create an account object from the private key (for signing transactions)
account = web3.eth.account.from_key(PRIVATE_KEY)


def get_bnb_balance(address: str) -> float:
    """
    Returns the balance (in BNB) for the specified address.
    """
    try:
        balance_wei = web3.eth.get_balance(address)
        balance_bnb = web3.from_wei(balance_wei, 'ether')
        return float(balance_bnb)
    except Exception as e:
        print(f"Error retrieving balance for {address}: {e}")
        raise


def send_dummy_transaction(to_address: str, amount: float) -> str:
    """
    Creates and sends a simple transaction transferring the specified amount of BNB.
    This function is for demonstration purposes only.
    """
    try:
        nonce = web3.eth.get_transaction_count(account.address)
        txn = {
            'nonce': nonce,
            'to': to_address,
            'value': web3.to_wei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': web3.to_wei('5', 'gwei')
        }
        # Sign the transaction with the private key
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return web3.toHex(tx_hash)
    except Exception as e:
        print(f"Error sending transaction to {to_address}: {e}")
        raise
