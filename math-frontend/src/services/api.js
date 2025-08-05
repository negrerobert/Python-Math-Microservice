import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api/v1/math',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add request ID for tracking
api.interceptors.request.use(
  (config) => {
    const requestId = Math.random().toString(36).substr(2, 9);
    config.headers['X-Request-ID'] = requestId;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const customError = {
      message: 'An unexpected error occurred',
      status: error.response?.status || 500,
      details: null,
      requestId: error.config?.headers['X-Request-ID'],
    };

    if (error.response?.data) {
      customError.message = error.response.data.error || error.response.data.message || customError.message;
      customError.details = error.response.data.details;
      customError.errorType = error.response.data.error_type;
    } else if (error.request) {
      customError.message = 'Network error - could not connect to the server';
      customError.status = 0;
    }

    return Promise.reject(customError);
  }
);

// Math Operations API
export const mathAPI = {
  // Power calculation
  async calculatePower(base, exponent) {
    try {
      const response = await api.post('/power', { base, exponent });
      return {
        success: true,
        data: response.data,
        processingTime: response.headers['x-processing-time-ms'],
        requestId: response.headers['x-request-id'],
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        details: error.details,
        errorType: error.errorType,
        status: error.status,
        requestId: error.requestId,
      };
    }
  },

  // Fibonacci calculation
  async calculateFibonacci(n) {
    try {
      const response = await api.post('/fibonacci', { n });
      return {
        success: true,
        data: response.data,
        processingTime: response.headers['x-processing-time-ms'],
        requestId: response.headers['x-request-id'],
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        details: error.details,
        errorType: error.errorType,
        status: error.status,
        requestId: error.requestId,
      };
    }
  },

  // Factorial calculation
  async calculateFactorial(n) {
    try {
      const response = await api.post('/factorial', { n });
      return {
        success: true,
        data: response.data,
        processingTime: response.headers['x-processing-time-ms'],
        requestId: response.headers['x-request-id'],
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        details: error.details,
        errorType: error.errorType,
        status: error.status,
        requestId: error.requestId,
      };
    }
  },

  // Get operation statistics
  async getStats() {
    try {
      const response = await api.get('/stats');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  },

  // Get cache statistics
  async getCacheStats() {
    try {
      const response = await api.get('/cache/stats');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  },

  // Get cache info
  async getCacheInfo() {
    try {
      const response = await api.get('/cache/info');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  },

  // Clear cache
  async clearCache() {
    try {
      const response = await api.post('/cache/clear');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  },

  // Get request history
  async getHistory(page = 1, pageSize = 20, operation = null) {
    try {
      const params = { page, page_size: pageSize };
      if (operation) params.operation = operation;
      
      const response = await api.get('/history', { params });
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
      };
    }
  },
};

export default api;