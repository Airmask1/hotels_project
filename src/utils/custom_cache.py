import json
from functools import wraps

from src.setup import redis_manager


def custom_cache(expire: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}"
            cached_value = await redis_manager.get(cache_key)
            if cached_value:
                print("Cache hit")
                return json.loads(cached_value)
            results = await func(*args, **kwargs)
            results_schemas = [r.model_dump() for r in results]
            results = json.dumps(results_schemas)
            await redis_manager.set(cache_key, results, expire=expire)
            return results_schemas

        return wrapper

    return decorator
