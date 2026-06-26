// src/components/TokenVerifier.jsx
// Componente para verificar tokens URT

import React, { useState } from 'react';
import api from '../services/api';

const TokenVerifier = () => {
  const [rid, setRid] = useState('');
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(null);
  const [verification, setVerification] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setToken(null);
    setVerification(null);

    try {
      const tokenData = await api.getToken(rid);
      setToken(tokenData);

      // Verificar token
      const verificationData = await api.verifyToken(rid);
      setVerification(verificationData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Verificar Token URT</h2>

      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={rid}
            onChange={(e) => setRid(e.target.value)}
            placeholder="Ingresa RID (ej: RID-A7CCC968)"
            className="flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Buscando...' : 'Buscar'}
          </button>
        </div>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {token && (
        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-bold text-lg mb-2">Información del Token</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <strong>RID:</strong>
                <p className="text-gray-700">{token.rid.id}</p>
              </div>
              <div>
                <strong>Tipo:</strong>
                <p className="text-gray-700">{token.rid.type}</p>
              </div>
              <div>
                <strong>Propietario:</strong>
                <p className="text-gray-700">{token.metadata.owner}</p>
              </div>
              <div>
                <strong>Creado:</strong>
                <p className="text-gray-700">{new Date(token.metadata.created_at).toLocaleDateString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="font-bold text-lg mb-2">Resultado de Verificación</h3>
            {verification && verification.verified && (
              <div className="text-green-700">
                <p className="font-bold">✓ Token Verificado</p>
                <ul className="mt-2 text-sm space-y-1">
                  {Object.entries(verification.checks).map(([check, value]) => (
                    <li key={check}>
                      {value ? '✓' : '✗'} {check.replace(/_/g, ' ').toUpperCase()}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {token.blockchain && token.blockchain.network !== 'None' && (
            <div className="bg-purple-50 p-4 rounded-lg">
              <h3 className="font-bold text-lg mb-2">Anclaje Blockchain</h3>
              <div className="text-sm space-y-1">
                <p><strong>Red:</strong> {token.blockchain.network}</p>
                <p><strong>TX Hash:</strong> {token.blockchain.transaction_hash?.substring(0, 20)}...</p>
                <p><strong>Confirmaciones:</strong> {token.blockchain.confirmation_count}</p>
              </div>
            </div>
          )}

          <div className="bg-gray-100 p-4 rounded-lg">
            <details>
              <summary className="font-bold cursor-pointer">Ver JSON Completo</summary>
              <pre className="mt-2 text-xs overflow-auto bg-white p-2 rounded">
                {JSON.stringify(token, null, 2)}
              </pre>
            </details>
          </div>
        </div>
      )}
    </div>
  );
};

export default TokenVerifier;
