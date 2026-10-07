from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.product import ProductResponse


class SaleCreate(BaseModel):
    product_id: int = Field(..., gt=0, description="ID of the product being purchased")
    quantity: int = Field(..., gt=0, description="Quantity to purchase (must be > 0)")


class SaleResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    created_at: datetime
    product: Optional[ProductResponse] = None

    model_config = ConfigDict(from_attributes=True)
