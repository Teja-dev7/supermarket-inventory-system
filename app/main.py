from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
import app.models  # Import all models so Base knows about them
from app.routers import (
    categories_router,
    products_router,
    inventory_router,
    sales_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Automatically create tables in Supabase PostgreSQL if they do not exist
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Supermarket Inventory Management API",
    description="A complete backend for managing Categories, Products, Inventory, and Sales connected to Supabase PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(sales_router)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Supermarket Inventory Management API is running.",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }
