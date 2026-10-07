from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.schemas.inventory import StockAddRequest, LowStockProductResponse
from app.schemas.product import ProductResponse
from app.services.inventory import add_stock, get_low_stock_products

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=List[ProductResponse])
def get_inventory_overview(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve full inventory list with current stock levels."""
    return db.query(Product).offset(skip).limit(limit).all()


@router.post("/{product_id}/add", response_model=ProductResponse)
def restock_product(
    product_id: int,
    stock_in: StockAddRequest,
    db: Session = Depends(get_db),
):
    """Add stock to an existing product."""
    return add_stock(db, product_id=product_id, quantity=stock_in.quantity)


@router.get("/low-stock", response_model=List[LowStockProductResponse])
def get_low_stock_items(db: Session = Depends(get_db)):
    """Retrieve products where current stock is less than or equal to their low stock threshold."""
    return get_low_stock_products(db)
