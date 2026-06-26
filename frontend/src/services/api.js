// src/services/api.js
// Cliente API REST para Fuente Protocol

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

class FuenteAPI {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  // Health check
  async healthCheck() {
    const response = await fetch(`${this.baseURL}/health`);
    return response.json();
  }

  // Create Token
  async createToken({
    data,
    name,
    resource_type,
    namespace = 'fuente',
    owner,
    description,
    tags = [],
    expiration_days
  }) {
    const response = await fetch(`${this.baseURL}/tokens`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        data,
        name,
        resource_type,
        namespace,
        owner,
        description,
        tags,
        expiration_days
      })
    });

    if (!response.ok) {
      throw new Error(`Error creating token: ${response.statusText}`);
    }

    return response.json();
  }

  // Get Token
  async getToken(rid) {
    const response = await fetch(`${this.baseURL}/tokens/${rid}`);
    
    if (!response.ok) {
      throw new Error(`Token not found: ${rid}`);
    }

    return response.json();
  }

  // List Tokens
  async listTokens(skip = 0, limit = 100) {
    const response = await fetch(
      `${this.baseURL}/tokens?skip=${skip}&limit=${limit}`
    );
    return response.json();
  }

  // Verify Token
  async verifyToken(rid) {
    const response = await fetch(`${this.baseURL}/tokens/${rid}/verify`, {
      method: 'POST'
    });
    return response.json();
  }

  // Anchor to Blockchain
  async anchorToBlockchain(rid, {
    network,
    transaction_hash,
    block_number
  }) {
    const response = await fetch(`${this.baseURL}/tokens/${rid}/anchor`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        network,
        transaction_hash,
        block_number
      })
    });
    return response.json();
  }

  // Search Tokens
  async searchTokens(q = '', tags = []) {
    const params = new URLSearchParams();
    if (q) params.append('q', q);
    tags.forEach(tag => params.append('tags', tag));
    
    const response = await fetch(`${this.baseURL}/search?${params}`);
    return response.json();
  }

  // Get Stats
  async getStats() {
    const response = await fetch(`${this.baseURL}/stats`);
    return response.json();
  }
}

export default new FuenteAPI();
