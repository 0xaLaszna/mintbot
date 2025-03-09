from dotenv import load_dotenv
import os
import json
from web3 import Web3

# Load .env file
load_dotenv(override=True)

# Ambil semua private key dari .env
PRIVATE_KEYS = os.getenv("PRIVATE_KEYS")
if not PRIVATE_KEYS:
    raise ValueError("PRIVATE_KEYS tidak ditemukan di .env!")

PRIVATE_KEYS = PRIVATE_KEYS.split(",")  # Pisahkan jika ada banyak

print(f"Saldo Wallet: {web3.from_wei(web3.eth.get_balance(wallet_address), 'ether')} ETH")
print(f"Gas Price: {web3.from_wei(web3.eth.gas_price, 'gwei')} GWEI")

# Hubungkan ke node Arbitrum
RPC_URL = os.getenv("RPC_URL")
if not RPC_URL:
    raise ValueError("RPC_URL tidak ditemukan di .env!")

web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.isConnected():
    raise Exception("Gagal terhubung ke jaringan Arbitrum!")

# Load ABI dari file JSON
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
if not CONTRACT_ADDRESS:
    raise ValueError("CONTRACT_ADDRESS tidak ditemukan di .env!")

with open("contract_abi.json", "r") as f:
    contract_abi = json.load(f)

# Inisialisasi kontrak
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

# Proses setiap private key
for private_key in PRIVATE_KEYS:
    private_key = private_key.strip().replace("0x", "")  # Hapus "0x" jika ada
    if len(private_key) != 64:  # Private key harus 64 karakter
        print(f"❌ Private key tidak valid: {private_key}")
        continue

    try:
        account = web3.eth.account.from_key(private_key)  # Inisialisasi akun
        wallet_address = account.address  # Ambil alamat wallet
        print(f"🔑 Menggunakan wallet: {wallet_address}")

    except Exception as e:
        print(f"❌ Gagal memproses private key: {private_key} - {str(e)}")
        
        # Ambil nonce terbaru
        nonce = web3.eth.get_transaction_count(wallet_address)

        # Panggil fungsi minting
   mint_txn = contract.functions.mint(1).build_transaction({
    'from': wallet_address,
    'value': web3.to_wei(0.01, 'ether'),
    'gas': 300000,
    'maxPriorityFeePerGas': web3.to_wei('2', 'gwei'),
    'maxFeePerGas': web3.to_wei('50', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address)

        })

        # Tanda tangani transaksi
        signed_txn = web3.eth.account.sign_transaction(mint_txn, private_key)

        # Kirim transaksi ke blockchain
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"✅ Minting sukses! TX Hash: {web3.to_hex(tx_hash)}")

    except Exception as e:
        print(f"❌ Gagal minting untuk {wallet_address}: {str(e)}")
