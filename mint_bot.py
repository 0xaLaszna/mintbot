from web3 import Web3
import json
import os
from dotenv import load_dotenv
# Load private key dari .env
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Konfigurasi jaringan Arbzukiswap
RPC_URL = "https://arbitrum.blockpi.network/v1/rpc/your-api-key"  # Ganti dengan RPC Arbitrum yang valid
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Pastikan koneksi berhasil
assert web3.is_connected(), "Gagal terhubung ke jaringan!"

# Alamat kontrak dan ABI
CONTRACT_ADDRESS = "0xYourNFTContractAddress"  # Ganti dengan alamat kontrak NFT Arbzukiswap
ABI = json.loads('[...]')  # Masukkan ABI kontrak di sini

# Load smart contract
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Load wallet
wallet_address = web3.eth.account.from_key(PRIVATE_KEY).address

# Fungsi untuk minting NFT
def mint_nft(amount):
    nonce = web3.eth.get_transaction_count(wallet_address)
    
    # Estimasi biaya gas
    gas_price = web3.eth.gas_price
    gas_limit = 300000  # Sesuaikan dengan kebutuhan
    
    # Persiapkan transaksi
    txn = contract.functions.mint(amount).build_transaction({
        "from": wallet_address,
        "value": web3.to_wei(0.01 * amount, "ether"),  # Ganti dengan harga mint per NFT
        "gas": gas_limit,
        "gasPrice": gas_price,
        "nonce": nonce,
    })
    
    # Tanda tangan transaksi
    signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    
    # Kirim transaksi
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Minting NFT... Tx Hash: {tx_hash.hex()}")

    # Tunggu konfirmasi
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status == 1:
        print(f"Sukses! NFT berhasil dimint. Tx: {tx_hash.hex()}")
    else:
        print("Minting gagal!")

# Jalankan bot untuk minting 1 NFT
mint_nft(1)
