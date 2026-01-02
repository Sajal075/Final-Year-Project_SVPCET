"use client";

import { useState, useEffect } from "react";
import { getProvider, connectWallet, formatAddress } from "@/utils/web3";
import { getContractReadOnly } from "@/utils/contract";
import { ethers } from "ethers";
import ProductTrackerABI from "@/contracts/ProductTracker.json";

export default function Dashboard() {
  const [account, setAccount] = useState<string | null>(null);
  const [role, setRole] = useState<string>("");
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    checkWalletConnection();
    if (account) {
      checkRole();
      // Note: In production, use event indexing or The Graph to fetch all products
    }
  }, [account]);

  const checkWalletConnection = async () => {
    if (typeof window.ethereum !== "undefined") {
      const accounts = await window.ethereum.request({ method: "eth_accounts" });
      if (accounts.length > 0) {
        setAccount(accounts[0]);
      }
    }
  };

  const checkRole = async () => {
    if (!account) return;
    const contract = getContractReadOnly();
    if (!contract) return;

    try {
      const [
        isManufacturer,
        isWarehouse,
        isLogistics,
        isDistributor,
        isRetailer,
      ] = await Promise.all([
        contract.authorizedManufacturers(account),
        contract.authorizedWarehouse(account),
        contract.authorizedLogistics(account),
        contract.authorizedDistributor(account),
        contract.authorizedRetailer(account),
      ]);

      if (isManufacturer) setRole("Manufacturer");
      else if (isWarehouse) setRole("Warehouse");
      else if (isLogistics) setRole("Logistics");
      else if (isDistributor) setRole("Distributor");
      else if (isRetailer) setRole("Retailer");
      else setRole("Unauthorized");
    } catch (error) {
      console.error("Error checking role:", error);
    }
  };

  const handleConnect = async () => {
    const address = await connectWallet();
    if (address) {
      setAccount(address);
    }
  };

  const fetchProducts = async () => {
    // This is a simplified version
    // In production, you would use event indexing or The Graph
    setLoading(true);
    try {
      // Listen to ProductRegistered events
      const contract = getContractReadOnly();
      if (!contract) return;

      const filter = contract.filters.ProductRegistered();
      const events = await contract.queryFilter(filter);
      // Process events...
    } catch (error) {
      console.error("Error fetching products:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

      {!account ? (
        <div className="bg-white rounded-lg shadow-lg p-6 text-center">
          <p className="text-gray-600 mb-4">Please connect your wallet to view the dashboard</p>
          <button
            onClick={handleConnect}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Connect Wallet
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Account Information</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Wallet Address</p>
                <p className="font-mono">{formatAddress(account)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Role</p>
                <p className="font-semibold">{role || "Checking..."}</p>
              </div>
            </div>
          </div>

          {role === "Manufacturer" && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Manufacturer Dashboard</h2>
              <div className="grid md:grid-cols-3 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Total Products</p>
                  <p className="text-2xl font-bold">-</p>
                  <p className="text-xs text-gray-500">Use event indexing to fetch</p>
                </div>
                <div className="bg-green-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Products Sold</p>
                  <p className="text-2xl font-bold">-</p>
                  <p className="text-xs text-gray-500">Use event indexing to fetch</p>
                </div>
                <div className="bg-purple-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Total Revenue</p>
                  <p className="text-2xl font-bold">-</p>
                  <p className="text-xs text-gray-500">Not tracked on-chain</p>
                </div>
              </div>

              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-4">Recent Products</h3>
                <p className="text-gray-600">
                  To view all products, implement event indexing or use The Graph protocol
                  to index ProductRegistered and ProductSold events from the blockchain.
                </p>
              </div>
            </div>
          )}

          {(role === "Warehouse" || role === "Logistics" || role === "Distributor" || role === "Retailer") && (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Supply Chain Dashboard</h2>
              <p className="text-gray-600 mb-4">
                You are authorized as: <span className="font-semibold">{role}</span>
              </p>
              <p className="text-gray-600">
                To update product status, go to the Verify page, scan or enter a product ID,
                and update the product at your stage of the supply chain.
              </p>
            </div>
          )}

          {role === "Unauthorized" && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-2">Not Authorized</h2>
              <p className="text-gray-700">
                Your wallet address is not authorized for any role. Please contact the contract
                owner to get authorized as a manufacturer, warehouse, logistics, distributor, or retailer.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}



