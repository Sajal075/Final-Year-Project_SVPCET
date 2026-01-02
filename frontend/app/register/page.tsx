"use client";

import { useState } from "react";
import { ethers } from "ethers";
import { registerProduct } from "@/utils/contract";
import { connectWallet, getProvider } from "@/utils/web3";
import QRCodeDisplay from "@/components/QRCodeDisplay";
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001";

export default function RegisterProduct() {
  const [formData, setFormData] = useState({
    productName: "",
    description: "",
    manufacturer: "",
  });
  const [productId, setProductId] = useState<string>("");
  const [qrCode, setQrCode] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");

  const generateProductId = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/product/generate-id`);
      setProductId(response.data.productId);
    } catch (err: any) {
      setError("Failed to generate product ID: " + err.message);
    }
  };

  const generateQRCode = async () => {
    if (!productId) {
      setError("Please generate a product ID first");
      return;
    }
    try {
      const response = await axios.get(`${API_URL}/api/qr/${productId}`);
      setQrCode(response.data.qrData);
    } catch (err: any) {
      setError("Failed to generate QR code: " + err.message);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      // Connect wallet
      const account = await connectWallet();
      if (!account) {
        throw new Error("Please connect your wallet");
      }

      // Generate product ID if not exists
      let finalProductId = productId;
      if (!finalProductId) {
        const response = await axios.get(`${API_URL}/api/product/generate-id`);
        finalProductId = response.data.productId;
        setProductId(finalProductId);
      }

      // Register product on blockchain
      const tx = await registerProduct(
        finalProductId,
        formData.productName,
        formData.description,
        formData.manufacturer
      );

      setSuccess(`Transaction sent: ${tx.hash}. Waiting for confirmation...`);
      await tx.wait();
      setSuccess(`Product registered successfully! Transaction: ${tx.hash}`);

      // Generate QR code
      await generateQRCode();
    } catch (err: any) {
      setError(err.message || "Failed to register product");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">Register New Product</h1>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Name
            </label>
            <input
              type="text"
              required
              value={formData.productName}
              onChange={(e) =>
                setFormData({ ...formData, productName: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Manufacturer Name
            </label>
            <input
              type="text"
              required
              value={formData.manufacturer}
              onChange={(e) =>
                setFormData({ ...formData, manufacturer: e.target.value })
              }
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <div className="flex gap-4">
            <button
              type="button"
              onClick={generateProductId}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              Generate Product ID
            </button>
            {productId && (
              <div className="flex items-center text-gray-700">
                Product ID: <span className="font-mono ml-2">{productId}</span>
              </div>
            )}
          </div>

          {error && (
            <div className="bg-red-100 text-red-700 p-4 rounded">{error}</div>
          )}

          {success && (
            <div className="bg-green-100 text-green-700 p-4 rounded">
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Registering..." : "Register Product"}
          </button>
        </form>

        {qrCode && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold mb-4">Product QR Code</h2>
            <QRCodeDisplay value={qrCode} />
            <p className="text-sm text-gray-600 mt-4 text-center">
              Scan this QR code to track the product through the supply chain
            </p>
          </div>
        )}
      </div>
    </div>
  );
}



