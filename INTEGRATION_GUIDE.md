# Integration Guide

## Overview

This guide explains how to integrate the ProductTracker smart contract with the frontend and backend, generate QR codes, and implement all core functionalities.

## Architecture

```
┌─────────────┐
│   Frontend  │ (Next.js/React)
│  (Browser)  │
└──────┬──────┘
       │
       │ HTTP API
       │
┌──────▼──────┐
│   Backend   │ (Node.js/Express)
│     API     │
└──────┬──────┘
       │
       │ ethers.js
       │
┌──────▼──────┐
│   Ethereum  │
│  Blockchain │
└─────────────┘
```

## Smart Contract Integration

### 1. Contract Deployment

```bash
cd contracts
npx hardhat compile
npx hardhat run scripts/deploy.js --network localhost
```

### 2. Contract ABI

The contract ABI is stored in:
- `backend/contracts/ProductTracker.json`
- `frontend/contracts/ProductTracker.json`

After compiling, generate the ABI:
```bash
cd backend
node scripts/generate-abi.js
```

### 3. Contract Address

Set the contract address in:
- `backend/.env`: `CONTRACT_ADDRESS=0x...`
- `frontend/.env.local`: `NEXT_PUBLIC_CONTRACT_ADDRESS=0x...`

## QR Code Generation

### Backend API

The backend provides an endpoint to generate QR codes:

```javascript
GET /api/qr/:productId
```

Response:
```json
{
  "success": true,
  "productId": "1234567890",
  "qrCode": "data:image/png;base64,...",
  "qrData": "{\"productId\":\"1234567890\",\"contractAddress\":\"0x...\",\"timestamp\":1234567890}"
}
```

### Frontend Generation

QR codes can be generated using the `qrcode.react` library:

```typescript
import QRCodeDisplay from "@/components/QRCodeDisplay";

<QRCodeDisplay value={qrData} size={256} level="H" />
```

### QR Code Data Format

```json
{
  "productId": "1234567890",
  "contractAddress": "0x...",
  "timestamp": 1234567890
}
```

## Wallet Authentication

### MetaMask Integration

1. Check if MetaMask is installed:
```typescript
if (typeof window.ethereum !== "undefined") {
  // MetaMask is installed
}
```

2. Connect wallet:
```typescript
const accounts = await window.ethereum.request({
  method: "eth_requestAccounts",
});
```

3. Get provider and signer:
```typescript
const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();
```

### Authorization

Users must be authorized for specific roles:
- Manufacturer: Can register products
- Warehouse: Can update warehouse status
- Logistics: Can update logistics status
- Distributor: Can update distributor status
- Retailer: Can update retailer status and mark products as sold

Check authorization:
```typescript
const isAuthorized = await contract.authorizedManufacturers(address);
```

## Product Registration Flow

1. **Generate Product ID**
   - Frontend calls: `GET /api/product/generate-id`
   - Backend generates unique ID using UUID

2. **Generate QR Code**
   - Frontend calls: `GET /api/qr/:productId`
   - Backend generates QR code with product data

3. **Register on Blockchain**
   - User connects wallet (MetaMask)
   - Frontend calls: `registerProduct(productId, name, description, manufacturer)`
   - Transaction is sent to blockchain
   - Wait for confirmation

4. **Display QR Code**
   - Show QR code to manufacturer
   - QR code can be printed and attached to product

## Supply Chain Update Flow

1. **Scan QR Code**
   - User scans QR code using camera
   - Extract product ID from QR data

2. **Verify Authorization**
   - Check if user's wallet is authorized for the role
   - Display appropriate update form

3. **Update Status**
   - User fills form (name, location, notes)
   - Frontend calls appropriate function:
     - `updateWarehouse()`
     - `updateLogistics()`
     - `updateDistributor()`
     - `updateRetailer()`
   - Transaction is sent to blockchain
   - Wait for confirmation

## Buyer Verification Flow

1. **Scan QR Code**
   - Buyer scans product QR code
   - Extract product ID

2. **Fetch Product Data**
   - Frontend calls: `getProduct(productId)`
   - Frontend calls: `getProductJourney(productId)`

3. **Display Information**
   - Show product details
   - Show supply chain journey
   - Verify authenticity

## Product Sale Flow

1. **Scan QR Code**
   - Retailer scans product QR code
   - Extract product ID

2. **Enter Buyer Information**
   - Buyer name
   - Buyer email
   - Buyer wallet address (optional)

3. **Mark as Sold**
   - Frontend calls: `markAsSold(productId, buyerAddress, buyerName, buyerEmail)`
   - Transaction is sent to blockchain
   - Product is marked as sold

## Manufacturer Dashboard

### Viewing Products

Currently, the dashboard shows a placeholder. To implement full functionality:

1. **Event Indexing** (Recommended)
   - Use The Graph protocol to index events
   - Index `ProductRegistered` events
   - Index `ProductSold` events
   - Query indexed data for product listing

2. **Direct Event Querying**
   - Query `ProductRegistered` events from contract
   - Filter by manufacturer address
   - Display products

### Sales Analytics

1. Query `ProductSold` events
2. Filter by manufacturer
3. Calculate metrics:
   - Total products sold
   - Sales by date
   - Buyer information

## Error Handling

### Common Errors

1. **"Not authorized"**
   - User's wallet is not authorized for the operation
   - Solution: Contact contract owner to authorize address

2. **"Product does not exist"**
   - Product ID is invalid or not registered
   - Solution: Verify product ID and registration

3. **"Product already sold"**
   - Product has already been marked as sold
   - Solution: Cannot mark as sold twice

4. **Transaction failed**
   - Insufficient gas
   - Network error
   - Solution: Check gas price, network connection

### Error Handling in Code

```typescript
try {
  const tx = await contract.registerManufacturer(...);
  await tx.wait();
  // Success
} catch (error: any) {
  if (error.code === "ACTION_REJECTED") {
    // User rejected transaction
  } else if (error.code === "INSUFFICIENT_FUNDS") {
    // Insufficient funds
  } else {
    // Other error
  }
}
```

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

### Integration Tests

1. Deploy contract to local network
2. Start backend server
3. Start frontend
4. Test full flow:
   - Register product
   - Generate QR code
   - Update supply chain
   - Verify product
   - Mark as sold

## Performance Optimization

### 1. Event Indexing

Use The Graph for efficient event querying:
- Index all contract events
- Create GraphQL API
- Query indexed data instead of on-chain queries

### 2. Caching

- Cache product data in backend
- Use Redis for frequently accessed data
- Cache QR codes

### 3. Batch Operations

- Batch multiple updates in single transaction
- Use multicall for multiple reads

## Security Best Practices

1. **Input Validation**
   - Validate all user inputs
   - Sanitize strings
   - Check product ID format

2. **Authorization**
   - Always check authorization on-chain
   - Don't rely on frontend checks alone

3. **Error Messages**
   - Don't expose sensitive information in error messages
   - Log errors server-side

4. **Gas Optimization**
   - Optimize contract functions
   - Use events for off-chain data

## Next Steps

1. Implement event indexing (The Graph)
2. Add product image storage (IPFS)
3. Implement batch operations
4. Add email notifications
5. Create mobile app
6. Add analytics dashboard
7. Implement user authentication
8. Add role-based access control

## Support

For issues and questions:
- Check documentation
- Review contract code
- Test on testnet first
- Contact development team



