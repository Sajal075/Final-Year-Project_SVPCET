/**
 * Script to generate contract ABI for backend use
 * Run this after compiling the contract: npx hardhat compile
 */

const fs = require("fs");
const path = require("path");

// Path to compiled contract artifacts
const artifactPath = path.join(__dirname, "../../contracts/artifacts/contracts/ProductTracker.sol/ProductTracker.json");
const outputPath = path.join(__dirname, "../contracts/ProductTracker.json");

try {
  if (!fs.existsSync(artifactPath)) {
    console.error("Contract artifact not found. Please compile the contract first:");
    console.error("cd contracts && npx hardhat compile");
    process.exit(1);
  }

  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
  
  // Create output directory if it doesn't exist
  const outputDir = path.dirname(outputPath);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  // Extract ABI and contract address info
  const contractInfo = {
    abi: artifact.abi,
    contractName: artifact.contractName,
  };

  fs.writeFileSync(outputPath, JSON.stringify(contractInfo, null, 2));
  console.log("Contract ABI generated successfully at:", outputPath);
} catch (error) {
  console.error("Error generating ABI:", error.message);
  process.exit(1);
}



