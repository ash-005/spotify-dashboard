"""Caching utilities for visualization functions."""

from functools import wraps
from datetime import datetime, timedelta

_cache = {}

def cache_plot(ttl_seconds=300):
    """
    Cache the output of a plotting function for a specified time.
    
    Args:
        ttl_seconds (int): Time to live in seconds for cached values
        
    Returns:
        Decorator function that caches plot HTML output
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = (
                func.__name__,
                str(args),
                str(sorted(kwargs.items()))
            )
            
            # Check if we have a valid cached value
            if cache_key in _cache:
                result, timestamp = _cache[cache_key]
                if datetime.now() - timestamp < timedelta(seconds=ttl_seconds):
                    return result
            
            # Generate and cache new result
            result = func(*args, **kwargs)
            _cache[cache_key] = (result, datetime.now())
            
            return result
        return wrapper
    return decorator
