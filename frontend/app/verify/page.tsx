"use client";

import { useState } from "react";
import QRScanner from "@/components/QRScanner";
import { getProduct, getProductJourney, Product, SupplyChainNode } from "@/utils/contract";
import { formatDate } from "@/utils/web3";

export default function VerifyProduct() {
  const [productId, setProductId] = useState<string>("");
  const [product, setProduct] = useState<Product | null>(null);
  const [journey, setJourney] = useState<SupplyChainNode[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [showScanner, setShowScanner] = useState(false);

  const handleScanSuccess = (decodedText: string) => {
    try {
      const data = JSON.parse(decodedText);
      if (data.productId) {
        setProductId(data.productId);
        fetchProductData(data.productId);
        setShowScanner(false);
      }
    } catch (err) {
      // If not JSON, assume it's just the product ID
      setProductId(decodedText);
      fetchProductData(decodedText);
      setShowScanner(false);
    }
  };

  const fetchProductData = async (id: string) => {
    setLoading(true);
    setError("");
    try {
      const [productData, journeyData] = await Promise.all([
        getProduct(id),
        getProductJourney(id),
      ]);
      setProduct(productData);
      setJourney(journeyData);
    } catch (err: any) {
      setError(err.message || "Failed to fetch product data");
      setProduct(null);
      setJourney([]);
    } finally {
      setLoading(false);
    }
  };

  const handleManualVerify = () => {
    if (productId) {
      fetchProductData(productId);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold mb-8">Verify Product</h1>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
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

        <div className="flex gap-4">
          <input
            type="text"
            placeholder="Enter Product ID"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
          />
          <button
            onClick={handleManualVerify}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Verify
          </button>
        </div>
      </div>

      {loading && (
        <div className="bg-white rounded-lg shadow-lg p-6 text-center">
          <p>Loading product information...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-6">{error}</div>
      )}

      {product && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Product Information</h2>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Product ID</p>
                <p className="font-mono font-semibold">{product.productId}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Product Name</p>
                <p className="font-semibold">{product.productName}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Manufacturer</p>
                <p>{product.manufacturer}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Manufacturing Date</p>
                <p>{formatDate(product.manufacturingDate)}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Status</p>
                <p className={product.isSold ? "text-green-600 font-semibold" : "text-blue-600 font-semibold"}>
                  {product.isSold ? "Sold" : "Available"}
                </p>
              </div>
              {product.isSold && (
                <>
                  <div>
                    <p className="text-sm text-gray-600">Buyer Name</p>
                    <p>{product.buyerName}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Sale Date</p>
                    <p>{formatDate(product.saleDate)}</p>
                  </div>
                </>
              )}
            </div>
            <div className="mt-4">
              <p className="text-sm text-gray-600">Description</p>
              <p>{product.description || "No description provided"}</p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Supply Chain Journey</h2>
            {journey.length === 0 ? (
              <p className="text-gray-600">No supply chain data available</p>
            ) : (
              <div className="space-y-4">
                {journey.map((node, index) => (
                  <div
                    key={index}
                    className="border-l-4 border-blue-500 pl-4 py-2"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-semibold capitalize">{node.nodeType}</h3>
                        <p className="text-gray-700">{node.nodeName}</p>
                        {node.location && (
                          <p className="text-sm text-gray-600">Location: {node.location}</p>
                        )}
                        {node.notes && (
                          <p className="text-sm text-gray-600 mt-1">{node.notes}</p>
                        )}
                      </div>
                      <div className="text-right">
                        <p className="text-sm text-gray-500">
                          {formatDate(node.timestamp)}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="bg-green-50 rounded-lg p-6 border-2 border-green-500">
            <h3 className="text-xl font-semibold text-green-800 mb-2">
              ✓ Product Authenticated
            </h3>
            <p className="text-green-700">
              This product has been verified on the blockchain. The supply chain
              history is authentic and cannot be tampered with.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}



