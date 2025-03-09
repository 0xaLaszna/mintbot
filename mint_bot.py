from dotenv import load_dotenv
import os
from web3 import Web3

# Load .env file
load_dotenv()

# Ambil semua private key dari .env
PRIVATE_KEYS = os.getenv("PRIVATE_KEYS")
if not PRIVATE_KEYS:
    raise ValueError("PRIVATE_KEYS tidak ditemukan di .env!")

PRIVATE_KEYS = PRIVATE_KEYS.split(",")  # Pisahkan jika ada banyak

# Hubungkan ke node Arbitrum
RPC_URL = os.getenv("RPC_URL")
web3 = Web3(Web3.HTTPProvider(RPC_URL))

if not web3.is_connected():
    raise Exception("Gagal terhubung ke jaringan Arbitrum!")

# Proses setiap private key
for private_key in PRIVATE_KEYS:
    account = web3.eth.account.from_key(private_key.strip())  # Inisialisasi akun
    wallet_address = account.address  # Ambil alamat wallet
    print(f"🔑 Menggunakan wallet: {wallet_address}")

    # Mulai proses minting
    try:
        contract_address = os.getenv("CONTRACT_ADDRESS")
        if not contract_address:
            raise ValueError("CONTRACT_ADDRESS tidak ditemukan di .env!")

        # Load ABI dari file JSON
        import json
        with open("contract_abi.json", "r") as f:
            contract_abi = json.load(f)

        # Inisialisasi kontrak
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)

        # Panggil fungsi minting
        mint_txn = contract.functions.mint().build_transaction({
            'from': wallet_address,
            'value': web3.to_wei(0.01, 'ether'),  # Sesuaikan dengan biaya minting
            'gas': 300000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(wallet_address)
        })

        # Tanda tangani transaksi
        signed_txn = web3.eth.account.sign_transaction(mint_txn, private_key.strip())

        # Kirim transaksi ke blockchain
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"✅ Minting sukses! TX Hash: {web3.to_hex(tx_hash)}")

    except Exception as e:
        print(f"❌ Gagal minting untuk {wallet_address}: {str(e)}")
