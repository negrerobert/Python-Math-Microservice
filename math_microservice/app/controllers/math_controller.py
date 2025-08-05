"""
Mathematical operations controller with caching support
Contains the business logic for all math operations
"""
import math
from typing import Union, Dict, Any
from app.utils.cache import math_cache
from app.utils.exceptions import MathOperationError
from app.utils.logger import app_logger, cache_logger


class MathController:
    """Controller class containing all mathematical operations with caching"""

    @staticmethod
    def calculate_power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """
        Calculate base raised to the power of exponent with caching

        Args:
            base: The base number
            exponent: The exponent

        Returns:
            Result of base^exponent

        Raises:
            MathOperationError: If calculation fails or results in overflow
        """
        operation = "power"
        params = {"base": base, "exponent": exponent}

        # Check cache first
        try:
            cached_result = math_cache.get(operation, params)
            if cached_result is not None:
                cache_logger.debug("Cache hit for power calculation", extra={
                    'base': base,
                    'exponent': exponent,
                    'result': cached_result,
                    'calculation_time_saved': True
                })
                return cached_result
        except Exception as e:
            cache_logger.warning("Cache get failed for power", extra={'error': str(e)})

        # Perform calculation
        try:
            result = base ** exponent

            # Check for infinity or very large numbers
            if math.isinf(result) or abs(result) > 1e100:
                raise MathOperationError(
                    operation=operation,
                    message="Result too large - calculation would cause overflow",
                    input_data=params
                )

            # Cache the result
            try:
                math_cache.set(operation, params, result)
                cache_logger.debug("Cached power calculation result", extra={
                    'base': base,
                    'exponent': exponent,
                    'result': result
                })
            except Exception as e:
                cache_logger.warning("Cache set failed for power", extra={'error': str(e)})

            app_logger.debug("Power calculation completed", extra={
                'base': base,
                'exponent': exponent,
                'result': result,
                'cached': False
            })

            return result

        except OverflowError:
            raise MathOperationError(
                operation=operation,
                message="Calculation overflow - numbers too large to compute",
                input_data=params
            )
        except (ValueError, ArithmeticError) as e:
            raise MathOperationError(
                operation=operation,
                message=f"Invalid calculation: {str(e)}",
                input_data=params
            )

    @staticmethod
    def calculate_fibonacci(n: int) -> int:
        """
        Calculate the nth Fibonacci number using iterative approach with caching

        Args:
            n: Position in Fibonacci sequence (0-indexed)

        Returns:
            The nth Fibonacci number

        Raises:
            MathOperationError: If calculation fails or n is invalid

        Note:
            F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)
        """
        operation = "fibonacci"
        params = {"n": n}

        # Validate input
        if n < 0:
            raise MathOperationError(
                operation=operation,
                message="Fibonacci sequence is not defined for negative numbers",
                input_data=params
            )

        if n > 1000:  # Prevent extremely large calculations
            raise MathOperationError(
                operation=operation,
                message="Fibonacci calculation limited to n <= 1000 for performance reasons",
                input_data=params
            )

        # Check cache first
        try:
            cached_result = math_cache.get(operation, params)
            if cached_result is not None:
                cache_logger.debug("Cache hit for fibonacci calculation", extra={
                    'n': n,
                    'result': cached_result
                })
                return int(cached_result)
        except Exception as e:
            cache_logger.warning("Cache get failed for fibonacci", extra={'error': str(e)})

        # Perform calculation
        try:
            if n == 0:
                result = 0
            elif n == 1:
                result = 1
            else:
                # Iterative approach for better performance
                a, b = 0, 1
                for _ in range(2, n + 1):
                    a, b = b, a + b
                result = b

            # Cache the result
            try:
                math_cache.set(operation, params, result)
                cache_logger.debug("Cached fibonacci calculation result", extra={
                    'n': n,
                    'result': result
                })
            except Exception as e:
                cache_logger.warning("Cache set failed for fibonacci", extra={'error': str(e)})

            app_logger.debug("Fibonacci calculation completed", extra={
                'n': n,
                'result': result,
                'cached': False
            })

            return result

        except Exception as e:
            raise MathOperationError(
                operation=operation,
                message=f"Fibonacci calculation failed: {str(e)}",
                input_data=params
            )

    @staticmethod
    def calculate_factorial(n: int) -> int:
        """
        Calculate factorial of n (n!) with caching

        Args:
            n: Non-negative integer

        Returns:
            n! = n × (n-1) × (n-2) × ... × 1

        Raises:
            MathOperationError: If calculation fails or n is invalid

        Note:
            0! = 1 by definition
        """
        operation = "factorial"
        params = {"n": n}

        # Validate input
        if n < 0:
            raise MathOperationError(
                operation=operation,
                message="Factorial is not defined for negative numbers",
                input_data=params
            )

        if n > 170:  # Factorial of 171 overflows in most systems
            raise MathOperationError(
                operation=operation,
                message="Factorial calculation limited to n <= 170 to prevent overflow",
                input_data=params
            )

        # Check cache first
        try:
            cached_result = math_cache.get(operation, params)
            if cached_result is not None:
                cache_logger.debug("Cache hit for factorial calculation", extra={
                    'n': n,
                    'result': cached_result
                })
                return int(cached_result)
        except Exception as e:
            cache_logger.warning("Cache get failed for factorial", extra={'error': str(e)})

        # Perform calculation
        try:
            if n == 0 or n == 1:
                result = 1
            else:
                result = 1
                for i in range(2, n + 1):
                    result *= i
                    # Additional safety check for extremely large numbers
                    if result > 1e100:
                        raise MathOperationError(
                            operation=operation,
                            message="Factorial result too large",
                            input_data=params
                        )

            # Cache the result
            try:
                math_cache.set(operation, params, result)
                cache_logger.debug("Cached factorial calculation result", extra={
                    'n': n,
                    'result': result
                })
            except Exception as e:
                cache_logger.warning("Cache set failed for factorial", extra={'error': str(e)})

            app_logger.debug("Factorial calculation completed", extra={
                'n': n,
                'result': result,
                'cached': False
            })

            return result

        except Exception as e:
            if isinstance(e, MathOperationError):
                raise
            raise MathOperationError(
                operation=operation,
                message=f"Factorial calculation failed: {str(e)}",
                input_data=params
            )