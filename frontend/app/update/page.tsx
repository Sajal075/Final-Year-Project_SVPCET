"use client";

import { useState } from "react";
import { connectWallet } from "@/utils/web3";
import {
  updateWarehouse,
  updateLogistics,
  updateDistributor,
  updateRetailer,
  markAsSold,
} from "@/utils/contract";
import QRScanner from "@/components/QRScanner";

type UpdateType = "warehouse" | "logistics" | "distributor" | "retailer" | "sale";

export default function UpdateProduct() {
  const [productId, setProductId] = useState<string>("");
  const [updateType, setUpdateType] = useState<UpdateType>("warehouse");
  const [formData, setFormData] = useState({
    name: "",
    location: "",
    notes: "",
    buyerName: "",
    buyerEmail: "",
    buyerAddress: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState<string>("");
  const [showScanner, setShowScanner] = useState(false);

  const handleScanSuccess = (decodedText: string) => {
    try {
      const data = JSON.parse(decodedText);
      if (data.productId) {
        setProductId(data.productId);
        setShowScanner(false);
      }
    } catch (err) {
      setProductId(decodedText);
      setShowScanner(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const account = await connectWallet();
      if (!account) {
        throw new Error("Please connect your wallet");
      }

      let tx;
      if (updateType === "warehouse") {
        tx = await updateWarehouse(productId, formData.name, formData.location, formData.notes);
      } else if (updateType === "logistics") {
        tx = await updateLogistics(productId, formData.name, formData.location, formData.notes);
      } else if (updateType === "distributor") {
        tx = await updateDistributor(productId, formData.name, formData.location, formData.notes);
      } else if (updateType === "retailer") {
        tx = await updateRetailer(productId, formData.name, formData.location, formData.notes);
      } else if (updateType === "sale") {
        if (!formData.buyerAddress || !formData.buyerName) {
          throw new Error("Buyer address and name are required");
        }
        tx = await markAsSold(
          productId,
          formData.buyerAddress,
          formData.buyerName,
          formData.buyerEmail || ""
        );
      }

      if (tx) {
        setSuccess(`Transaction sent: ${tx.hash}. Waiting for confirmation...`);
        await tx.wait();
        setSuccess(`Update successful! Transaction: ${tx.hash}`);
        // Reset form
        setFormData({
          name: "",
          location: "",
          notes: "",
          buyerName: "",
          buyerEmail: "",
          buyerAddress: "",
        });
      }
    } catch (err: any) {
      setError(err.message || "Failed to update product");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">Update Product Status</h1>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Update Type
          </label>
          <select
            value={updateType}
            onChange={(e) => setUpdateType(e.target.value as UpdateType)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="warehouse">Warehouse</option>
            <option value="logistics">Logistics</option>
            <option value="distributor">Distributor</option>
            <option value="retailer">Retailer</option>
            <option value="sale">Mark as Sold</option>
          </select>
        </div>

        <div className="mb-4">
          <button
            onClick={() => setShowScanner(!showScanner)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {showScanner ? "Hide Scanner" : "Scan QR Code"}
          </button>
        </div>

        {showScanner && (
          <div className="mb-6">
            <QRScanner
              onScanSuccess={handleScanSuccess}
              onScanFailure={(err) => console.log("Scan error:", err)}
            />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product ID
            </label>
            <input
              type="text"
              required
              value={productId}
              onChange={(e) => setProductId(e.target.value)}
              placeholder="Enter or scan product ID"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {updateType !== "sale" && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {updateType.charAt(0).toUpperCase() + updateType.slice(1)} Name
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location
                </label>
                <input
                  type="text"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Notes
                </label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </>
          )}

          {updateType === "sale" && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Buyer Address
                </label>
                <input
                  type="text"
                  required
                  value={formData.buyerAddress}
                  onChange={(e) => setFormData({ ...formData, buyerAddress: e.target.value })}
                  placeholder="0x..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Buyer Name
                </label>
                <input
                  type="text"
                  required
                  value={formData.buyerName}
                  onChange={(e) => setFormData({ ...formData, buyerName: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Buyer Email
                </label>
                <input
                  type="email"
                  value={formData.buyerEmail}
                  onChange={(e) => setFormData({ ...formData, buyerEmail: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </>
          )}

          {error && (
            <div className="bg-red-100 text-red-700 p-4 rounded">{error}</div>
          )}

          {success && (
            <div className="bg-green-100 text-green-700 p-4 rounded">{success}</div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? "Updating..." : "Update Product"}
          </button>
        </form>
      </div>
    </div>
  );
}



