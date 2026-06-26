// src/App.jsx
// Aplicación principal React

import React, { useState, useEffect } from 'react';
import TokenCreator from './components/TokenCreator';
import TokenVerifier from './components/TokenVerifier';
import api from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('create');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await api.getStats();
        setStats(data);
      } catch (error) {
        console.error('Error loading stats:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
    // Actualizar cada 30 segundos
    const interval = setInterval(loadStats, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-blue-600">🔐 Fuente Protocol</h1>
              <p className="text-gray-600">Universal Resource Token (URT)</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">API Status: <span className="text-green-600 font-bold">✓ Connected</span></p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-gray-600 text-sm font-medium">Total Tokens</h3>
              <p className="text-3xl font-bold text-blue-600">{stats.total_tokens}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-gray-600 text-sm font-medium">Tokens Anclados</h3>
              <p className="text-3xl font-bold text-green-600">{stats.anchored_tokens}</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-gray-600 text-sm font-medium">Tipos de Recursos</h3>
              <p className="text-3xl font-bold text-purple-600">
                {stats.resource_types ? Object.keys(stats.resource_types).length : 0}
              </p>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('create')}
              className={`flex-1 py-4 px-6 font-medium ${
                activeTab === 'create'
                  ? 'bg-blue-50 border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              📝 Crear Token
            </button>
            <button
              onClick={() => setActiveTab('verify')}
              className={`flex-1 py-4 px-6 font-medium ${
                activeTab === 'verify'
                  ? 'bg-blue-50 border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              ✓ Verificar Token
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'create' && <TokenCreator />}
            {activeTab === 'verify' && <TokenVerifier />}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-12">
        <div className="max-w-6xl mx-auto px-6 py-6 text-center text-sm">
          <p>&copy; 2026 Fuente Protocol. Todos los derechos reservados.</p>
          <p className="mt-2 text-gray-400">
            <a href="https://github.com/akiles1993/Fuente" className="hover:text-white">
              GitHub
            </a>
            {' '} • {' '}
            <a href="https://fuente.io" className="hover:text-white">
              Sitio Web
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
