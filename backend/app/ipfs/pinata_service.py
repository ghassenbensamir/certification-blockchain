import os
import requests

from dotenv import load_dotenv

load_dotenv()

PINATA_API_KEY = os.getenv(
    "PINATA_API_KEY"
)

PINATA_SECRET_API_KEY = os.getenv(
    "PINATA_SECRET_API_KEY"
)

def upload_to_ipfs(metadata):
    student = metadata["student_name"]
    course = metadata["course"]

    filename = f"{student}_{course}_certificate.json"

    file_data = {
        "pinataMetadata": {
            "name": filename
        },
        "pinataContent": metadata
    }
    url = (
        "https://api.pinata.cloud/"
        "pinning/pinJSONToIPFS"
    )

    headers = {
        "pinata_api_key":
            PINATA_API_KEY,

        "pinata_secret_api_key":
            PINATA_SECRET_API_KEY,

        "Content-Type":
            "application/json"
    }

    response = requests.post(
        url,
        json=file_data,
        headers=headers
    )

    result = response.json()
    print("PINATA RESPONSE:", result) 
    return result["IpfsHash"]