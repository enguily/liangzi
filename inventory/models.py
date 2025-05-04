from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # 商品名称（添加索引优化查询）
    description = models.TextField()                        # 商品描述
    
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.IntegerField(default=0)  # 当前库存
    version = models.IntegerField(default=0)   # 版本号

    class Meta:
        indexes = [
            models.Index(fields=['product'], name='inventory_product_idx'),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name="non_negative_quantity",
                violation_error_message="库存不可为负数"
            )
        ]
