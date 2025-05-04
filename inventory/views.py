from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.utils.decorators import sync_and_async_middleware
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async
from .services import ProductService, InventoryService

@method_decorator(require_http_methods(["GET"]), name='dispatch')
@method_decorator(sync_and_async_middleware, name='dispatch')
class ProductSearchView(View):
    async def get(self, request):
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
       
        try:
            # 异步化查询
            page_obj = await sync_to_async(ProductService.search_products)(keyword, page)
            data = [{'id': p.id, 'name': p.name} for p in page_obj]
            return JsonResponse({
                'data': data,
                'page': page,
                'total_pages': page_obj.paginator.num_pages
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(require_http_methods(["POST"]), name='dispatch')
@method_decorator(sync_and_async_middleware, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch') 
class ReserveProductView(View):
    async def post(self, request):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 0))
        try:
            success = await sync_to_async(InventoryService.deduct_inventory)(product_id, quantity)
            return JsonResponse({'success': success})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)