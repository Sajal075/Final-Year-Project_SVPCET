// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ProductTracker
 * @dev Smart contract for tracking products through the supply chain
 * @notice Each product has a unique ID and QR code that tracks its journey from manufacturer to buyer
 */
contract ProductTracker {
    // Struct to store product information
    struct Product {
        uint256 productId;
        string productName;
        string description;
        string manufacturer;
        uint256 manufacturingDate;
        bool isSold;
        address buyerAddress;
        string buyerName;
        string buyerEmail;
        uint256 saleDate;
    }

    // Struct to store supply chain information
    struct SupplyChainNode {
        string nodeType; // warehouse, logistics, distributor, retailer
        string nodeName;
        string location;
        uint256 timestamp;
        string notes;
    }

    // Mapping from productId to Product
    mapping(uint256 => Product) public products;

    // Mapping from productId to array of SupplyChainNode
    mapping(uint256 => SupplyChainNode[]) public productJourney;

    // Mapping to store authorized addresses for each role
    mapping(address => bool) public authorizedManufacturers;
    mapping(address => bool) public authorizedWarehouse;
    mapping(address => bool) public authorizedLogistics;
    mapping(address => bool) public authorizedDistributor;
    mapping(address => bool) public authorizedRetailer;

    // Events
    event ProductRegistered(
        uint256 indexed productId,
        string productName,
        string manufacturer,
        address indexed manufacturerAddress
    );

    event WarehouseUpdated(
        uint256 indexed productId,
        string warehouseName,
        string location,
        uint256 timestamp
    );

    event LogisticsUpdated(
        uint256 indexed productId,
        string logisticsName,
        string location,
        uint256 timestamp
    );

    event DistributorUpdated(
        uint256 indexed productId,
        string distributorName,
        string location,
        uint256 timestamp
    );

    event RetailerUpdated(
        uint256 indexed productId,
        string retailerName,
        string location,
        uint256 timestamp
    );

    event ProductSold(
        uint256 indexed productId,
        address indexed buyerAddress,
        string buyerName,
        uint256 saleDate
    );

    // Modifiers
    modifier onlyAuthorizedManufacturer() {
        require(
            authorizedManufacturers[msg.sender],
            "Not authorized as manufacturer"
        );
        _;
    }

    modifier onlyAuthorizedWarehouse() {
        require(authorizedWarehouse[msg.sender], "Not authorized as warehouse");
        _;
    }

    modifier onlyAuthorizedLogistics() {
        require(
            authorizedLogistics[msg.sender],
            "Not authorized as logistics"
        );
        _;
    }

    modifier onlyAuthorizedDistributor() {
        require(
            authorizedDistributor[msg.sender],
            "Not authorized as distributor"
        );
        _;
    }

    modifier onlyAuthorizedRetailer() {
        require(
            authorizedRetailer[msg.sender],
            "Not authorized as retailer"
        );
        _;
    }

    modifier productExists(uint256 _productId) {
        require(products[_productId].productId != 0, "Product does not exist");
        _;
    }

    // Constructor - deployer is the owner and can authorize users
    address public owner;

    constructor() {
        owner = msg.sender;
        // Owner is automatically authorized as manufacturer
        authorizedManufacturers[msg.sender] = true;
    }

    /**
     * @dev Authorize a manufacturer address
     */
    function authorizeManufacturer(address _address) external {
        require(msg.sender == owner, "Only owner can authorize");
        authorizedManufacturers[_address] = true;
    }

    /**
     * @dev Authorize a warehouse address
     */
    function authorizeWarehouse(address _address) external {
        require(msg.sender == owner, "Only owner can authorize");
        authorizedWarehouse[_address] = true;
    }

    /**
     * @dev Authorize a logistics address
     */
    function authorizeLogistics(address _address) external {
        require(msg.sender == owner, "Only owner can authorize");
        authorizedLogistics[_address] = true;
    }

    /**
     * @dev Authorize a distributor address
     */
    function authorizeDistributor(address _address) external {
        require(msg.sender == owner, "Only owner can authorize");
        authorizedDistributor[_address] = true;
    }

    /**
     * @dev Authorize a retailer address
     */
    function authorizeRetailer(address _address) external {
        require(msg.sender == owner, "Only owner can authorize");
        authorizedRetailer[_address] = true;
    }

    /**
     * @dev Register a new product by manufacturer
     * @param _productId Unique product ID
     * @param _productName Name of the product
     * @param _description Product description
     * @param _manufacturer Manufacturer name
     */
    function registerManufacturer(
        uint256 _productId,
        string memory _productName,
        string memory _description,
        string memory _manufacturer
    ) external onlyAuthorizedManufacturer {
        require(
            products[_productId].productId == 0,
            "Product ID already exists"
        );

        products[_productId] = Product({
            productId: _productId,
            productName: _productName,
            description: _description,
            manufacturer: _manufacturer,
            manufacturingDate: block.timestamp,
            isSold: false,
            buyerAddress: address(0),
            buyerName: "",
            buyerEmail: "",
            saleDate: 0
        });

        // Add manufacturing node to journey
        productJourney[_productId].push(
            SupplyChainNode({
                nodeType: "manufacturer",
                nodeName: _manufacturer,
                location: "",
                timestamp: block.timestamp,
                notes: "Product manufactured"
            })
        );

        emit ProductRegistered(
            _productId,
            _productName,
            _manufacturer,
            msg.sender
        );
    }

    /**
     * @dev Update warehouse information for a product
     */
    function updateWarehouse(
        uint256 _productId,
        string memory _warehouseName,
        string memory _location,
        string memory _notes
    ) external onlyAuthorizedWarehouse productExists(_productId) {
        productJourney[_productId].push(
            SupplyChainNode({
                nodeType: "warehouse",
                nodeName: _warehouseName,
                location: _location,
                timestamp: block.timestamp,
                notes: _notes
            })
        );

        emit WarehouseUpdated(_productId, _warehouseName, _location, block.timestamp);
    }

    /**
     * @dev Update logistics information for a product
     */
    function updateLogistics(
        uint256 _productId,
        string memory _logisticsName,
        string memory _location,
        string memory _notes
    ) external onlyAuthorizedLogistics productExists(_productId) {
        productJourney[_productId].push(
            SupplyChainNode({
                nodeType: "logistics",
                nodeName: _logisticsName,
                location: _location,
                timestamp: block.timestamp,
                notes: _notes
            })
        );

        emit LogisticsUpdated(_productId, _logisticsName, _location, block.timestamp);
    }

    /**
     * @dev Update distributor information for a product
     */
    function updateDistributor(
        uint256 _productId,
        string memory _distributorName,
        string memory _location,
        string memory _notes
    ) external onlyAuthorizedDistributor productExists(_productId) {
        productJourney[_productId].push(
            SupplyChainNode({
                nodeType: "distributor",
                nodeName: _distributorName,
                location: _location,
                timestamp: block.timestamp,
                notes: _notes
            })
        );

        emit DistributorUpdated(_productId, _distributorName, _location, block.timestamp);
    }

    /**
     * @dev Update retailer information for a product
     */
    function updateRetailer(
        uint256 _productId,
        string memory _retailerName,
        string memory _location,
        string memory _notes
    ) external onlyAuthorizedRetailer productExists(_productId) {
        productJourney[_productId].push(
            SupplyChainNode({
                nodeType: "retailer",
                nodeName: _retailerName,
                location: _location,
                timestamp: block.timestamp,
                notes: _notes
            })
        );

        emit RetailerUpdated(_productId, _retailerName, _location, block.timestamp);
    }

    /**
     * @dev Mark product as sold and register buyer information
     */
    function markAsSold(
        uint256 _productId,
        address _buyerAddress,
        string memory _buyerName,
        string memory _buyerEmail
    ) external onlyAuthorizedRetailer productExists(_productId) {
        require(!products[_productId].isSold, "Product already sold");

        products[_productId].isSold = true;
        products[_productId].buyerAddress = _buyerAddress;
        products[_productId].buyerName = _buyerName;
        products[_productId].buyerEmail = _buyerEmail;
        products[_productId].saleDate = block.timestamp;

        emit ProductSold(_productId, _buyerAddress, _buyerName, block.timestamp);
    }

    /**
     * @dev Get product information
     */
    function getProduct(uint256 _productId)
        external
        view
        returns (Product memory)
    {
        require(products[_productId].productId != 0, "Product does not exist");
        return products[_productId];
    }

    /**
     * @dev Get full product journey (supply chain history)
     */
    function getProductJourney(uint256 _productId)
        external
        view
        returns (SupplyChainNode[] memory)
    {
        require(products[_productId].productId != 0, "Product does not exist");
        return productJourney[_productId];
    }

    /**
     * @dev Get journey length for a product
     */
    function getJourneyLength(uint256 _productId) external view returns (uint256) {
        return productJourney[_productId].length;
    }
}

