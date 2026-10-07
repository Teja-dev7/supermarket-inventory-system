from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, description="Product name")
    category_id: int = Field(..., gt=0, description="Category ID this product belongs to")
    price: float = Field(..., gt=0, description="Price of the product, must be greater than 0")
    stock_quantity: int = Field(0, ge=0, description="Initial stock quantity, cannot be negative")
    low_stock_threshold: int = Field(10, ge=0, description="Threshold below which item is flagged as low stock")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    category_id: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    low_stock_threshold: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)
