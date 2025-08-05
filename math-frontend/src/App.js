import React, { useState, useEffect } from 'react';
import { 
  Calculator, 
  Activity, 
  Database, 
  History,
  Zap,
  Hash,
  RefreshCw,
  Trash2
} from 'lucide-react';

// API Service - matches your existing api.js structure
const API_BASE_URL = '/api/v1/math';

const mathAPI = {
  async calculatePower(base, exponent) {
    try {
      const response = await fetch(`${API_BASE_URL}/power`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ base, exponent })
      });
      
      const data = await response.json();
      const processingTime = response.headers.get('x-processing-time-ms');
      const requestId = response.headers.get('x-request-id');
      
      if (response.ok) {
        return { success: true, data, processingTime, requestId };
      } else {
        return { 
          success: false, 
          error: data.error || 'Request failed', 
          details: data.details,
          errorType: data.error_type,
          status: response.status,
          requestId 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        error: 'Network error - could not connect to the server',
        status: 0 
      };
    }
  },

  async calculateFibonacci(n) {
    try {
      const response = await fetch(`${API_BASE_URL}/fibonacci`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n })
      });
      
      const data = await response.json();
      const processingTime = response.headers.get('x-processing-time-ms');
      const requestId = response.headers.get('x-request-id');
      
      if (response.ok) {
        return { success: true, data, processingTime, requestId };
      } else {
        return { 
          success: false, 
          error: data.error || 'Request failed', 
          details: data.details,
          errorType: data.error_type,
          status: response.status,
          requestId 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        error: 'Network error - could not connect to the server',
        status: 0 
      };
    }
  },

  async calculateFactorial(n) {
    try {
      const response = await fetch(`${API_BASE_URL}/factorial`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ n })
      });
      
      const data = await response.json();
      const processingTime = response.headers.get('x-processing-time-ms');
      const requestId = response.headers.get('x-request-id');
      
      if (response.ok) {
        return { success: true, data, processingTime, requestId };
      } else {
        return { 
          success: false, 
          error: data.error || 'Request failed', 
          details: data.details,
          errorType: data.error_type,
          status: response.status,
          requestId 
        };
      }
    } catch (error) {
      return { 
        success: false, 
        error: 'Network error - could not connect to the server',
        status: 0 
      };
    }
  },

  async getStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`);
      const data = await response.json();
      return response.ok ? { success: true, data } : { success: false, error: data.error };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  },

  async getCacheStats() {
    try {
      const response = await fetch(`${API_BASE_URL}/cache/stats`);
      const data = await response.json();
      return response.ok ? { success: true, data } : { success: false, error: data.error };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  },

  async clearCache() {
    try {
      const response = await fetch(`${API_BASE_URL}/cache/clear`, { method: 'POST' });
      const data = await response.json();
      return response.ok ? { success: true, data } : { success: false, error: data.error };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  },

  async getHistory(page = 1, pageSize = 20) {
    try {
      const response = await fetch(`${API_BASE_URL}/history?page=${page}&page_size=${pageSize}`);
      const data = await response.json();
      return response.ok ? { success: true, data } : { success: false, error: data.error };
    } catch (error) {
      return { success: false, error: 'Network error' };
    }
  }
};

const MathCalculator = ({ onCalculationComplete }) => {
  const [activeTab, setActiveTab] = useState('power');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Form states
  const [powerForm, setPowerForm] = useState({ base: '', exponent: '' });
  const [fibonacciForm, setFibonacciForm] = useState({ n: '' });
  const [factorialForm, setFactorialForm] = useState({ n: '' });

  const tabs = [
    { id: 'power', name: 'Power', icon: Zap, color: 'text-blue-600' },
    { id: 'fibonacci', name: 'Fibonacci', icon: Hash, color: 'text-green-600' },
    { id: 'factorial', name: 'Factorial', icon: '!', color: 'text-purple-600' },
  ];

  const resetState = () => {
    setResult(null);
    setError(null);
  };

  const handleCalculation = async (operation) => {
    resetState();
    setLoading(true);

    let values, apiCall;

    try {
      switch (operation) {
        case 'power':
          values = { base: Number(powerForm.base), exponent: Number(powerForm.exponent) };
          apiCall = () => mathAPI.calculatePower(values.base, values.exponent);
          break;
        case 'fibonacci':
          values = { n: Number(fibonacciForm.n) };
          apiCall = () => mathAPI.calculateFibonacci(values.n);
          break;
        case 'factorial':
          values = { n: Number(factorialForm.n) };
          apiCall = () => mathAPI.calculateFactorial(values.n);
          break;
        default:
          throw new Error('Unknown operation');
      }

      const response = await apiCall();

      if (response.success) {
        setResult({
          ...response.data,
          processingTime: response.processingTime,
          requestId: response.requestId,
        });

        if (onCalculationComplete) {
          onCalculationComplete({
            operation,
            success: true,
            result: response.data.result,
            processingTime: response.processingTime,
          });
        }
      } else {
        setError({
          message: response.error,
          details: response.details,
          errorType: response.errorType,
          status: response.status,
          requestId: response.requestId,
        });

        if (onCalculationComplete) {
          onCalculationComplete({
            operation,
            success: false,
            error: response.error,
          });
        }
      }
    } catch (err) {
      setError({
        message: err.message || 'An unexpected error occurred',
        details: null,
      });
    } finally {
      setLoading(false);
    }
  };

  const formatResult = (result) => {
    if (typeof result === 'number') {
      if (Math.abs(result) >= 1e10) {
        return result.toExponential(6);
      }
      return result.toLocaleString();
    }
    return String(result);
  };

  const renderPowerForm = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Base</label>
          <input
            type="number"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            value={powerForm.base}
            onChange={(e) => setPowerForm({ ...powerForm, base: e.target.value })}
            placeholder="e.g., 2"
            disabled={loading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Exponent</label>
          <input
            type="number"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            value={powerForm.exponent}
            onChange={(e) => setPowerForm({ ...powerForm, exponent: e.target.value })}
            placeholder="e.g., 10"
            disabled={loading}
          />
        </div>
      </div>
      <button
        onClick={() => handleCalculation('power')}
        disabled={loading || !powerForm.base || !powerForm.exponent}
        className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {loading ? (
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
        ) : (
          <Zap className="w-4 h-4" />
        )}
        <span>Calculate {powerForm.base}^{powerForm.exponent}</span>
      </button>
    </div>
  );

  const renderFibonacciForm = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Position (n)</label>
        <input
          type="number"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
          value={fibonacciForm.n}
          onChange={(e) => setFibonacciForm({ n: e.target.value })}
          placeholder="e.g., 10"
          min="0"
          disabled={loading}
        />
        <p className="text-xs text-gray-500 mt-1">Find the nth number in the Fibonacci sequence</p>
      </div>
      <button
        onClick={() => handleCalculation('fibonacci')}
        disabled={loading || !fibonacciForm.n}
        className="w-full bg-green-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {loading ? (
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
        ) : (
          <Hash className="w-4 h-4" />
        )}
        <span>Calculate F({fibonacciForm.n})</span>
      </button>
    </div>
  );

  const renderFactorialForm = () => (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Number (n)</label>
        <input
          type="number"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
          value={factorialForm.n}
          onChange={(e) => setFactorialForm({ n: e.target.value })}
          placeholder="e.g., 5"
          min="0"
          disabled={loading}
        />
        <p className="text-xs text-gray-500 mt-1">Calculate n! = n × (n-1) × ... × 1</p>
      </div>
      <button
        onClick={() => handleCalculation('factorial')}
        disabled={loading || !factorialForm.n}
        className="w-full bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {loading ? (
          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
        ) : (
          <span className="text-lg">!</span>
        )}
        <span>Calculate {factorialForm.n}!</span>
      </button>
    </div>
  );

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
      <div className="flex items-center space-x-2 mb-6">
        <Calculator className="w-6 h-6 text-blue-600" />
        <h2 className="text-xl font-semibold text-gray-800">Calculator</h2>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
        {tabs.map((tab) => {
          const Icon = tab.icon === '!' ? 'span' : tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => {
                setActiveTab(tab.id);
                resetState();
              }}
              className={`flex-1 flex items-center justify-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                activeTab === tab.id
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              {Icon === 'span' ? (
                <span className={`text-lg font-bold ${activeTab === tab.id ? tab.color : ''}`}>!</span>
              ) : (
                <Icon className={`w-4 h-4 ${activeTab === tab.id ? tab.color : ''}`} />
              )}
              <span>{tab.name}</span>
            </button>
          );
        })}
      </div>

      {/* Form Content */}
      <div className="mb-6">
        {activeTab === 'power' && renderPowerForm()}
        {activeTab === 'fibonacci' && renderFibonacciForm()}
        {activeTab === 'factorial' && renderFactorialForm()}
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-start space-x-2">
            <div className="flex-shrink-0 w-2 h-2 bg-red-400 rounded-full mt-2" />
            <div className="flex-1">
              <h4 className="text-sm font-medium text-red-800">Error</h4>
              <p className="text-sm text-red-700 mt-1">{error.message}</p>
              {error.details && Array.isArray(error.details) && (
                <ul className="mt-2 text-xs text-red-600 space-y-1">
                  {error.details.map((detail, index) => (
                    <li key={index} className="flex items-center space-x-1">
                      <span>•</span>
                      <span>{typeof detail === 'string' ? detail : detail.message}</span>
                    </li>
                  ))}
                </ul>
              )}
              {error.errorType && (
                <p className="text-xs text-red-500 mt-2">
                  Type: {error.errorType}
                  {error.requestId && ` | Request ID: ${error.requestId}`}
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-medium text-green-800">Result</h4>
            {result.processingTime && (
              <span className="text-xs text-green-600">
                {parseFloat(result.processingTime).toFixed(2)}ms
              </span>
            )}
          </div>
          <div className="text-2xl font-mono font-bold text-green-900 break-all">
            {formatResult(result.result)}
          </div>
          <div className="flex items-center justify-between mt-2 text-xs text-green-600">
            <span>Operation: {result.operation}</span>
            {result.requestId && (
              <span>ID: {result.requestId}</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const StatusCard = ({ title, value, icon: Icon, color, subtitle, loading = false }) => (
  <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        {loading ? (
          <div className="animate-spin rounded-full h-6 w-6 border-2 border-gray-200 border-t-blue-600 mt-2" />
        ) : (
          <p className={`text-2xl font-bold ${color}`}>{value}</p>
        )}
        {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
      </div>
      <div className={`p-3 rounded-full ${color.replace('text-', 'bg-').replace('-600', '-100')}`}>
        <Icon className={`w-6 h-6 ${color}`} />
      </div>
    </div>
  </div>
);

const RecentCalculations = ({ calculations }) => (
  <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
    <div className="flex items-center space-x-2 mb-4">
      <History className="w-5 h-5 text-gray-600" />
      <h3 className="text-lg font-semibold text-gray-800">Recent Calculations</h3>
    </div>
    
    {calculations.length === 0 ? (
      <div className="text-center py-8 text-gray-500">
        <Calculator className="w-12 h-12 mx-auto mb-3 opacity-30" />
        <p>No calculations yet</p>
        <p className="text-sm">Start by performing some calculations above</p>
      </div>
    ) : (
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {calculations.slice(-10).reverse().map((calc, index) => (
          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className={`w-2 h-2 rounded-full ${calc.success ? 'bg-green-400' : 'bg-red-400'}`} />
              <div>
                <p className="font-medium text-gray-900 capitalize">{calc.operation}</p>
                <p className="text-sm text-gray-600">
                  Result: {typeof calc.result === 'number' ? calc.result.toLocaleString() : 'Error'}
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium text-gray-700">{calc.processingTime}ms</p>
              <p className="text-xs text-gray-500">{calc.success ? 'Success' : 'Failed'}</p>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

const PerformanceDashboard = ({ calculations, onRefresh }) => {
  const [stats, setStats] = useState(null);
  const [cacheStats, setCacheStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const [statsRes, cacheStatsRes] = await Promise.all([
        mathAPI.getStats(),
        mathAPI.getCacheStats(),
      ]);

      if (statsRes.success) setStats(statsRes.data);
      if (cacheStatsRes.success) setCacheStats(cacheStatsRes.data);
    } catch (err) {
      console.error('Failed to fetch performance data:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    if (onRefresh) onRefresh();
  };

  const handleClearCache = async () => {
    try {
      const result = await mathAPI.clearCache();
      if (result.success) {
        await fetchData();
      }
    } catch (err) {
      console.error('Failed to clear cache:', err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (calculations.length > 0) {
      const timer = setTimeout(fetchData, 1000);
      return () => clearTimeout(timer);
    }
  }, [calculations]);

  const totalCalculations = calculations.length;
  const successfulCalculations = calculations.filter(c => c.success).length;
  const averageTime = calculations.length > 0 
    ? (calculations.reduce((sum, c) => sum + parseFloat(c.processingTime || 0), 0) / calculations.length).toFixed(2)
    : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-6 h-6 text-blue-600" />
            <h2 className="text-xl font-semibold text-gray-800">Performance Dashboard</h2>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-300 transition-colors duration-200 flex items-center space-x-1"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
            <button
              onClick={handleClearCache}
              className="bg-gray-200 text-red-600 px-4 py-2 rounded-lg font-medium hover:bg-red-50 transition-colors duration-200 flex items-center space-x-1"
            >
              <Trash2 className="w-4 h-4" />
              <span>Clear Cache</span>
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatusCard
          title="Cache Hit Rate"
          value={cacheStats ? `${cacheStats.cache_statistics.hit_rate_percent.toFixed(1)}%` : '0%'}
          icon={Zap}
          color="text-green-600"
          subtitle={cacheStats ? `${cacheStats.cache_statistics.hits} hits` : 'Loading...'}
          loading={loading}
        />
        <StatusCard
          title="Total Operations"
          value={stats ? stats.reduce((sum, stat) => sum + stat.total_requests, 0) : totalCalculations}
          icon={Activity}
          color="text-blue-600"
          subtitle="All operations"
          loading={loading && totalCalculations === 0}
        />
        <StatusCard
          title="Avg Response Time"
          value={`${averageTime}ms`}
          icon={Activity}
          color="text-purple-600"
          subtitle="Processing time"
        />
        <StatusCard
          title="Cache Size"
          value={cacheStats ? cacheStats.cache_statistics.current_size : '0'}
          icon={Database}
          color="text-orange-600"
          subtitle={cacheStats ? `/ ${cacheStats.cache_statistics.max_size} max` : 'Loading...'}
          loading={loading}
        />
      </div>

      {/* Operation Statistics Table */}
      {stats && (
        <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Operation Statistics
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Operation
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total Requests
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Success Rate
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Time
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.map((stat) => (
                  <tr key={stat.operation} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm font-medium text-gray-900 capitalize">
                        {stat.operation}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.total_requests.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`text-sm font-medium ${
                        stat.success_rate >= 95 ? 'text-green-600' : 
                        stat.success_rate >= 80 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {stat.success_rate.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.avg_execution_time_ms.toFixed(3)}ms
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

function App() {
  const [calculations, setCalculations] = useState([]);
  const [activeTab, setActiveTab] = useState('calculator');

  const handleCalculationComplete = (calculationData) => {
    setCalculations(prev => [...prev, {
      ...calculationData,
      timestamp: new Date().toISOString()
    }]);
  };

  const tabs = [
    { id: 'calculator', name: 'Calculator', icon: Calculator },
    { id: 'dashboard', name: 'Dashboard', icon: Activity }
  ];

  const totalCalculations = calculations.length;
  const successfulCalculations = calculations.filter(c => c.success).length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Calculator className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Math Microservice</h1>
                <p className="text-sm text-gray-600">Mathematical operations API</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{totalCalculations} Operations</p>
                <p className="text-xs text-gray-600">
                  {successfulCalculations}/{totalCalculations} successful
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.name}</span>
                </button>
              );
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'calculator' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <MathCalculator onCalculationComplete={handleCalculationComplete} />
            </div>
            <div className="space-y-6">
              <RecentCalculations calculations={calculations} />
            </div>
          </div>
        )}

        {activeTab === 'dashboard' && (
          <PerformanceDashboard 
            calculations={calculations} 
            onRefresh={() => console.log('Dashboard refreshed')} 
          />
        )}

        
      </main>
    </div>
  );
}

export default App;