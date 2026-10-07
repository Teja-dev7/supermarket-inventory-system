from pydantic import BaseModel, Field


class StockAddRequest(BaseModel):
    quantity: int = Field(..., gt=0, description="Quantity to add, must be greater than 0")


class LowStockProductResponse(BaseModel):
    id: int
    name: str
    stock_quantity: int
    low_stock_threshold: int
    category_id: int
    price: float

    class Config:
        from_attributes = True
