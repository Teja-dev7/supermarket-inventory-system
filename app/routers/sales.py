from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.inventory import process_sale

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale_in: SaleCreate, db: Session = Depends(get_db)):
    """Process a new sale: automatically verifies stock, deducts quantity, and creates sale record."""
    return process_sale(db, product_id=sale_in.product_id, quantity=sale_in.quantity)


@router.get("/", response_model=List[SaleResponse])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve sale history."""
    return (
        db.query(Sale)
        .order_by(Sale.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """Retrieve details for a specific sale record."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sale with ID {sale_id} not found.",
        )
    return sale
