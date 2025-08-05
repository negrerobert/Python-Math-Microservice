import requests
import time
import json

base_url = "http://127.0.0.1:8000/api/v1/math"

def test_caching_performance():
    """Test cache performance with repeated requests"""
    print("Testing Cache Performance...")

    # Test same calculation multiple times
    test_cases = [
        {"endpoint": "power", "data": {"base": 2, "exponent": 10}},
        {"endpoint": "fibonacci", "data": {"n": 30}},
        {"endpoint": "factorial", "data": {"n": 10}}
    ]

    for case in test_cases:
        print(f"\n--- Testing {case['endpoint']} caching ---")
        endpoint = f"{base_url}/{case['endpoint']}"

        # First request (cache miss)
        start = time.time()
        response1 = requests.post(endpoint, json=case['data'])
        time1 = time.time() - start

        # Second request (should be cache hit)
        start = time.time()
        response2 = requests.post(endpoint, json=case['data'])
        time2 = time.time() - start

        # Third request (should also be cache hit)
        start = time.time()
        response3 = requests.post(endpoint, json=case['data'])
        time3 = time.time() - start

        print(f"First request (cache miss):  {time1*1000:.2f}ms")
        print(f"Second request (cache hit):  {time2*1000:.2f}ms")
        print(f"Third request (cache hit):   {time3*1000:.2f}ms")

        if response1.status_code == 200:
            result = response1.json()['result']
            print(f"Result: {result}")
            print(f"Speed improvement: {((time1-time2)/time1*100):.1f}%")
        else:
            print(f"Error: {response1.text}")

def test_cache_management():
    """Test cache management endpoints"""
    print("\nTesting Cache Management...")

    # Get cache stats
    response = requests.get(f"{base_url}/cache/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"Cache Stats: {json.dumps(stats, indent=2)}")

    # Get cache info
    response = requests.get(f"{base_url}/cache/info")
    if response.status_code == 200:
        info = response.json()
        print(f"Cache has {info['total_keys']} keys")
        print(f"Hit rate: {info['stats']['hit_rate_percent']}%")

    # Clear cache
    response = requests.post(f"{base_url}/cache/clear")
    if response.status_code == 200:
        result = response.json()
        print(f"Cache cleared: {result['message']}")

def test_error_handling():
    """Test enhanced error handling"""
    print("\nTesting Error Handling...")

    error_cases = [
        {"endpoint": "power", "data": {"base": 2, "exponent": 1000}, "description": "Power overflow"},
        {"endpoint": "fibonacci", "data": {"n": -5}, "description": "Negative fibonacci"},
        {"endpoint": "fibonacci", "data": {"n": 2000}, "description": "Fibonacci too large"},
        {"endpoint": "factorial", "data": {"n": -1}, "description": "Negative factorial"},
        {"endpoint": "factorial", "data": {"n": 200}, "description": "Factorial too large"},
    ]

    for case in error_cases:
        endpoint = f"{base_url}/{case['endpoint']}"
        response = requests.post(endpoint, json=case['data'])

        print(f"\n{case['description']}:")
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            error_detail = response.json()
            print(f"Error Type: {error_detail.get('error_type', 'Unknown')}")
            print(f"Message: {error_detail.get('error', 'No message')}")

def test_validation_errors():
    """Test input validation errors"""
    print("\nTesting Input Validation...")

    validation_cases = [
        {"endpoint": "power", "data": {"base": "not_a_number", "exponent": 2}},
        {"endpoint": "fibonacci", "data": {"n": "invalid"}},
        {"endpoint": "factorial", "data": {}},  # Missing required field
    ]

    for case in validation_cases:
        endpoint = f"{base_url}/{case['endpoint']}"
        response = requests.post(endpoint, json=case['data'])

        print(f"\nTesting {case['endpoint']} with invalid data:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 422:
            error_detail = response.json()
            print(f"Validation errors: {len(error_detail.get('details', []))}")

def test_performance_monitoring():
    """Test performance monitoring features"""
    print("\nTesting Performance Monitoring...")

    # Make several requests to generate data
    for i in range(5):
        requests.post(f"{base_url}/power", json={"base": 2, "exponent": i+1})
        requests.post(f"{base_url}/fibonacci", json={"n": i*2})

    # Check operation stats
    response = requests.get(f"{base_url}/stats")
    if response.status_code == 200:
        stats = response.json()
        print("Operation Statistics:")
        for stat in stats:
            print(f"  {stat['operation']}: {stat['total_requests']} requests, "
                  f"{stat['success_rate']}% success, "
                  f"{stat['avg_execution_time_ms']}ms avg")

    # Check history
    response = requests.get(f"{base_url}/history?page_size=5")
    if response.status_code == 200:
        history = response.json()
        print(f"\nRecent History ({history['total_records']} total records):")
        for req in history['requests'][:3]:
            # Handle None results for failed operations
            result_display = req['result'] if req['result'] is not None else "FAILED"
            success_indicator = "✓" if req['success'] else "✗"
            exec_time = req.get('execution_time_ms', 0) or 0
            print(f"  {success_indicator} {req['operation']}: {result_display} "
                  f"({exec_time:.3f}ms)")

    # Test cache info endpoint (this was failing before)
    response = requests.get(f"{base_url}/cache/info")
    if response.status_code == 200:
        cache_info = response.json()
        print(f"\nCache Info: {cache_info['total_keys']} keys, "
              f"Hit rate: {cache_info['stats']['hit_rate_percent']}%")
    else:
        print(f"\nCache info endpoint failed with status {response.status_code}")
        if response.text:
            print(f"Error: {response.text[:200]}...")

def test_headers_and_logging():
    """Test custom headers and logging features"""
    print("\nTesting Headers and Logging...")

    response = requests.post(f"{base_url}/power", json={"base": 3, "exponent": 4})

    print("Response Headers:")
    print(f"  Request ID: {response.headers.get('X-Request-ID', 'Not found')}")
    print(f"  Processing Time: {response.headers.get('X-Processing-Time-MS', 'Not found')}ms")
    print(f"  Content Type: {response.headers.get('Content-Type', 'Not found')}")

if __name__ == "__main__":
    print("=== Math Microservice Advanced Features Test ===")
    print("Testing Phase 3 (Logging & Error Handling) + Phase 4 (Caching)")

    try:
        test_caching_performance()
        test_cache_management()
        test_error_handling()
        test_validation_errors()
        test_performance_monitoring()
        test_headers_and_logging()

        print("\nAll tests completed!")
        print("\nCheck your logs for detailed JSON output!")
        print("Visit http://127.0.0.1:8000/docs to see the enhanced API documentation")

    except requests.exceptions.ConnectionError:
        print("Cannot connect to the API. Make sure the server is running:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f"Test failed with error: {e}")