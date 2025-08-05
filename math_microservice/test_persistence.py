import requests
import time

base_url = "http://127.0.0.1:8000/api/v1/math"


def test_operations():
    """Test all mathematical operations"""
    print("Testing mathematical operations...")

    # Test power
    response = requests.post(f"{base_url}/power", json={"base": 2, "exponent": 3})
    print(f"Power: {response.json()}")

    # Test fibonacci
    response = requests.post(f"{base_url}/fibonacci", json={"n": 10})
    print(f"Fibonacci: {response.json()}")

    # Test factorial
    response = requests.post(f"{base_url}/factorial", json={"n": 5})
    print(f"Factorial: {response.json()}")

    # Test error case
    response = requests.post(f"{base_url}/factorial", json={"n": -1})
    print(f"Error case status: {response.status_code}")


def test_history():
    """Test history endpoint"""
    print("\nTesting history endpoint...")

    response = requests.get(f"{base_url}/history")
    history = response.json()
    print(f"Total records: {history['total_records']}")
    print(f"Number of requests returned: {len(history['requests'])}")

    if history['requests']:
        latest = history['requests'][0]
        print(f"Latest request: {latest['operation']} -> {latest['result']}")


def test_stats():
    """Test statistics endpoint"""
    print("\nTesting statistics endpoint...")

    response = requests.get(f"{base_url}/stats")
    stats = response.json()

    for stat in stats:
        print(f"Operation: {stat['operation']}")
        print(f"  Total requests: {stat['total_requests']}")
        print(f"  Success rate: {stat['success_rate']}%")
        print(f"  Avg execution time: {stat['avg_execution_time_ms']:.3f}ms")


if __name__ == "__main__":
    print("=== Math Microservice Database Persistence Test ===")

    # Test operations (this will create database records)
    test_operations()

    # Small delay to ensure database writes complete
    time.sleep(0.5)

    # Test history and stats
    test_history()
    test_stats()

    print("\n=== Test completed! ===")
    print("Check your database file: math_microservice.db")