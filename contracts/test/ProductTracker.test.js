const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ProductTracker", function () {
  let productTracker;
  let owner;
  let manufacturer;
  let warehouse;
  let logistics;
  let distributor;
  let retailer;
  let buyer;

  beforeEach(async function () {
    [owner, manufacturer, warehouse, logistics, distributor, retailer, buyer] =
      await ethers.getSigners();

    const ProductTracker = await ethers.getContractFactory("ProductTracker");
    productTracker = await ProductTracker.deploy();

    // Authorize users
    await productTracker.authorizeManufacturer(manufacturer.address);
    await productTracker.authorizeWarehouse(warehouse.address);
    await productTracker.authorizeLogistics(logistics.address);
    await productTracker.authorizeDistributor(distributor.address);
    await productTracker.authorizeRetailer(retailer.address);
  });

  describe("Deployment", function () {
    it("Should set the right owner", async function () {
      expect(await productTracker.owner()).to.equal(owner.address);
    });

    it("Should authorize owner as manufacturer", async function () {
      expect(await productTracker.authorizedManufacturers(owner.address)).to.be.true;
    });
  });

  describe("Authorization", function () {
    it("Should authorize manufacturer", async function () {
      const newManufacturer = (await ethers.getSigners())[7];
      await productTracker.authorizeManufacturer(newManufacturer.address);
      expect(await productTracker.authorizedManufacturers(newManufacturer.address)).to.be.true;
    });

    it("Should reject unauthorized manufacturer registration", async function () {
      const unauthorized = (await ethers.getSigners())[7];
      await expect(
        productTracker
          .connect(unauthorized)
          .registerManufacturer(1, "Test Product", "Description", "Test Manufacturer")
      ).to.be.revertedWith("Not authorized as manufacturer");
    });
  });

  describe("Product Registration", function () {
    it("Should register a new product", async function () {
      const productId = 1;
      await expect(
        productTracker
          .connect(manufacturer)
          .registerManufacturer(productId, "Test Product", "Description", "Test Manufacturer")
      )
        .to.emit(productTracker, "ProductRegistered")
        .withArgs(productId, "Test Product", "Test Manufacturer", manufacturer.address);

      const product = await productTracker.getProduct(productId);
      expect(product.productId).to.equal(productId);
      expect(product.productName).to.equal("Test Product");
      expect(product.manufacturer).to.equal("Test Manufacturer");
    });

    it("Should reject duplicate product ID", async function () {
      const productId = 1;
      await productTracker
        .connect(manufacturer)
        .registerManufacturer(productId, "Test Product", "Description", "Test Manufacturer");

      await expect(
        productTracker
          .connect(manufacturer)
          .registerManufacturer(productId, "Another Product", "Description", "Test Manufacturer")
      ).to.be.revertedWith("Product ID already exists");
    });
  });

  describe("Supply Chain Updates", function () {
    const productId = 1;

    beforeEach(async function () {
      await productTracker
        .connect(manufacturer)
        .registerManufacturer(productId, "Test Product", "Description", "Test Manufacturer");
    });

    it("Should update warehouse information", async function () {
      await expect(
        productTracker
          .connect(warehouse)
          .updateWarehouse(productId, "Warehouse A", "Location A", "Stored")
      )
        .to.emit(productTracker, "WarehouseUpdated");

      const journey = await productTracker.getProductJourney(productId);
      expect(journey.length).to.equal(2); // manufacturer + warehouse
      expect(journey[1].nodeType).to.equal("warehouse");
    });

    it("Should update logistics information", async function () {
      await productTracker
        .connect(logistics)
        .updateLogistics(productId, "Logistics A", "Location B", "In transit");

      const journey = await productTracker.getProductJourney(productId);
      expect(journey[journey.length - 1].nodeType).to.equal("logistics");
    });

    it("Should update distributor information", async function () {
      await productTracker
        .connect(distributor)
        .updateDistributor(productId, "Distributor A", "Location C", "Received");

      const journey = await productTracker.getProductJourney(productId);
      expect(journey[journey.length - 1].nodeType).to.equal("distributor");
    });

    it("Should update retailer information", async function () {
      await productTracker
        .connect(retailer)
        .updateRetailer(productId, "Retailer A", "Location D", "In store");

      const journey = await productTracker.getProductJourney(productId);
      expect(journey[journey.length - 1].nodeType).to.equal("retailer");
    });
  });

  describe("Product Sale", function () {
    const productId = 1;

    beforeEach(async function () {
      await productTracker
        .connect(manufacturer)
        .registerManufacturer(productId, "Test Product", "Description", "Test Manufacturer");
    });

    it("Should mark product as sold", async function () {
      await expect(
        productTracker
          .connect(retailer)
          .markAsSold(productId, buyer.address, "John Doe", "john@example.com")
      )
        .to.emit(productTracker, "ProductSold")
        .withArgs(productId, buyer.address, "John Doe", await ethers.provider.getBlockNumber());

      const product = await productTracker.getProduct(productId);
      expect(product.isSold).to.be.true;
      expect(product.buyerAddress).to.equal(buyer.address);
      expect(product.buyerName).to.equal("John Doe");
    });

    it("Should reject selling already sold product", async function () {
      await productTracker
        .connect(retailer)
        .markAsSold(productId, buyer.address, "John Doe", "john@example.com");

      await expect(
        productTracker
          .connect(retailer)
          .markAsSold(productId, buyer.address, "Jane Doe", "jane@example.com")
      ).to.be.revertedWith("Product already sold");
    });
  });

  describe("Product Journey", function () {
    const productId = 1;

    it("Should return full product journey", async function () {
      await productTracker
        .connect(manufacturer)
        .registerManufacturer(productId, "Test Product", "Description", "Test Manufacturer");

      await productTracker
        .connect(warehouse)
        .updateWarehouse(productId, "Warehouse A", "Location A", "Stored");

      await productTracker
        .connect(logistics)
        .updateLogistics(productId, "Logistics A", "Location B", "In transit");

      const journey = await productTracker.getProductJourney(productId);
      expect(journey.length).to.equal(3);
      expect(journey[0].nodeType).to.equal("manufacturer");
      expect(journey[1].nodeType).to.equal("warehouse");
      expect(journey[2].nodeType).to.equal("logistics");
    });
  });
});



