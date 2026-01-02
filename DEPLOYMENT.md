# Deployment Guide

## Prerequisites

1. Node.js (v18 or higher)
2. npm or yarn
3. MetaMask browser extension
4. Hardhat (for smart contract development)
5. An Ethereum wallet with testnet ETH (for testing)

## Step 1: Install Dependencies

```bash
# Install root dependencies
npm install

# Install contract dependencies
cd contracts
npm install

# Install backend dependencies
cd ../backend
npm install

# Install frontend dependencies
cd ../frontend
npm install
```

## Step 2: Configure Environment Variables

### Contracts (.env in contracts directory)

```env
PRIVATE_KEY=your_private_key_here
SEPOLIA_RPC_URL=https://sepolia.infura.io/v3/your_project_id
ETHERSCAN_API_KEY=your_etherscan_api_key
```

### Backend (.env in backend directory)

```env
PORT=3001
CONTRACT_ADDRESS=your_deployed_contract_address
RPC_URL=http://localhost:8545
PRIVATE_KEY=your_private_key_for_backend_operations
```

### Frontend (.env.local in frontend directory)

```env
NEXT_PUBLIC_CONTRACT_ADDRESS=your_deployed_contract_address
NEXT_PUBLIC_RPC_URL=http://localhost:8545
NEXT_PUBLIC_CHAIN_ID=31337
NEXT_PUBLIC_API_URL=http://localhost:3001
```

## Step 3: Local Development Setup

### 3.1 Start Local Blockchain

```bash
cd contracts
npx hardhat node
```

This will start a local Hardhat node on `http://localhost:8545` with 20 test accounts.

### 3.2 Deploy Contract to Local Network

In a new terminal:

```bash
cd contracts
npm run deploy:local
```

Copy the deployed contract address and update it in:
- `backend/.env` (CONTRACT_ADDRESS)
- `frontend/.env.local` (NEXT_PUBLIC_CONTRACT_ADDRESS)

### 3.3 Generate Contract ABI for Backend

After compiling the contract:

```bash
cd contracts
npx hardhat compile
cd ../backend
node scripts/generate-abi.js
```

### 3.4 Start Backend Server

```bash
cd backend
npm run dev
```

Backend will run on `http://localhost:3001`

### 3.5 Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## Step 4: Testnet Deployment (Sepolia)

### 4.1 Deploy Contract to Sepolia

```bash
cd contracts
npm run deploy:sepolia
```

### 4.2 Update Configuration

Update the contract address in:
- `backend/.env` (CONTRACT_ADDRESS)
- `frontend/.env.local` (NEXT_PUBLIC_CONTRACT_ADDRESS)

Update RPC URLs to use Sepolia:
- `backend/.env` (RPC_URL)
- `frontend/.env.local` (NEXT_PUBLIC_RPC_URL and NEXT_PUBLIC_CHAIN_ID=11155111)

### 4.3 Authorize Users

After deployment, you need to authorize users for different roles. Connect to the contract owner wallet and call:

```javascript
// In a script or using ethers.js
await contract.authorizeManufacturer(manufacturerAddress);
await contract.authorizeWarehouse(warehouseAddress);
await contract.authorizeLogistics(logisticsAddress);
await contract.authorizeDistributor(distributorAddress);
await contract.authorizeRetailer(retailerAddress);
```

## Step 5: Mainnet Deployment

**WARNING**: Only deploy to mainnet after thorough testing on testnets.

1. Update all environment variables with mainnet values
2. Deploy contract: `npm run deploy:mainnet` (create a mainnet script)
3. Verify contract on Etherscan
4. Update all configuration files with mainnet contract address
5. Deploy backend and frontend to production servers

## Step 6: Production Deployment

### Backend Deployment

Options:
- Heroku
- AWS EC2
- DigitalOcean
- Railway

Set environment variables in your hosting platform.

### Frontend Deployment

Options:
- Vercel (recommended for Next.js)
- Netlify
- AWS Amplify

Set environment variables in your hosting platform.

## Troubleshooting

### Contract Not Found

- Ensure contract is deployed
- Verify contract address is correct in all .env files
- Check network (localhost vs testnet vs mainnet)

### Transaction Failures

- Check if wallet is connected
- Verify user is authorized for the operation
- Ensure sufficient gas/ETH balance
- Check if product exists (for updates)

### QR Code Not Scanning

- Ensure camera permissions are granted
- Use HTTPS in production (required for camera access)
- Try different browsers

### Backend API Errors

- Verify backend is running
- Check CORS configuration
- Verify contract ABI is generated correctly

## Security Considerations

1. **Never commit private keys** to version control
2. **Use environment variables** for all sensitive data
3. **Test thoroughly** on testnets before mainnet
4. **Verify smart contracts** on Etherscan
5. **Use HTTPS** in production
6. **Implement rate limiting** on API endpoints
7. **Validate all inputs** on both frontend and backend
8. **Use secure wallet connections** (MetaMask)

## Next Steps

1. Implement event indexing (The Graph) for better product listing
2. Add user authentication and session management
3. Implement analytics and reporting
4. Add email notifications
5. Create mobile app (React Native)
6. Implement batch operations for multiple products
7. Add product image upload and storage (IPFS)



