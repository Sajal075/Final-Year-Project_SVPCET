import { ethers } from "ethers";
import { getSigner, getProvider } from "./web3";
import ProductTrackerABI from "../contracts/ProductTracker.json";

const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS || "";

export interface Product {
  productId: string;
  productName: string;
  description: string;
  manufacturer: string;
  manufacturingDate: string;
  isSold: boolean;
  buyerAddress: string;
  buyerName: string;
  buyerEmail: string;
  saleDate: string;
}

export interface SupplyChainNode {
  nodeType: string;
  nodeName: string;
  location: string;
  timestamp: string;
  notes: string;
}

export const getContract = async (): Promise<ethers.Contract | null> => {
  const signer = await getSigner();
  if (signer && CONTRACT_ADDRESS) {
    return new ethers.Contract(CONTRACT_ADDRESS, ProductTrackerABI.abi, signer);
  }
  return null;
};

export const getContractReadOnly = (): ethers.Contract | null => {
  const provider = getProvider();
  if (provider && CONTRACT_ADDRESS) {
    return new ethers.Contract(CONTRACT_ADDRESS, ProductTrackerABI.abi, provider);
  }
  return null;
};

export const registerProduct = async (
  productId: string,
  productName: string,
  description: string,
  manufacturer: string
): Promise<ethers.ContractTransactionResponse> => {
  const contract = await getContract();
  if (!contract) throw new Error("Contract not initialized");

  return await contract.registerManufacturer(
    productId,
    productName,
    description,
    manufacturer
  );
};

export const updateWarehouse = async (
  productId: string,
  warehouseName: string,
  location: string,
  notes: string
): Promise<ethers.ContractTransactionResponse> => {
  const contract = await getContract();
  if (!contract) throw new Error("Contract not initialized");

  return await contract.updateWarehouse(productId, warehouseName, location, notes);
};

export const updateLogistics = async (
  productId: string,
  logisticsName: string,
  location: string,
  notes: string
): Promise<ethers.ContractTransactionResponse> => {
  const contract = await getContract();
  if (!contract) throw new Error("Contract not initialized");

  return await contract.updateLogistics(productId, logisticsName, location, notes);
};

export const updateDistributor = async (
  productId: string,
  distributorName: string,
  location: string,
  notes: string
): Promise<ethers.ContractTransactionResponse> => {
  const contract = await getContract();
  if (!contract) throw new Error("Contract not initialized");

  return await contract.updateDistributor(productId, distributorName, location, notes);
};

export const updateRetailer = async (
  productId: string,
  retailerName: string,
  location: string,
  notes: string
): Promise<ethers.ContractTransactionResponse> => {
  const contract = await getContract();
  if (!contract) throw new Error("Contract not initialized");

  return await contract.updateRetailer(productId, retailerName, location, notes);
};

export const markAsSold = async (
  productId: string,
  buyerAddress: string,
  buyerName: string,
  buyerEmail: string
): Promise<ethers.ContractTransactionResponse> => {
  const contract = await getContract();
  if (!contract) throw new Error("Contract not initialized");

  return await contract.markAsSold(productId, buyerAddress, buyerName, buyerEmail);
};

export const getProduct = async (productId: string): Promise<Product> => {
  const contract = getContractReadOnly();
  if (!contract) throw new Error("Contract not initialized");

  const product = await contract.getProduct(productId);
  return {
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
  };
};

export const getProductJourney = async (
  productId: string
): Promise<SupplyChainNode[]> => {
  const contract = getContractReadOnly();
  if (!contract) throw new Error("Contract not initialized");

  const journey = await contract.getProductJourney(productId);
  return journey.map((node: any) => ({
    nodeType: node.nodeType,
    nodeName: node.nodeName,
    location: node.location,
    timestamp: node.timestamp.toString(),
    notes: node.notes,
  }));
};



