"""Module containing core utility functions."""
import time
from functools import wraps


def time_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        end_time = time.time()
        setattr(
            response,
            "data",
            {
                "time": end_time - start_time,
                "objects": response.data,
            },
        )
        return response

    return wrapper
