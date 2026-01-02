const hre = require("hardhat");

async function main() {
  console.log("Deploying ProductTracker contract...");

  const ProductTracker = await hre.ethers.getContractFactory("ProductTracker");
  const productTracker = await ProductTracker.deploy();

  await productTracker.waitForDeployment();

  const address = await productTracker.getAddress();
  console.log("ProductTracker deployed to:", address);
  console.log("Network:", hre.network.name);
  console.log("Chain ID:", (await hre.ethers.provider.getNetwork()).chainId);

  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    address: address,
    network: hre.network.name,
    chainId: (await hre.ethers.provider.getNetwork()).chainId,
    timestamp: new Date().toISOString(),
  };

  fs.writeFileSync(
    `./deployments/${hre.network.name}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );

  console.log("Deployment info saved to deployments/", hre.network.name, ".json");

  // Verify contract on Etherscan (for testnets/mainnet)
  if (hre.network.name !== "localhost" && hre.network.name !== "hardhat") {
    console.log("Waiting for block confirmations...");
    await productTracker.deploymentTransaction().wait(6);

    try {
      await hre.run("verify:verify", {
        address: address,
        constructorArguments: [],
      });
      console.log("Contract verified on Etherscan");
    } catch (error) {
      console.log("Verification failed:", error.message);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

