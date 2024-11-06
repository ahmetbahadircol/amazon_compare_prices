from functools import wraps
import time
from sp_api.base.exceptions import (
    SellingApiRequestThrottledException,
    SellingApiForbiddenException,
)

from auth_amazon import auth


def ensure_collection(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.set_collection is None:
            print(
                "Collection is not set. Please set the collection before using this method."
            )
            return
        return func(self, *args, **kwargs)

    return wrapper


def retry_on_throttling(delay=1, max_retries=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except SellingApiRequestThrottledException as e:
                    if attempt < max_retries - 1:
                        print(f"Quota exceeded, retrying in {current_delay} seconds...")
                        time.sleep(current_delay)
                        current_delay *= 2
                    else:
                        print("Max retries reached, failing...")
                        raise e

        return wrapper

    return decorator


def reauth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SellingApiForbiddenException:
            print("Re-Auth is needed. Re-authaticating...")
            auth()
            return func(*args, **kwargs)

    return wrapper
