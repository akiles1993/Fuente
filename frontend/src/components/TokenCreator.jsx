// src/components/TokenCreator.jsx
// Componente para crear tokens URT

import React, { useState } from 'react';
import api from '../services/api';

const TokenCreator = () => {
  const [formData, setFormData] = useState({
    name: '',
    resourceType: 'certificate',
    owner: '',
    description: '',
    tags: '',
    expirationDays: 365,
    file: null
  });

  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    setFormData(prev => ({
      ...prev,
      file: e.target.files[0]
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Leer archivo
      const fileReader = new FileReader();
      fileReader.onload = async () => {
        const base64 = fileReader.result.split(',')[1];

        const newToken = await api.createToken({
          data: base64,
          name: formData.name,
          resource_type: formData.resourceType,
          owner: formData.owner,
          description: formData.description,
          tags: formData.tags.split(',').map(t => t.trim()),
          expiration_days: parseInt(formData.expirationDays)
        });

        setToken(newToken);
        setFormData({
          name: '',
          resourceType: 'certificate',
          owner: '',
          description: '',
          tags: '',
          expirationDays: 365,
          file: null
        });
      };
      fileReader.readAsDataURL(formData.file);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Crear Token URT</h2>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {token ? (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
          <h3 className="font-bold mb-2">Token Creado!</h3>
          <p><strong>RID:</strong> {token.rid.id}</p>
          <p><strong>URN:</strong> {token.urn.value}</p>
          <p><strong>Hash:</strong> {token.hash.value.substring(0, 32)}...</p>
          <div className="mt-4">
            <pre className="bg-gray-100 p-2 rounded text-sm overflow-auto">
              {JSON.stringify(token, null, 2)}
            </pre>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Nombre</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Tipo de Recurso</label>
            <select
              name="resourceType"
              value={formData.resourceType}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring"
            >
              <option value="document">Documento</option>
              <option value="certificate">Certificado</option>
              <option value="credential">Credencial</option>
              <option value="nft">NFT</option>
              <option value="digital_asset">Activo Digital</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Propietario (Email)</label>
            <input
              type="email"
              name="owner"
              value={formData.owner}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Descripción</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring"
              rows="3"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Etiquetas (separadas por comas)</label>
            <input
              type="text"
              name="tags"
              value={formData.tags}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring"
              placeholder="educacion, certificado, blockchain"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Archivo</label>
            <input
              type="file"
              name="file"
              onChange={handleFileChange}
              className="w-full"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Expiración (días)</label>
            <input
              type="number"
              name="expirationDays"
              value={formData.expirationDays}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Creando...' : 'Crear Token'}
          </button>
        </form>
      )}
    </div>
  );
};

export default TokenCreator;
