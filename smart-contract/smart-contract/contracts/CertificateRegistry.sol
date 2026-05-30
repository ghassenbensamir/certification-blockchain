// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CertificateRegistry {

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    struct Certificate {
        uint256 id;
        address student;
        string studentName;
        string courseName;
        string ipfsCID;
        bool valid;
        uint256 issuedAt;
    }

    uint256 public certificateCount;

    mapping(uint256 => Certificate)
        public certificates;

    mapping(address => uint256[])
        public studentCertificates;

    modifier onlyOwner() {
        require(
            msg.sender == owner,
            "Not owner"
        );
        _;
    }

    event CertificateIssued(
        uint256 indexed id,
        address indexed student,
        string ipfsCID
    );

    event CertificateRevoked(
        uint256 indexed id
    );

    function issueCertificate(
        address _student,
        string memory _studentName,
        string memory _courseName,
        string memory _ipfsCID
    ) public onlyOwner {

        certificateCount++;

        certificates[certificateCount] =
            Certificate({
                id: certificateCount,
                student: _student,
                studentName: _studentName,
                courseName: _courseName,
                ipfsCID: _ipfsCID,
                valid: true,
                issuedAt: block.timestamp
            });

        studentCertificates[_student]
            .push(certificateCount);

        emit CertificateIssued(
            certificateCount,
            _student,
            _ipfsCID
        );
    }

    function verifyCertificate(
        uint256 _id
    )
        public
        view
        returns (
            uint256,
            address,
            string memory,
            string memory,
            string memory,
            bool,
            uint256
        )
    {
        Certificate memory cert =
            certificates[_id];

        return (
            cert.id,
            cert.student,
            cert.studentName,
            cert.courseName,
            cert.ipfsCID,
            cert.valid,
            cert.issuedAt
        );
    }

    function revokeCertificate(
        uint256 _id
    ) public onlyOwner {

        certificates[_id].valid = false;

        emit CertificateRevoked(_id);
    }

    function getStudentCertificates(
        address _student
    )
        public
        view
        returns (
            uint256[] memory
        )
    {
        return studentCertificates[_student];
    }

    function getCertificateCount()
    public
    view
    returns(uint256)
{
    return certificateCount;
}
}