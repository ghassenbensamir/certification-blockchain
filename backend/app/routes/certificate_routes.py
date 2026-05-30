import requests

from fastapi import APIRouter

from app.models.certificate_model import (
    CertificateRequest
)

from app.ipfs.pinata_service import (
    upload_to_ipfs
)

from app.blockchain.web3_service import (

    get_latest_certificate_id,
    issue_certificate,
    verify_certificate,
    revoke_certificate
)
from app.blockchain.pdf_service import generate_pdf, generate_qr

router = APIRouter()

@router.post("/issue-certificate")
def create_certificate(
    data: CertificateRequest
):

    metadata = {
        "student_name":
            data.student_name,

        "course":
            data.course,

        "issuer":
            data.issuer,

        "issue_date":
            data.issue_date,

        "student_wallet":
            data.student_wallet
    }

    ipfs_hash = upload_to_ipfs(
        metadata
    )

    tx_hash = issue_certificate(
    data.student_wallet,
    data.student_name,
    data.course,
    ipfs_hash
    )
    certificate_id =get_latest_certificate_id()
    return {
        "message":
            "Certificate issued",
            
        "certificate_id":
        certificate_id,


        "ipfs_hash":
            ipfs_hash,

        "transaction_hash":
            tx_hash
    }

@router.get("/verify/{certificate_id}")
def verify(certificate_id: int):

    cert = verify_certificate(
        certificate_id
    )

    ipfs_url = (
    "https://gateway.pinata.cloud/ipfs/"
    f"{cert['ipfs_cid']}"
    )

    metadata = requests.get(
        ipfs_url
    ).json()

    return {
        "certificate": cert,
        "metadata": metadata
    }

@router.post("/revoke/{certificate_id}")
def revoke(certificate_id: int):

    tx_hash = revoke_certificate(
        certificate_id
    )

    return {
        "message":
            "Certificate revoked",

        "transaction_hash":
            tx_hash
    }
from app.blockchain.web3_service import (
    get_student_certificates
)

@router.get(
    "/student-certificates/{wallet}"
)
def student_certificates(
    wallet: str
):

    certs = get_student_certificates(
        wallet
    )

    return {
        "wallet": wallet,
        "certificates": certs
    }

from app.blockchain.web3_service import verify_certificate
import requests


@router.get("/download-pdf/{certificate_id}")
def get_certificate_pdf(certificate_id: int):

    # 1. blockchain data
    cert = verify_certificate(certificate_id)

    # 2. IPFS metadata
    ipfs_url = f"https://gateway.pinata.cloud/ipfs/{cert['ipfs_cid']}"
    metadata = requests.get(ipfs_url).json()

    # 3. QR generation
    #qr_path = generate_qr(certificate_id)

    # 4. PDF generation
    pdf_file = generate_pdf(metadata, certificate_id)

    return {
        "message": "PDF generated",
        "file": pdf_file
    }