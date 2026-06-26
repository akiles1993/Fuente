// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title URT Token (Universal Resource Token)
 * @dev Implementación de token ERC-20 basado en URT Protocol
 * @author Fuente Protocol Contributors
 */

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract URTToken is IERC20 {
    string public name = "Universal Resource Token";
    string public symbol = "URT";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    address public owner;
    bool public paused;
    
    // Estructura para registrar tokens URT
    struct ResourceToken {
        string rid;              // RID-XXXXXXXX
        string urn;             // urn:resource:namespace:RID
        bytes32 contentHash;    // SHA-256 del contenido
        uint256 createdAt;
        address issuer;
        bool isVerified;
    }
    
    mapping(bytes32 => ResourceToken) public registeredTokens;
    bytes32[] public tokenRegistry;
    
    event TokenIssued(
        bytes32 indexed tokenId,
        string rid,
        string urn,
        address indexed issuer,
        uint256 timestamp
    );
    
    event TokenVerified(
        bytes32 indexed tokenId,
        address indexed verifier,
        uint256 timestamp
    );
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner");
        _;
    }
    
    modifier whenNotPaused() {
        require(!paused, "Token paused");
        _;
    }
    
    constructor(uint256 initialSupply) {
        owner = msg.sender;
        totalSupply = initialSupply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }
    
    // ===== ERC-20 Functions =====
    
    function transfer(address recipient, uint256 amount) 
        public 
        whenNotPaused 
        returns (bool) 
    {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }
    
    function approve(address spender, uint256 amount) 
        public 
        returns (bool) 
    {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }
    
    function transferFrom(address sender, address recipient, uint256 amount) 
        public 
        whenNotPaused 
        returns (bool) 
    {
        require(balanceOf[sender] >= amount, "Insufficient balance");
        require(allowance[sender][msg.sender] >= amount, "Allowance exceeded");
        
        balanceOf[sender] -= amount;
        balanceOf[recipient] += amount;
        allowance[sender][msg.sender] -= amount;
        
        emit Transfer(sender, recipient, amount);
        return true;
    }
    
    // ===== URT Protocol Functions =====
    
    /**
     * @dev Emite un nuevo token URT vinculado a un recurso
     * @param rid Resource ID (RID-XXXXXXXX)
     * @param urn Referencia global (urn:resource:...)
     * @param contentHash Hash SHA-256 del contenido
     */
    function issueURToken(
        string memory rid,
        string memory urn,
        bytes32 contentHash
    ) public returns (bytes32) {
        bytes32 tokenId = keccak256(abi.encodePacked(rid, block.timestamp));
        
        registeredTokens[tokenId] = ResourceToken({
            rid: rid,
            urn: urn,
            contentHash: contentHash,
            createdAt: block.timestamp,
            issuer: msg.sender,
            isVerified: false
        });
        
        tokenRegistry.push(tokenId);
        
        emit TokenIssued(tokenId, rid, urn, msg.sender, block.timestamp);
        
        // Acuñar tokens ERC-20 de recompensa
        uint256 rewardAmount = 10 * 10 ** uint256(decimals);
        balanceOf[msg.sender] += rewardAmount;
        totalSupply += rewardAmount;
        
        return tokenId;
    }
    
    /**
     * @dev Verifica un token URT registrado
     * @param tokenId ID del token
     */
    function verifyURToken(bytes32 tokenId) public onlyOwner {
        require(registeredTokens[tokenId].createdAt != 0, "Token not found");
        registeredTokens[tokenId].isVerified = true;
        
        emit TokenVerified(tokenId, msg.sender, block.timestamp);
    }
    
    /**
     * @dev Obtiene información de un token registrado
     */
    function getURToken(bytes32 tokenId) 
        public 
        view 
        returns (ResourceToken memory) 
    {
        return registeredTokens[tokenId];
    }
    
    /**
     * @dev Obtiene el total de tokens registrados
     */
    function getTokenCount() public view returns (uint256) {
        return tokenRegistry.length;
    }
    
    /**
     * @dev Obtiene un token ID por índice
     */
    function getTokenByIndex(uint256 index) public view returns (bytes32) {
        require(index < tokenRegistry.length, "Index out of bounds");
        return tokenRegistry[index];
    }
    
    // ===== Admin Functions =====
    
    function pauseToken() public onlyOwner {
        paused = true;
    }
    
    function unpauseToken() public onlyOwner {
        paused = false;
    }
    
    function mint(address to, uint256 amount) public onlyOwner {
        balanceOf[to] += amount;
        totalSupply += amount;
        emit Transfer(address(0), to, amount);
    }
    
    function burn(uint256 amount) public {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Transfer(msg.sender, address(0), amount);
    }
}

/**
 * @title URTFactory
 * @dev Factoría para crear instancias de URT Tokens
 */
contract URTFactory {
    URTToken[] public createdTokens;
    address[] public creators;
    
    event URTTokenCreated(address indexed token, address indexed creator);
    
    function createURTToken(uint256 initialSupply) public returns (address) {
        URTToken newToken = new URTToken(initialSupply);
        createdTokens.push(newToken);
        creators.push(msg.sender);
        
        emit URTTokenCreated(address(newToken), msg.sender);
        return address(newToken);
    }
    
    function getTokenCount() public view returns (uint256) {
        return createdTokens.length;
    }
    
    function getToken(uint256 index) public view returns (address) {
        return address(createdTokens[index]);
    }
}
