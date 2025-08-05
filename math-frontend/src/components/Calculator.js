import React, { useState } from 'react';
import { Calculator as CalculatorIcon, Zap, Hash, Factorial } from 'lucide-react';
import { mathAPI } from '../services/api';

const Calculator = ({ onCalculationComplete }) => {
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
    { id: 'factorial', name: 'Factorial', icon: Factorial, color: 'text-purple-600' },
  ];

  const resetState = () => {
    setResult(null);
    setError(null);
  };

  const validateInput = (operation, values) => {
    const errors = [];

    switch (operation) {
      case 'power':
        if (!values.base || isNaN(values.base)) {
          errors.push('Base must be a valid number');
        }
        if (!values.exponent || isNaN(values.exponent)) {
          errors.push('Exponent must be a valid number');
        }
        if (Math.abs(values.base) > 1000) {
          errors.push('Base should be between -1000 and 1000 for performance');
        }
        if (Math.abs(values.exponent) > 1000) {
          errors.push('Exponent should be between -1000 and 1000 for performance');
        }
        break;

      case 'fibonacci':
        if (!values.n || isNaN(values.n) || !Number.isInteger(Number(values.n))) {
          errors.push('N must be a valid integer');
        }
        if (Number(values.n) < 0) {
          errors.push('N must be non-negative');
        }
        if (Number(values.n) > 1000) {
          errors.push('N should be ≤ 1000 for performance reasons');
        }
        break;

      case 'factorial':
        if (!values.n || isNaN(values.n) || !Number.isInteger(Number(values.n))) {
          errors.push('N must be a valid integer');
        }
        if (Number(values.n) < 0) {
          errors.push('N must be non-negative');
        }
        if (Number(values.n) > 170) {
          errors.push('N should be ≤ 170 to prevent overflow');
        }
        break;

      default:
        errors.push('Unknown operation');
    }

    return errors;
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

      // Validate input
      const validationErrors = validateInput(operation, values);
      if (validationErrors.length > 0) {
        setError({
          message: 'Input validation failed',
          details: validationErrors,
        });
        setLoading(false);
        return;
      }

      // Make API call
      const response = await apiCall();

      if (response.success) {
        setResult({
          ...response.data,
          processingTime: response.processingTime,
          requestId: response.requestId,
        });

        // Notify parent component
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

        // Notify parent component
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
      // Format large numbers with scientific notation
      if (Math.abs(result) >= 1e10) {
        return result.toExponential(6);
      }
      // Format normal numbers with commas
      return result.toLocaleString();
    }
    return String(result);
  };

  const renderPowerForm = () => (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Base
          </label>
          <input
            type="number"
            className="input-field"
            value={powerForm.base}
            onChange={(e) => setPowerForm({ ...powerForm, base: e.target.value })}
            placeholder="e.g., 2"
            disabled={loading}
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Exponent
          </label>
          <input
            type="number"
            className="input-field"
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
        className="btn-primary w-full flex items-center justify-center space-x-2"
      >
        {loading ? (
          <div className="loading-spinner w-4 h-4" />
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
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Position (n)
        </label>
        <input
          type="number"
          className="input-field"
          value={fibonacciForm.n}
          onChange={(e) => setFibonacciForm({ n: e.target.value })}
          placeholder="e.g., 10"
          min="0"
          disabled={loading}
        />
        <p className="text-xs text-gray-500 mt-1">
          Find the nth number in the Fibonacci sequence
        </p>
      </div>
      <button
        onClick={() => handleCalculation('fibonacci')}
        disabled={loading || !fibonacciForm.n}
        className="btn-primary w-full flex items-center justify-center space-x-2"
      >
        {loading ? (
          <div className="loading-spinner w-4 h-4" />
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
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Number (n)
        </label>
        <input
          type="number"
          className="input-field"
          value={factorialForm.n}
          onChange={(e) => setFactorialForm({ n: e.target.value })}
          placeholder="e.g., 5"
          min="0"
          disabled={loading}
        />
        <p className="text-xs text-gray-500 mt-1">
          Calculate n! = n × (n-1) × ... × 1
        </p>
      </div>
      <button
        onClick={() => handleCalculation('factorial')}
        disabled={loading || !factorialForm.n}
        className="btn-primary w-full flex items-center justify-center space-x-2"
      >
        {loading ? (
          <div className="loading-spinner w-4 h-4" />
        ) : (
          <Factorial className="w-4 h-4" />
        )}
        <span>Calculate {factorialForm.n}!</span>
      </button>
    </div>
  );

  return (
    <div className="card animate-fade-in">
      <div className="flex items-center space-x-2 mb-6">
        <CalculatorIcon className="w-6 h-6 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-800">Math Calculator</h2>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
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
              <Icon className={`w-4 h-4 ${activeTab === tab.id ? tab.color : ''}`} />
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
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg animate-slide-up">
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
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg animate-slide-up">
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

export default Calculator;