const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const { ethers } = require("ethers");
const QRCode = require("qrcode");
const { v4: uuidv4 } = require("uuid");

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize blockchain connection
let provider;
let contract;
let wallet;

try {
  provider = new ethers.JsonRpcProvider(process.env.RPC_URL || "http://localhost:8545");
  
  if (process.env.PRIVATE_KEY) {
    wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
  }

  // Contract ABI
  let contractABI;
  try {
    const contractData = require("./contracts/ProductTracker.json");
    contractABI = contractData.abi || contractData;
  } catch (error) {
    console.warn("Contract ABI not found. Please run: node scripts/generate-abi.js");
    contractABI = [];
  }

  const contractAddress = process.env.CONTRACT_ADDRESS;

  if (contractAddress && contractABI.length > 0) {
    contract = new ethers.Contract(
      contractAddress,
      contractABI,
      wallet || provider
    );
    console.log("Contract initialized at:", contractAddress);
  } else {
    console.warn("Contract not initialized. Set CONTRACT_ADDRESS in .env");
  }
} catch (error) {
  console.error("Error initializing blockchain connection:", error.message);
}

// Routes

/**
 * Health check endpoint
 */
app.get("/health", (req, res) => {
  res.json({ status: "ok", contractAddress: process.env.CONTRACT_ADDRESS });
});

/**
 * Generate QR code for a product ID
 * GET /api/qr/:productId
 */
app.get("/api/qr/:productId", async (req, res) => {
  try {
    const { productId } = req.params;
    
    // Generate QR code data URL
    const qrData = JSON.stringify({
      productId: productId,
      contractAddress: process.env.CONTRACT_ADDRESS,
      timestamp: Date.now(),
    });

    const qrCodeDataURL = await QRCode.toDataURL(qrData, {
      errorCorrectionLevel: "H",
      type: "image/png",
      quality: 0.92,
      margin: 1,
    });

    res.json({
      success: true,
      productId: productId,
      qrCode: qrCodeDataURL,
      qrData: qrData,
    });
  } catch (error) {
    console.error("Error generating QR code:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Generate unique product ID
 * GET /api/product/generate-id
 */
app.get("/api/product/generate-id", (req, res) => {
  try {
    // Generate a unique product ID (using UUID and timestamp)
    const productId = BigInt(`0x${uuidv4().replace(/-/g, "").substring(0, 16)}`);
    
    res.json({
      success: true,
      productId: productId.toString(),
    });
  } catch (error) {
    console.error("Error generating product ID:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Register a new product (manufacturer)
 * POST /api/product/register
 */
app.post("/api/product/register", async (req, res) => {
  try {
    const { productId, productName, description, manufacturer, signer } = req.body;

    if (!contract) {
      return res.status(500).json({ success: false, error: "Contract not initialized" });
    }

    if (!productId || !productName || !manufacturer) {
      return res.status(400).json({ success: false, error: "Missing required fields" });
    }

    // This endpoint assumes the transaction is sent from the frontend
    // For server-side transactions, uncomment below:
    /*
    const tx = await contract.registerManufacturer(
      productId,
      productName,
      description || "",
      manufacturer
    );
    await tx.wait();
    */

    res.json({
      success: true,
      message: "Product registration initiated",
      productId: productId,
    });
  } catch (error) {
    console.error("Error registering product:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Get product information
 * GET /api/product/:productId
 */
app.get("/api/product/:productId", async (req, res) => {
  try {
    const { productId } = req.params;

    if (!contract) {
      return res.status(500).json({ success: false, error: "Contract not initialized" });
    }

    const product = await contract.getProduct(productId);
    
    res.json({
      success: true,
      product: {
        productId: product.productId.toString(),
        productName: product.productName,
        description: product.description,
        manufacturer: product.manufacturer,
        manufacturingDate: product.manufacturingDate.toString(),
        isSold: product.isSold,
        buyerAddress: product.buyerAddress,
        buyerName: product.buyerName,
        buyerEmail: product.buyerEmail,
        saleDate: product.saleDate.toString(),
      },
    });
  } catch (error) {
    console.error("Error fetching product:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Get product journey (supply chain history)
 * GET /api/product/:productId/journey
 */
app.get("/api/product/:productId/journey", async (req, res) => {
  try {
    const { productId } = req.params;

    if (!contract) {
      return res.status(500).json({ success: false, error: "Contract not initialized" });
    }

    const journey = await contract.getProductJourney(productId);
    
    const formattedJourney = journey.map((node) => ({
      nodeType: node.nodeType,
      nodeName: node.nodeName,
      location: node.location,
      timestamp: node.timestamp.toString(),
      notes: node.notes,
    }));

    res.json({
      success: true,
      journey: formattedJourney,
    });
  } catch (error) {
    console.error("Error fetching product journey:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Update warehouse information
 * POST /api/supply-chain/warehouse
 */
app.post("/api/supply-chain/warehouse", async (req, res) => {
  try {
    const { productId, warehouseName, location, notes } = req.body;

    if (!contract) {
      return res.status(500).json({ success: false, error: "Contract not initialized" });
    }

    // Transaction should be sent from frontend with user's wallet
    res.json({
      success: true,
      message: "Warehouse update initiated",
      productId: productId,
    });
  } catch (error) {
    console.error("Error updating warehouse:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Get all products for a manufacturer
 * Note: This requires indexing events or using The Graph
 * For now, returns a message suggesting event-based approach
 */
app.get("/api/manufacturer/products", async (req, res) => {
  try {
    // In production, use event indexing or The Graph
    res.json({
      success: true,
      message: "Use event indexing or The Graph to fetch all products",
      products: [],
    });
  } catch (error) {
    console.error("Error fetching manufacturer products:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * Get sales data for a manufacturer
 */
app.get("/api/manufacturer/sales", async (req, res) => {
  try {
    // In production, use event indexing to fetch ProductSold events
    res.json({
      success: true,
      message: "Use event indexing to fetch sales data",
      sales: [],
    });
  } catch (error) {
    console.error("Error fetching sales:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
  console.log(`Contract address: ${process.env.CONTRACT_ADDRESS || "Not set"}`);
});

