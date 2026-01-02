"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Blockchain Product Tracker
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Track products from manufacturer to buyer with full supply chain transparency
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mt-12">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Register Products</h2>
          <p className="text-gray-600 mb-4">
            Manufacturers can register new products and generate unique QR codes for tracking.
          </p>
          <Link
            href="/register"
            className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Register Product
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Verify Products</h2>
          <p className="text-gray-600 mb-4">
            Buyers can scan QR codes to verify product authenticity and view the full supply chain journey.
          </p>
          <Link
            href="/verify"
            className="inline-block bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Verify Product
          </Link>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Dashboard</h2>
          <p className="text-gray-600 mb-4">
            View products, sales data, and manage your supply chain operations.
          </p>
          <Link
            href="/dashboard"
            className="inline-block bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
          >
            View Dashboard
          </Link>
        </div>
      </div>

      <div className="mt-12 bg-blue-50 rounded-lg p-8">
        <h2 className="text-2xl font-semibold mb-4">How It Works</h2>
        <div className="grid md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
              1
            </div>
            <h3 className="font-semibold">Manufacture</h3>
            <p className="text-sm text-gray-600">Product is registered with unique ID</p>
          </div>
          <div className="text-center">
            <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
              2
            </div>
            <h3 className="font-semibold">Track</h3>
            <p className="text-sm text-gray-600">Supply chain nodes update product status</p>
          </div>
          <div className="text-center">
            <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
              3
            </div>
            <h3 className="font-semibold">Verify</h3>
            <p className="text-sm text-gray-600">Buyers scan QR code to verify authenticity</p>
          </div>
          <div className="text-center">
            <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-2 text-xl font-bold">
              4
            </div>
            <h3 className="font-semibold">Sell</h3>
            <p className="text-sm text-gray-600">Product is marked as sold with buyer info</p>
          </div>
        </div>
      </div>
    </div>
  );
}



