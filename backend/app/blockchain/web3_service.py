import json
import os

from web3 import Web3
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
load_dotenv()

GANACHE_URL = os.getenv("GANACHE_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
CHAIN_ID = int(os.getenv("CHAIN_ID"))

web3 = Web3(
    Web3.HTTPProvider(GANACHE_URL)
)

with open(r"D:\blockchain-certification\smart-contract\backend\contract\abi.json", "r") as f:
    abi = json.load(f)

with open(
    r"D:\blockchain-certification\smart-contract\backend\contract\contract_address.txt",
    "r"
) as f:
    contract_address = f.read().strip()

contract = web3.eth.contract(
    address=contract_address,
    abi=abi
)

def issue_certificate(
    student_wallet,
    student_name,
    course_name,
    ipfs_cid
):

    nonce = web3.eth.get_transaction_count(
        WALLET_ADDRESS
    )

    transaction = (
        contract.functions.issueCertificate(
            student_wallet,
            student_name,
            course_name,
            ipfs_cid
        ).build_transaction({
            "chainId": CHAIN_ID,
            "gas": 3000000,
            "gasPrice": web3.to_wei(
                "20",
                "gwei"
            ),
            "nonce": nonce
        })
    )

    signed_txn = (
        web3.eth.account.sign_transaction(
            transaction,
            PRIVATE_KEY
        )
    )

    tx_hash = (
        web3.eth.send_raw_transaction(
            signed_txn.raw_transaction
        )
    )

    receipt = (
        web3.eth.wait_for_transaction_receipt(
            tx_hash
        )
    )

    return receipt.transactionHash.hex()

def verify_certificate(certificate_id):

    cert = (
        contract.functions.verifyCertificate(
            certificate_id
        ).call()
    )

    return {
        "id": cert[0],
        "student": cert[1],
        "student_name": cert[2],
        "course_name": cert[3],
        "ipfs_cid": cert[4],
        "valid": cert[5],
        "issued_at": cert[6]
    }

def revoke_certificate(certificate_id):

    nonce = web3.eth.get_transaction_count(
        WALLET_ADDRESS
    )

    transaction = (
        contract.functions.revokeCertificate(
            certificate_id
        ).build_transaction({
            "chainId": CHAIN_ID,
            "gas": 3000000,
            "gasPrice": web3.to_wei(
                "20",
                "gwei"
            ),
            "nonce": nonce
        })
    )

    signed_txn = (
        web3.eth.account.sign_transaction(
            transaction,
            PRIVATE_KEY
        )
    )

    tx_hash = (
        web3.eth.send_raw_transaction(
            signed_txn.raw_transaction
        )
    )

    receipt = (
        web3.eth.wait_for_transaction_receipt(
            tx_hash
        )
    )

    return receipt.transactionHash.hex()




def get_latest_certificate_id():

    return (
        contract.functions
        .getCertificateCount()
        .call()
    )


def get_student_certificates(
    wallet_address
):

    ids = (
        contract.functions
        .getStudentCertificates(
            wallet_address
        )
        .call()
    )

    certificates = []

    for cert_id in ids:

        cert = (
            contract.functions
            .verifyCertificate(cert_id)
            .call()
        )

        certificates.append({
            "id": cert[0],
            "student": cert[1],
            "student_name": cert[2],
            "course_name": cert[3],
            "ipfs_cid": cert[4],
            "valid": cert[5],
            "issued_at": cert[6]
        })

    return certificates