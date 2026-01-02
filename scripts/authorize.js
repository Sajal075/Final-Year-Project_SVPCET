/**
 * Script to authorize users for different roles
 * Usage: npx hardhat run scripts/authorize.js --network localhost
 */

const hre = require("hardhat");

async function main() {
  // Get contract address from deployment or environment
  const contractAddress = process.env.CONTRACT_ADDRESS || "0x5FbDB2315678afecb367f032d93F642f64180aa3";
  
  console.log("Authorizing users for contract:", contractAddress);

  const ProductTracker = await hre.ethers.getContractFactory("ProductTracker");
  const contract = await ProductTracker.attach(contractAddress);

  // Get signers
  const [owner, user1, user2, user3, user4, user5] = await hre.ethers.getSigners();

  console.log("Owner address:", owner.address);

  // Authorize users (you can modify these addresses)
  try {
    // Authorize user1 as manufacturer
    let tx = await contract.authorizeManufacturer(user1.address);
    await tx.wait();
    console.log("✓ Authorized", user1.address, "as Manufacturer");

    // Authorize user2 as warehouse
    tx = await contract.authorizeWarehouse(user2.address);
    await tx.wait();
    console.log("✓ Authorized", user2.address, "as Warehouse");

    // Authorize user3 as logistics
    tx = await contract.authorizeLogistics(user3.address);
    await tx.wait();
    console.log("✓ Authorized", user3.address, "as Logistics");

    // Authorize user4 as distributor
    tx = await contract.authorizeDistributor(user4.address);
    await tx.wait();
    console.log("✓ Authorized", user4.address, "as Distributor");

    // Authorize user5 as retailer
    tx = await contract.authorizeRetailer(user5.address);
    await tx.wait();
    console.log("✓ Authorized", user5.address, "as Retailer");

    // Verify authorizations
    console.log("\nVerifying authorizations:");
    console.log("Manufacturer:", await contract.authorizedManufacturers(user1.address));
    console.log("Warehouse:", await contract.authorizedWarehouse(user2.address));
    console.log("Logistics:", await contract.authorizedLogistics(user3.address));
    console.log("Distributor:", await contract.authorizedDistributor(user4.address));
    console.log("Retailer:", await contract.authorizedRetailer(user5.address));

  } catch (error) {
    console.error("Error authorizing users:", error.message);
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

