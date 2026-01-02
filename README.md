# Product Tracker - Blockchain Supply Chain Management System

A decentralized product authentication and supply chain management system built on Ethereum blockchain. This system tracks products from manufacturer to buyer, ensuring authenticity and full supply chain transparency using QR codes.

## 🚀 Features

- ✅ **Product Registration**: Generate unique product IDs and QR codes for each product
- ✅ **Supply Chain Tracking**: Update product status at each stage (warehouse, logistics, distributor, retailer)
- ✅ **Buyer Verification**: Scan QR codes to verify product authenticity and view full journey
- ✅ **Manufacturer Dashboard**: View products and sales information
- ✅ **Blockchain Timestamping**: Immutable records of all supply chain updates
- ✅ **Secure Authentication**: Wallet-based authentication using MetaMask
- ✅ **QR Code Generation & Scanning**: Full QR code support for product tracking
- ✅ **Role-Based Access Control**: Authorized users for each supply chain stage

## Project Structure

```
.
├── contracts/          # Smart contracts (Solidity)
├── backend/            # Node.js/Express API server
├── frontend/           # Next.js/React frontend
└── README.md
```

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- MetaMask browser extension
- Hardhat (for smart contract development)
- An Ethereum wallet with testnet ETH (for testing)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cursor
```

2. Install root dependencies:
```bash
npm install
```

3. Install contract dependencies:
```bash
cd contracts
npm install
```

4. Install backend dependencies:
```bash
cd ../backend
npm install
```

5. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

## Configuration

### Smart Contract Configuration

1. Create a `.env` file in the `contracts` directory:
```env
PRIVATE_KEY=your_private_key_here
SEPOLIA_RPC_URL=your_sepolia_rpc_url
ETHERSCAN_API_KEY=your_etherscan_api_key
```

### Backend Configuration

1. Create a `.env` file in the `backend` directory:
```env
PORT=3001
CONTRACT_ADDRESS=your_deployed_contract_address
RPC_URL=http://localhost:8545
PRIVATE_KEY=your_private_key_for_backend_operations
```

### Frontend Configuration

1. Create a `.env.local` file in the `frontend` directory:
```env
NEXT_PUBLIC_CONTRACT_ADDRESS=your_deployed_contract_address
NEXT_PUBLIC_RPC_URL=http://localhost:8545
NEXT_PUBLIC_CHAIN_ID=31337
```

## Deployment

### Local Development

1. Start local blockchain (Hardhat node):
```bash
cd contracts
npx hardhat node
```

2. Deploy contract to local network:
```bash
npm run deploy:local
```

3. Update contract address in backend and frontend `.env` files

4. Start backend server:
```bash
cd ../backend
npm run dev
```

5. Start frontend:
```bash
cd ../frontend
npm run dev
```

### Testnet Deployment (Sepolia)

1. Deploy contract to Sepolia:
```bash
cd contracts
npm run deploy:testnet
```

2. Update contract address in backend and frontend `.env` files with the deployed address

3. Update RPC URLs to use Sepolia RPC endpoint

## Usage

### For Manufacturers

1. Connect wallet (MetaMask)
2. Register new products with unique IDs
3. View product dashboard with all registered products
4. View sales and buyer information

### For Supply Chain Partners

1. Connect wallet (must be authorized)
2. Scan QR code of product
3. Update product status at your stage (warehouse/logistics/distributor/retailer)
4. Add location and notes

### For Buyers

1. Scan product QR code
2. View full product journey
3. Verify product authenticity
4. See manufacturing date and all supply chain nodes

## Testing

### Smart Contract Tests

```bash
cd contracts
npm test
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Technology Stack

- **Smart Contracts**: Solidity ^0.8.20
- **Blockchain**: Ethereum (Hardhat for development)
- **Backend**: Node.js, Express.js
- **Frontend**: Next.js, React, TypeScript
- **Blockchain Interaction**: ethers.js
- **QR Codes**: qrcode, qr-scanner
- **Authentication**: MetaMask, Web3

## Security Considerations

- Always use authorized addresses for supply chain updates
- Verify contract addresses before interacting
- Use environment variables for sensitive keys
- Test on testnets before mainnet deployment
- Regularly audit smart contract code

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.

