
## Overview
A decentralized application for issuing, verifying, revoking, and managing academic certificates using Blockchain and IPFS.

## Features
- Certificate issuance linked to a student's wallet
- Blockchain-based authenticity verification
- IPFS decentralized metadata storage
- Student certificate lookup by wallet address
- Certificate revocation
- PDF certificate generation
- QR-code based verification

## Technology Stack
- Solidity
- Hardhat
- Ganache
- FastAPI
- Web3.py
- HTML/CSS/JavaScript
- MetaMask
- Pinata IPFS

## Architecture
Frontend -> FastAPI -> Web3.py -> Smart Contract -> Blockchain
                            |
                            v
                          IPFS

## Installation
### Smart Contract
```bash
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### Backend
```bash
python -m venv venv
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
python -m http.server 5500
```

## Main Workflows

### Issue Certificate
1. Admin enters certificate information.
2. Metadata uploaded to IPFS.
3. CID stored on blockchain.
4. Certificate linked to student's wallet.

### Verify Certificate
1. User enters certificate ID.
2. Blockchain returns CID and status.
3. Metadata fetched from IPFS.
4. Authenticity displayed.

### Revoke Certificate
1. Admin revokes certificate.
2. Certificate status changes to REVOKED.
3. History remains immutable.

### Student Certificates
1. User enters wallet address.
2. Application retrieves all associated certificates.



