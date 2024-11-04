from functools import wraps


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
