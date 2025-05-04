from django.core.cache import caches
from django.core.cache.backends.redis import RedisCache

class InventoryCache:
    _cache: RedisCache = caches['inventory']  # 使用独立 Redis 缓存池

    @classmethod
    def get_inventory(cls, product_id: int) -> int:
        key = f'inventory:{product_id}'
        cached = cls._cache.get(key)
        if cached is not None:
            return int(cached)
        inventory = Inventory.objects.only('quantity').get(product_id=product_id).quantity
        cls._cache.set(key, inventory, timeout=30)  
        return inventory

    @classmethod
    def invalidate_cache(cls, product_id: int) -> None:
        cls._cache.delete(f'inventory:{product_id}')
        # cls._cache.client.publish('invalidation_channel', f'inventory:{product_id}')
