let currentAccount = "";

async function connectWallet() {

    if(window.ethereum) {

        const accounts =
            await window.ethereum.request({
                method: 'eth_requestAccounts'
            });

        currentAccount = accounts[0];

        document.getElementById(
            "wallet"
        ).innerText =
            "Connected: " + currentAccount;

    } else {

        alert(
            "MetaMask not installed"
        );
    }
}

async function issueCertificate() {

    const data = {

        student_wallet:
            document.getElementById(
                "studentWallet"
            ).value,

        student_name:
            document.getElementById(
                "studentName"
            ).value,

        course:
            document.getElementById(
                "course"
            ).value,

        issuer:
            document.getElementById(
                "issuer"
            ).value,

        issue_date:
            document.getElementById(
                "issueDate"
            ).value
    };

    const response = await fetch(
        "http://127.0.0.1:8000/issue-certificate",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify(data)
        }
    );

    const result =
        await response.json();

    alert(
        JSON.stringify(result)
    );
}

async function verifyCertificate() {

    const id =
        document.getElementById(
            "certificateId"
        ).value;

    const response = await fetch(
        `http://127.0.0.1:8000/verify/${id}`
    );

    const result =
        await response.json();

    document.getElementById(
    "result"
).innerHTML = `

    <h3>
        Verification Result
    </h3>

    <p>
        Student:
        ${result.metadata.student_name}
    </p>

    <p>
        Course:
        ${result.metadata.course}
    </p>

    <p>
        Issuer:
        ${result.metadata.issuer}
    </p>

    <p>
        Valid:
        ${result.certificate.valid}
    </p>

    <a
        href="
        http://127.0.0.1:8000/download-pdf/${id}
        "
        target="_blank"
    >
        <button>
            Download PDF
        </button>
    </a>
`;
}

async function loadStudentCertificates() {

    const wallet =
        document.getElementById(
            "walletSearch"
        ).value;

    const response = await fetch(
        `http://127.0.0.1:8000/student-certificates/${wallet}`
    );

    const result =
        await response.json();

    const container =
        document.getElementById(
            "studentCertificates"
        );

    container.innerHTML = "";

    if(
        result.certificates.length === 0
    ) {

        container.innerHTML =
            "<p>No certificates found</p>";

        return;
    }

    result.certificates.forEach(cert => {

        const statusClass =
            cert.valid
                ? "badge-valid"
                : "badge-revoked";

        const statusText =
            cert.valid
                ? "VALID"
                : "REVOKED";

        container.innerHTML += `

            <div class="certificate-card">

                <h3>
                    Certificate #${cert.id}
                </h3>

                <p>
                    Student:
                    ${cert.student_name}
                </p>

                <p>
                    Course:
                    ${cert.course_name}
                </p>

                <p>
                    Wallet:
                    ${cert.student}
                </p>

                <div class="
                    badge ${statusClass}
                ">
                    ${statusText}
                </div>

                <br><br>

                <button
                    onclick="
                        verifyCertificateById(
                            ${cert.id}
                        )
                    "
                >
                    Verify
                </button>

                <a
                    href="
                    http://127.0.0.1:8000/download-pdf/${cert.id}
                    "
                    target="_blank"
                >
                    <button>
                        Download PDF
                    </button>
                </a>

            </div>
        `;
    });
}

async function revokeCertificate() {

    const id =
        document.getElementById(
            "revokeId"
        ).value;

    const response = await fetch(
        `http://127.0.0.1:8000/revoke/${id}`,
        {
            method: "POST"
        }
    );

    const result =
        await response.json();

    alert(
        result.message
    );
}

async function verifyCertificateById(id) {

    const response = await fetch(
        `http://127.0.0.1:8000/verify/${id}`
    );

    const result =
        await response.json();

    document.getElementById(
        "result"
    ).innerHTML = `

        <h3>
            Verification Result
        </h3>

        <p>
            Student:
            ${result.metadata.student_name}
        </p>

        <p>
            Course:
            ${result.metadata.course}
        </p>

        <p>
            Issuer:
            ${result.metadata.issuer}
        </p>

        <p>
            Valid:
            ${result.certificate.valid}
        </p>

        <a
            href="
            http://127.0.0.1:8000/download-pdf/${id}
            "
            target="_blank"
        >
            <button>
                Download PDF
            </button>
        </a>
    `;
}