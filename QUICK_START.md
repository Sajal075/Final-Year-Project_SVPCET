# Quick Start Guide

## Prerequisites

- Node.js v18 or higher
- npm or yarn
- MetaMask browser extension
- Git

## Installation

1. **Clone and Install Dependencies**

```bash
# Install root dependencies
npm install

# Install contract dependencies
cd contracts && npm install && cd ..

# Install backend dependencies
cd backend && npm install && cd ..

# Install frontend dependencies
cd frontend && npm install && cd ..
```

## Local Development Setup

### Step 1: Start Local Blockchain

```bash
cd contracts
npx hardhat node
```

Keep this terminal running. This starts a local Ethereum node with test accounts.

### Step 2: Deploy Contract

In a new terminal (make sure you're in the project root, then navigate to contracts):

```bash
cd contracts
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

**Important:** Make sure you're in the `contracts/` directory (not `contracts/contracts/`) when running these commands.

Copy the deployed contract address from the output (it will look like `0x...`).

### Step 3: Configure Environment Variables

**Backend (.env in backend directory):**

```env
PORT=3001
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
RPC_URL=http://localhost:8545
PRIVATE_KEY=your_private_key_here
```

**Frontend (.env.local in frontend directory):**

```env
NEXT_PUBLIC_CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
NEXT_PUBLIC_RPC_URL=http://localhost:8545
NEXT_PUBLIC_CHAIN_ID=31337
NEXT_PUBLIC_API_URL=http://localhost:3001
```

Replace the contract address with the one from Step 2.

### Step 4: Generate Contract ABI

```bash
cd backend
node scripts/generate-abi.js
```

### Step 5: Start Backend

```bash
cd backend
npm run dev
```

Backend runs on `http://localhost:3001`

### Step 6: Start Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

Frontend runs on `http://localhost:3000`

## Using the Application

### 1. Connect MetaMask

1. Open `http://localhost:3000` in your browser
2. Install MetaMask if not installed
3. Click "Connect Wallet" in the navbar
4. Add local network to MetaMask:
   - Network Name: Localhost 8545
   - RPC URL: http://localhost:8545
   - Chain ID: 31337
   - Currency Symbol: ETH

### 2. Authorize Users (First Time Setup)

You need to authorize your wallet address for different roles. Use the Hardhat console or create a script:

```bash
cd contracts
npx hardhat console --network localhost
```

Then in the console:

```javascript
const ProductTracker = await ethers.getContractFactory("ProductTracker");
const contract = await ProductTracker.attach("YOUR_CONTRACT_ADDRESS");
const [owner, user1] = await ethers.getSigners();

// Authorize as manufacturer
await contract.authorizeManufacturer(user1.address);
await contract.authorizeWarehouse(user1.address);
await contract.authorizeLogistics(user1.address);
await contract.authorizeDistributor(user1.address);
await contract.authorizeRetailer(user1.address);
```

### 3. Register a Product

1. Go to "Register Product" page
2. Fill in product details:
   - Product Name
   - Description
   - Manufacturer Name
3. Click "Generate Product ID"
4. Click "Register Product"
5. Approve transaction in MetaMask
6. Wait for confirmation
7. QR code will be displayed

### 4. Update Supply Chain

1. Go to "Update Status" page
2. Select update type (Warehouse, Logistics, Distributor, Retailer)
3. Scan QR code or enter Product ID
4. Fill in details (name, location, notes)
5. Click "Update Product"
6. Approve transaction in MetaMask

### 5. Verify Product

1. Go to "Verify Product" page
2. Scan QR code or enter Product ID
3. View product information and supply chain journey
4. Verify authenticity

### 6. Mark Product as Sold

1. Go to "Update Status" page
2. Select "Mark as Sold"
3. Scan QR code or enter Product ID
4. Enter buyer information
5. Click "Update Product"
6. Approve transaction in MetaMask

## Testing

### Run Smart Contract Tests

```bash
cd contracts
npm test
```

### Test the Full Flow

1. Register a product as manufacturer
2. Update warehouse status
3. Update logistics status
4. Update distributor status
5. Update retailer status
6. Mark product as sold
7. Verify product as buyer

## Troubleshooting

### MetaMask Connection Issues

- Ensure MetaMask is installed and unlocked
- Check that you're on the correct network (Localhost 8545)
- Try disconnecting and reconnecting

### Transaction Failures

- Check if you have enough ETH (use Hardhat accounts)
- Verify you're authorized for the operation
- Check contract address is correct

### Backend Not Starting

- Check if port 3001 is available
- Verify contract address in .env
- Check if contract ABI is generated

### Frontend Not Loading

- Check if backend is running
- Verify environment variables
- Check browser console for errors

## Next Steps

1. Read the full [DEPLOYMENT.md](./DEPLOYMENT.md) guide
2. Review [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) for detailed integration
3. Explore the codebase
4. Customize for your needs
5. Deploy to testnet for testing

## Support

For issues:
1. Check the documentation
2. Review error messages
3. Check contract deployment
4. Verify environment variables



