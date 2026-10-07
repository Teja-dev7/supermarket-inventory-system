from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.inventory import router as inventory_router
from app.routers.sales import router as sales_router

__all__ = ["categories_router", "products_router", "inventory_router", "sales_router"]
