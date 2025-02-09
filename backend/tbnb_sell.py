import os
from web3 import Web3
from config import TBNB_RPC_URL, TBNB_WALLET, PRIVATE_KEY

def connect_to_bsc():
    """Connects to the Binance Smart Chain Testnet and returns a Web3 instance."""
    web3 = Web3(Web3.HTTPProvider(TBNB_RPC_URL))

    if not web3.is_connected():
        raise ConnectionError("Failed to connect to BSC Testnet")

    return web3

def send_bnb(receiver_address: str, amount_in_bnb: float):
    """Sends the specified amount of tBNB to the recipient address."""
    web3 = connect_to_bsc()
    sender_address = TBNB_WALLET
    private_key = PRIVATE_KEY  # Store your private key securely

    if not sender_address or not private_key:
        raise ValueError("Sender address or private key is not set.")

    nonce = web3.eth.get_transaction_count(sender_address)

    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': web3.to_wei(amount_in_bnb, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('10', 'gwei'),
        'chainId': 97  # BSC Testnet Chain ID
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    print(f"Transaction sent! Tx hash: {web3.to_hex(tx_hash)}")

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")

    return tx_hash

if __name__ == "__main__":
    # Example usage
    recipient = "0xd3EC55046Cc8BB7c292dCFF521FD4f6610F48Ecb"
    amount = 0.045  # Example amount
    send_bnb(recipient, amount)
