import qrcode

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_qr(certificate_id):

    verification_url = (
        f"http://127.0.0.1:8000/verify/"
        f"{certificate_id}"
    )

    qr = qrcode.make(verification_url)

    qr_path = (
        f"qr_{certificate_id}.png"
    )

    qr.save(qr_path)

    return qr_path


def generate_pdf(
    metadata,
    certificate_id
):

    pdf_path = (
        f"certificate_{certificate_id}.pdf"
    )

    qr_path = generate_qr(
        certificate_id
    )

    c = canvas.Canvas(
        pdf_path,
        pagesize=A4
    )

    c.setFont(
        "Helvetica-Bold",
        24
    )

    c.drawString(
        170,
        800,
        "ACADEMIC CERTIFICATE"
    )

    c.setFont(
        "Helvetica",
        14
    )

    c.drawString(
        100,
        720,
        f"Student: "
        f"{metadata['student_name']}"
    )

    c.drawString(
        100,
        690,
        f"Course: "
        f"{metadata['course']}"
    )

    c.drawString(
        100,
        660,
        f"Issuer: "
        f"{metadata['issuer']}"
    )

    c.drawString(
        100,
        630,
        f"Issue Date: "
        f"{metadata['issue_date']}"
    )

    c.drawImage(
        qr_path,
        380,
        580,
        width=120,
        height=120
    )

    c.drawString(
        340,
        560,
        "Scan to verify"
    )

    c.save()

    return pdf_path