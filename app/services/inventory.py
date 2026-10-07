from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.sale import Sale


def process_sale(db: Session, product_id: int, quantity: int) -> Sale:
    """Processes a sale transaction:

    1. Checks if product exists.
    2. Validates positive quantity.
    3. Checks if sufficient stock is available (prevents negative stock).
    4. Deducts stock quantity from product.
    5. Records sale entry with unit and total price.
    6. Commits changes within a database transaction.
    """
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than zero.",
        )

    # Fetch product with row-level lock (with_for_update) for strong concurrency safety
    product = db.query(Product).filter(Product.id == product_id).with_for_update().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    if product.stock_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {product.stock_quantity}, Requested: {quantity}",
        )

    try:
        # Atomic stock deduction
        product.stock_quantity -= quantity

        total_price = round(product.price * quantity, 2)
        sale = Sale(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
            total_price=total_price,
        )

        db.add(sale)
        db.commit()
        db.refresh(sale)
        return sale
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process sale: {str(e)}",
        )


def add_stock(db: Session, product_id: int, quantity: int) -> Product:
    """Restocks a product:

    1. Verifies product existence.
    2. Ensures quantity > 0.
    3. Adds quantity to current stock.
    """
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restock quantity must be greater than zero.",
        )

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found.",
        )

    product.stock_quantity += quantity
    db.commit()
    db.refresh(product)
    return product


def get_low_stock_products(db: Session) -> List[Product]:
    """Retrieves all products where current stock is less than or equal to low stock threshold."""
    return (
        db.query(Product)
        .filter(Product.stock_quantity <= Product.low_stock_threshold)
        .order_by(Product.stock_quantity.asc())
        .all()
    )
