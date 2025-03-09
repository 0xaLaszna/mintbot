from web3 import Web3
import json
import os
from dotenv import load_dotenv
# Load private key dari .env
load_dotenv()

# Ambil semua private key dari .env
PRIVATE_KEYS = os.getenv("PRIVATE_KEYS")
if not PRIVATE_KEYS:
    raise ValueError("PRIVATE_KEYS tidak ditemukan di .env!")

PRIVATE_KEYS = PRIVATE_KEYS.split(",")  # Jika ingin multi-wallet

from web3 import Web3

# Ganti dengan RPC URL dari jaringan Arbitrum
RPC_URL = "https://arbitrum-one.publicnode.com"  

# Hubungkan ke jaringan Arbitrum
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Periksa koneksi
assert web3.isConnected(), "Gagal terhubung ke jaringan!"
print("Berhasil terhubung ke jaringan Arbitrum!")

# Proses setiap private key
for private_key in PRIVATE_KEYS:
    account = web3.eth.account.from_key(private_key.strip())
    wallet_address = account.address
    print(f"🔑 Menggunakan wallet: {wallet_address}")

    # Masukkan logika minting di sini...

# Alamat kontrak dan ABI
CONTRACT_ADDRESS = "0x071126cBec1C5562530Ab85fD80dd3e3a42A70B8"  # Ganti dengan alamat kontrak NFT Arbzukiswap
with open("contract_abi.json", "r") as file:
    ABI = json.load(file)

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
