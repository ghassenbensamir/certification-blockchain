const hre = require("hardhat");
const fs = require("fs");

async function main() {

    const CertificateRegistry =
        await hre.ethers.getContractFactory(
            "CertificateRegistry"
        );

    const contract =
        await CertificateRegistry.deploy();

    await contract.waitForDeployment();

    const address =
        await contract.getAddress();

    console.log(
        "Contract deployed to:",
        address
    );

    const artifact =
        await hre.artifacts.readArtifact(
            "CertificateRegistry"
        );

    fs.mkdirSync(
        "../backend/contract",
        { recursive: true }
    );

    fs.writeFileSync(
        "../backend/contract/abi.json",
        JSON.stringify(
            artifact.abi,
            null,
            2
        )
    );

    fs.writeFileSync(
        "../backend/contract/contract_address.txt",
        address
    );
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});