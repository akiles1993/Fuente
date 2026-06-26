// src/services/web3.js
// Integración Web3 para Fuente Protocol

import { ethers } from 'ethers';

const URT_TOKEN_ABI = [
  {
    constant: false,
    inputs: [{ name: 'to', type: 'address' }, { name: 'amount', type: 'uint256' }],
    name: 'transfer',
    outputs: [{ name: '', type: 'bool' }],
    payable: false,
    stateMutability: 'nonpayable',
    type: 'function'
  },
  {
    constant: true,
    inputs: [{ name: 'account', type: 'address' }],
    name: 'balanceOf',
    outputs: [{ name: '', type: 'uint256' }],
    payable: false,
    stateMutability: 'view',
    type: 'function'
  },
  {
    constant: false,
    inputs: [
      { name: 'rid', type: 'string' },
      { name: 'urn', type: 'string' },
      { name: 'contentHash', type: 'bytes32' }
    ],
    name: 'issueURToken',
    outputs: [{ name: '', type: 'bytes32' }],
    payable: false,
    stateMutability: 'nonpayable',
    type: 'function'
  },
  {
    constant: false,
    inputs: [{ name: 'tokenId', type: 'bytes32' }],
    name: 'verifyURToken',
    outputs: [],
    payable: false,
    stateMutability: 'nonpayable',
    type: 'function'
  }
];

class Web3Service {
  constructor() {
    this.provider = null;
    this.signer = null;
    this.contract = null;
  }

  async connect() {
    if (window.ethereum) {
      try {
        // Solicitar conexión
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        
        this.provider = new ethers.BrowserProvider(window.ethereum);
        this.signer = await this.provider.getSigner();
        
        return {
          connected: true,
          address: await this.signer.getAddress(),
          chainId: (await this.provider.getNetwork()).chainId
        };
      } catch (error) {
        console.error('Conexión rechazada:', error);
        return { connected: false, error: error.message };
      }
    } else {
      return { 
        connected: false, 
        error: 'MetaMask no instalado' 
      };
    }
  }

  async getBalance(address) {
    if (!this.provider) throw new Error('Provider no conectado');
    return this.provider.getBalance(address);
  }

  async issueURToken(contractAddress, rid, urn, contentHash) {
    if (!this.signer) throw new Error('Signer no disponible');

    this.contract = new ethers.Contract(
      contractAddress,
      URT_TOKEN_ABI,
      this.signer
    );

    try {
      const tx = await this.contract.issueURToken(rid, urn, contentHash);
      const receipt = await tx.wait();
      return receipt;
    } catch (error) {
      console.error('Error en issueURToken:', error);
      throw error;
    }
  }

  async verifyURToken(contractAddress, tokenId) {
    if (!this.signer) throw new Error('Signer no disponible');

    this.contract = new ethers.Contract(
      contractAddress,
      URT_TOKEN_ABI,
      this.signer
    );

    try {
      const tx = await this.contract.verifyURToken(tokenId);
      const receipt = await tx.wait();
      return receipt;
    } catch (error) {
      console.error('Error en verifyURToken:', error);
      throw error;
    }
  }

  async getURTokenInfo(contractAddress, tokenId) {
    if (!this.provider) throw new Error('Provider no conectado');

    this.contract = new ethers.Contract(
      contractAddress,
      URT_TOKEN_ABI,
      this.provider
    );

    try {
      const tokenInfo = await this.contract.getURToken(tokenId);
      return tokenInfo;
    } catch (error) {
      console.error('Error obteniendo info de token:', error);
      throw error;
    }
  }
}

export default new Web3Service();
