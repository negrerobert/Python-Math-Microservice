import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Zap, 
  Clock, 
  TrendingUp, 
  Database, 
  Trash2, 
  RefreshCw,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar
} from 'recharts';
import { mathAPI } from '../services/api';

const PerformanceDashboard = ({ calculations }) => {
  const [stats, setStats] = useState(null);
  const [cacheStats, setCacheStats] = useState(null);
  const [cacheInfo, setCacheInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const [statsRes, cacheStatsRes, cacheInfoRes] = await Promise.all([
        mathAPI.getStats(),
        mathAPI.getCacheStats(),
        mathAPI.getCacheInfo(),
      ]);

      if (statsRes.success) setStats(statsRes.data);
      if (cacheStatsRes.success) setCacheStats(cacheStatsRes.data);
      if (cacheInfoRes.success) setCacheInfo(cacheInfoRes.data);

      setError(null);
    } catch (err) {
      setError('Failed to fetch performance data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
  };

  const handleClearCache = async () => {
    try {
      const result = await mathAPI.clearCache();
      if (result.success) {
        await fetchData(); // Refresh data after clearing cache
      } else {
        setError('Failed to clear cache');
      }
    } catch (err) {
      setError('Failed to clear cache');
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Update data when new calculations come in
  useEffect(() => {
    if (calculations.length > 0) {
      // Refresh data periodically when there are new calculations
      const timer = setTimeout(fetchData, 1000);
      return () => clearTimeout(timer);
    }
  }, [calculations]);

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center h-48">
          <div className="loading-spinner w-8 h-8" />
          <span className="ml-2 text-gray-600">Loading performance data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="flex items-center justify-center h-48 text-red-600">
          <AlertCircle className="w-6 h-6 mr-2" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  // Prepare chart data
  const recentCalculations = calculations.slice(-10).map((calc, index) => ({
    name: `#${index + 1}`,
    processingTime: parseFloat(calc.processingTime) || 0,
    operation: calc.operation,
    success: calc.success,
  }));

  const operationColors = {
    power: '#3b82f6',
    fibonacci: '#10b981',
    factorial: '#8b5cf6',
  };

  const pieData = stats ? stats.map(stat => ({
    name: stat.operation,
    value: stat.total_requests,
    color: operationColors[stat.operation] || '#6b7280',
  })) : [];

  const RADIAN = Math.PI / 180;
  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight="bold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="card">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-6 h-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-800">Performance Dashboard</h2>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="btn-secondary flex items-center space-x-1"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
            <button
              onClick={handleClearCache}
              className="btn-secondary flex items-center space-x-1 text-red-600 hover:bg-red-50"
            >
              <Trash2 className="w-4 h-4" />
              <span>Clear Cache</span>
            </button>
          </div>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Cache Hit Rate */}
        {cacheStats && (
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Cache Hit Rate</p>
                <p className="text-2xl font-bold text-green-600">
                  {cacheStats.cache_statistics.hit_rate_percent.toFixed(1)}%
                </p>
              </div>
              <div className="p-3 bg-green-100 rounded-full">
                <Zap className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              {cacheStats.cache_statistics.hits} hits / {cacheStats.cache_statistics.hits + cacheStats.cache_statistics.misses} total
            </div>
          </div>
        )}

        {/* Total Operations */}
        {stats && (
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Operations</p>
                <p className="text-2xl font-bold text-blue-600">
                  {stats.reduce((sum, stat) => sum + stat.total_requests, 0)}
                </p>
              </div>
              <div className="p-3 bg-blue-100 rounded-full">
                <Activity className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Across all operation types
            </div>
          </div>
        )}

        {/* Average Response Time */}
        {stats && (
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Response Time</p>
                <p className="text-2xl font-bold text-purple-600">
                  {(stats.reduce((sum, stat) => sum + stat.avg_execution_time_ms, 0) / stats.length).toFixed(2)}ms
                </p>
              </div>
              <div className="p-3 bg-purple-100 rounded-full">
                <Clock className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Execution time only
            </div>
          </div>
        )}

        {/* Cache Size */}
        {cacheStats && (
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Cache Size</p>
                <p className="text-2xl font-bold text-orange-600">
                  {cacheStats.cache_statistics.current_size}
                </p>
              </div>
              <div className="p-3 bg-orange-100 rounded-full">
                <Database className="w-6 h-6 text-orange-600" />
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              / {cacheStats.cache_statistics.max_size} max
            </div>
          </div>
        )}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Performance Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2 text-primary-600" />
            Recent Response Times
          </h3>
          {recentCalculations.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={recentCalculations}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [`${value.toFixed(2)}ms`, 'Processing Time']}
                  labelFormatter={(label) => `Request ${label}`}
                />
                <Area 
                  type="monotone" 
                  dataKey="processingTime" 
                  stroke="#3b82f6" 
                  fill="#3b82f6" 
                  fillOpacity={0.3} 
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              <p>No recent calculations to display</p>
            </div>
          )}
        </div>

        {/* Operation Distribution */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Operation Distribution
          </h3>
          {pieData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={renderCustomizedLabel}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${value} requests`, 'Total']} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500">
              <p>No operation data available</p>
            </div>
          )}
        </div>
      </div>

      {/* Operation Statistics Table */}
      {stats && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Detailed Operation Statistics
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
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.map((stat) => (
                  <tr key={stat.operation} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div 
                          className="w-3 h-3 rounded-full mr-3"
                          style={{ backgroundColor: operationColors[stat.operation] }}
                        />
                        <span className="text-sm font-medium text-gray-900 capitalize">
                          {stat.operation}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.total_requests.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`text-sm font-medium ${
                          stat.success_rate >= 95 ? 'text-green-600' : 
                          stat.success_rate >= 80 ? 'text-yellow-600' : 'text-red-600'
                        }`}>
                          {stat.success_rate.toFixed(1)}%
                        </span>
                        {stat.success_rate >= 95 ? (
                          <CheckCircle className="w-4 h-4 ml-1 text-green-600" />
                        ) : (
                          <AlertCircle className="w-4 h-4 ml-1 text-yellow-600" />
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {stat.avg_execution_time_ms.toFixed(3)}ms
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        stat.success_rate >= 95 
                          ? 'bg-green-100 text-green-800' 
                          : stat.success_rate >= 80 
                          ? 'bg-yellow-100 text-yellow-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {stat.success_rate >= 95 ? 'Excellent' : 
                         stat.success_rate >= 80 ? 'Good' : 'Needs Attention'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Cache Details */}
      {cacheInfo && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Cache Information
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-2">Cache Metrics</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Hits:</span>
                  <span className="font-medium">{cacheInfo.stats.hits}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Misses:</span>
                  <span className="font-medium">{cacheInfo.stats.misses}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Cache Sets:</span>
                  <span className="font-medium">{cacheInfo.stats.sets}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">TTL:</span>
                  <span className="font-medium">{cacheInfo.stats.ttl_seconds}s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Uptime:</span>
                  <span className="font-medium">{cacheInfo.stats.uptime_seconds.toFixed(1)}s</span>
                </div>
              </div>
            </div>
            
            {cacheInfo.sample_keys && cacheInfo.sample_keys.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-2">Sample Cache Keys</h4>
                <div className="space-y-2">
                  {cacheInfo.sample_keys.slice(0, 5).map((key, index) => (
                    <div key={index} className="text-xs bg-gray-50 p-2 rounded">
                      <div className="font-mono text-gray-600">Key: {key.key}</div>
                      <div className="text-gray-500 mt-1">Value: {key.value}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default PerformanceDashboard;