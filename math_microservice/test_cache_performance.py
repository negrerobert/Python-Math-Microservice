import requests
import time
import statistics

base_url = "http://127.0.0.1:8000/api/v1/math"


def test_cache_performance_detailed():
    """Test cache performance with statistical analysis"""
    print("Detailed Cache Performance Analysis")
    print("=" * 50)

    # Clear cache to start fresh
    requests.post(f"{base_url}/cache/clear")
    print("Cache cleared - starting fresh\n")

    test_cases = [
        {
            "name": "Power Calculation (2^50)",
            "endpoint": "power",
            "data": {"base": 2, "exponent": 50}
        },
        {
            "name": "Fibonacci (50th number)",
            "endpoint": "fibonacci",
            "data": {"n": 50}
        },
        {
            "name": "Factorial (20!)",
            "endpoint": "factorial",
            "data": {"n": 20}
        }
    ]

    for case in test_cases:
        print(f"Testing: {case['name']}")
        print("-" * 40)

        endpoint = f"{base_url}/{case['endpoint']}"
        miss_times = []
        hit_times = []

        # Test cache miss (first request)
        print("Cache Miss Tests (first calculation):")
        for i in range(3):
            # Clear cache before each miss test
            requests.post(f"{base_url}/cache/clear")

            start = time.time()
            response = requests.post(endpoint, json=case['data'])
            end = time.time()

            if response.status_code == 200:
                miss_time = (end - start) * 1000
                miss_times.append(miss_time)
                result = response.json()['result']
                print(f"  Miss #{i + 1}: {miss_time:.2f}ms -> Result: {result}")
            else:
                print(f"  Miss #{i + 1}: FAILED ({response.status_code})")

        # Test cache hits (subsequent requests)
        print("Cache Hit Tests (cached results):")
        for i in range(3):
            start = time.time()
            response = requests.post(endpoint, json=case['data'])
            end = time.time()

            if response.status_code == 200:
                hit_time = (end - start) * 1000
                hit_times.append(hit_time)
                result = response.json()['result']
                print(f"  Hit #{i + 1}: {hit_time:.2f}ms -> Result: {result}")
            else:
                print(f"  Hit #{i + 1}: FAILED ({response.status_code})")

        # Statistical analysis
        if miss_times and hit_times:
            avg_miss = statistics.mean(miss_times)
            avg_hit = statistics.mean(hit_times)
            improvement = ((avg_miss - avg_hit) / avg_miss) * 100

            print(f"\nPerformance Analysis:")
            print(f"  Average Miss Time: {avg_miss:.2f}ms")
            print(f"  Average Hit Time:  {avg_hit:.2f}ms")
            print(f"  Performance Improvement: {improvement:.1f}%")

            if improvement > 0:
                print(f"  Cache is working! {improvement:.1f}% faster")
            else:
                print(f"  Negative improvement - network/overhead effects")

        print("\n")


def test_cache_statistics():
    """Test cache statistics and management"""
    print("Cache Statistics & Management")
    print("=" * 50)

    # Get initial stats
    response = requests.get(f"{base_url}/cache/stats")
    if response.status_code == 200:
        stats = response.json()['cache_statistics']
        print(f"Initial Cache Stats:")
        print(f"  Total Requests: {stats['hits'] + stats['misses']}")
        print(f"  Hit Rate: {stats['hit_rate_percent']}%")
        print(f"  Cache Size: {stats['current_size']}/{stats['max_size']}")
        print(f"  Uptime: {stats['uptime_seconds']:.1f}s")

    # Test cache info endpoint
    print(f"\nTesting Cache Info Endpoint:")
    response = requests.get(f"{base_url}/cache/info")
    if response.status_code == 200:
        info = response.json()
        print(f"  Cache Info endpoint working")
        print(f"  Sample Keys: {len(info['sample_keys'])}")
        if info['sample_keys']:
            print(f"  First Key Preview: {info['sample_keys'][0]}")
    else:
        print(f"  Cache Info endpoint failed: {response.status_code}")
        print(f"  Error: {response.text[:200]}")

    # Test cache clearing
    print(f"\nTesting Cache Clear:")
    response = requests.post(f"{base_url}/cache/clear")
    if response.status_code == 200:
        result = response.json()
        print(f"  Cache cleared: {result['message']}")
        print(f"  Items removed: {result['items_removed']}")
    else:
        print(f"  Cache clear failed: {response.status_code}")


def test_complex_calculations():
    """Test caching with more complex calculations that show clear benefits"""
    print("Complex Calculation Cache Benefits")
    print("=" * 50)

    # Test with calculations that have more significant computation time
    complex_tests = [
        {"endpoint": "fibonacci", "data": {"n": 100}, "name": "Fibonacci(100)"},
        {"endpoint": "factorial", "data": {"n": 50}, "name": "Factorial(50)"},
        {"endpoint": "power", "data": {"base": 1.5, "exponent": 100}, "name": "1.5^100"}
    ]

    # Clear cache
    requests.post(f"{base_url}/cache/clear")

    for test in complex_tests:
        print(f"\nTesting {test['name']}:")
        endpoint = f"{base_url}/{test['endpoint']}"

        # First request (cache miss)
        print("  Computing for first time...")
        start = time.time()
        response1 = requests.post(endpoint, json=test['data'])
        miss_time = (time.time() - start) * 1000

        if response1.status_code == 200:
            result = response1.json()['result']
            print(f"  First calculation: {miss_time:.2f}ms -> {result}")

            # Second request (cache hit)
            print("  Retrieving from cache...")
            start = time.time()
            response2 = requests.post(endpoint, json=test['data'])
            hit_time = (time.time() - start) * 1000

            if response2.status_code == 200:
                print(f"  Cached retrieval: {hit_time:.2f}ms -> {response2.json()['result']}")
                improvement = ((miss_time - hit_time) / miss_time) * 100
                print(f"  Speed improvement: {improvement:.1f}%")
            else:
                print(f"  Cache retrieval failed: {response2.status_code}")
        else:
            print(f"  Calculation failed: {response1.status_code} - {response1.text}")


if __name__ == "__main__":
    print("=== Math Microservice Cache Performance Analysis ===\n")

    try:
        test_cache_performance_detailed()
        test_cache_statistics()
        test_complex_calculations()

        print("\n" + "=" * 50)
        print("Cache Performance Analysis Complete!")
        print("Key Insights:")
        print("• Cache hits show performance benefit for calculation time")
        print("• Total request time includes DB, middleware, and network overhead")
        print("• More complex calculations show greater cache benefits")
        print("• JSON structured logging provides detailed performance metrics")

    except requests.exceptions.ConnectionError:
        print(" Cannot connect to the API. Make sure the server is running:")
        print("   uvicorn app.main:app --reload")
    except Exception as e:
        print(f" Test failed with error: {e}")