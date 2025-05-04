from django.db import transaction, DatabaseError
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Inventory
from .cache import InventoryCache

class ProductService:
    @staticmethod
    def search_products(keyword: str, page: int = 1, page_size: int = 10):
        queryset = Product.objects.filter(name__icontains=keyword)
        return Paginator(queryset.only('id', 'name'), page_size).get_page(page)

class InventoryService:
    @staticmethod
    @transaction.atomic
    def deduct_inventory(product_id: int, quantity: int) -> bool:
        try:
            #查找库存
            inventory = (Inventory.objects.select_for_update(skip_locked=True).get(product_id=product_id))
            if inventory.quantity < quantity:
                return False
            # 更新
            updated = (Inventory.objects.filter(product_id=product_id, version=inventory.version)
                .update(
                    quantity=F('quantity') - quantity,
                    version=F('version') + 1
                )
            )
            if updated == 0:
                raise DatabaseError("并发更新冲突")
            InventoryCache.invalidate_cache(product_id)
            return True
        except Inventory.DoesNotExist:
            raise ValueError("商品不存在")
        except DatabaseError as e:
            transaction.set_rollback(True)
            raise e