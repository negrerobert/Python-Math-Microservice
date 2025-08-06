# Math Microservice

A microservice for mathematical operations built with FastAPI, featuring database persistence, caching and monitoring.

## Core Features

- **Mathematical Operations**: Power (`a^b`), Fibonacci sequence, Factorial calculations
- **Database Persistence**: All API requests stored with SQLAlchemy + SQLite
- **Caching**: TTL-based cache with 95% performance improvement on repeated operations
- **Monitoring**: Structured JSON logging, performance metrics, request tracking
- **REST API**: OpenAPI/Swagger documentation with proper error handling
- **MVC Architecture**: Clean separation of concerns

## Architecture

```
API Layer (FastAPI Routes) → Controllers (Business Logic) → Models (Database) → Utils (Cache/Logging)
```

**Tech Stack**: FastAPI + SQLAlchemy + SQLite + TTL Cache + Pydantic validation

## Requirements

- **Python 3.8+**
- **Dependencies**: FastAPI, SQLAlchemy, Pydantic, SQLite (see `requirements.txt`)

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/negrerobert/Python-Math-Microservice
cd Python-Math-Microservice
```

### 2. Backend Setup (Main Application)
```bash
# Navigate to backend directory
cd math_microservice

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload
```

**Backend runs at**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### 3. Frontend Setup (Optional Demo Interface)
```bash
# Navigate to frontend directory
cd ../math-frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

**Frontend runs at**: `http://localhost:3000`

## API Usage

### Core Endpoints

| Method | Endpoint | Description | Example |
|--------|----------|-------------|---------|
| `POST` | `/api/v1/math/power` | Calculate base^exponent | `{"base": 2, "exponent": 10}` |
| `POST` | `/api/v1/math/fibonacci` | Get nth Fibonacci number | `{"n": 10}` |
| `POST` | `/api/v1/math/factorial` | Calculate n! | `{"n": 5}` |
| `GET` | `/api/v1/math/stats` | Operation statistics | - |
| `GET` | `/api/v1/math/history` | Request history | - |
| `GET` | `/api/v1/math/cache/stats` | Cache performance | - |

### Quick Test
```bash
# Power calculation
curl -X POST "http://localhost:8000/api/v1/math/power" \
     -H "Content-Type: application/json" \
     -d '{"base": 2, "exponent": 10}'

# Response: {"operation": "power", "result": 1024, "success": true}
```

## Testing

Run the test suite:
```bash
# Test all features
python test_advanced_features.py

# Test cache performance  
python test_cache_performance.py

# Test database persistence
python test_persistence.py
```

**Expected Results**:
- Cache hit rates improve from 0% to 80%+ on repeated operations
- Response times: ~25ms (cache miss) → ~2ms (cache hit)
- All operations persist to SQLite database

## Performance Features

### Caching System
- **5-minute TTL** with 1000 item capacity
- **95% speed improvement** for repeated calculations
- **Cache management** endpoints for monitoring and clearing

### Monitoring & Logging
- **Structured JSON logging** with unique request IDs
- **Performance metrics**: Response times, success rates, error tracking  
- **Request persistence**: Complete audit trail in SQLite
- **Real-time statistics** via API endpoints



## Key Implementation Details

### MVC Architecture
- **Routes**: API endpoints with validation
- **Controllers**: Business logic with caching
- **Models**: Database schemas and operations
- **Utils**: Cross-cutting concerns (logging, caching, exceptions)

### Database Schema
```sql
-- API Requests (audit trail)
api_requests: id, operation, input_data, result, success, timestamp, execution_time_ms

-- Operation Statistics (performance tracking)  
operation_stats: operation, total_requests, success_rate, avg_execution_time_ms
```
