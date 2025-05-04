from django.urls import path
from .views import ProductSearchView, ReserveProductView

urlpatterns = [
    # 商品搜索接口（GET /api/inventory/products/search/）
    path(
        "products/search/",
        ProductSearchView.as_view(),
        name="product-search"
    ),
    
    # 商品预订接口（POST /api/inventory/products/reserve/）
    path(
        "products/reserve/",
        ReserveProductView.as_view(),
        name="product-reserve"
    ),
]