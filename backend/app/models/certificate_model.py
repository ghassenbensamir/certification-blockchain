from pydantic import BaseModel

class CertificateRequest(BaseModel):

    student_wallet: str
    student_name: str
    course: str
    issuer: str
    issue_date: str