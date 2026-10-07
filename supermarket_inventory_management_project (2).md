# Supermarket Inventory Management Backend

## 1. Project Goal

Build a beginner-friendly backend for a **Supermarket Inventory Management System** using:

- Python
- FastAPI
- Supabase PostgreSQL
- SQLAlchemy
- Pydantic
- Uvicorn
- VS Code

The main business flow is:

```text
Category
   ↓
Products
   ↓
Stock
   ↓
Sale
   ↓
Stock automatically decreases
```

Example:

```text
Category: Beverages
Product: Coca-Cola 500ml
Stock: 100

Customer buys 3

Stock becomes:
100 - 3 = 97
```

---

# 2. What You Will Build

The application should support:

### Category Management

- Create category
- View all categories
- View one category
- Update category
- Delete category

Example:

```text
Beverages
Groceries
Dairy
Snacks
Personal Care
```

### Product Management

- Add product
- View products
- View products by category
- Update product
- Delete product

Example:

```text
Product:
Coca-Cola 500ml

Category:
Beverages

Price:
40

Stock:
100
```

### Inventory Management

- View current stock
- Add stock
- Reduce stock
- Detect low stock
- Prevent stock from becoming negative

### Sales

When a product is sold:

```text
POST /sales

product_id = 10
quantity = 3
```

Backend should:

1. Find the product.
2. Check available stock.
3. Check whether requested quantity is available.
4. Reduce stock.
5. Save the sale.
6. Return sale details.

Example:

```text
Before sale:
Stock = 100

Customer buys:
3

After sale:
Stock = 97
```

---

# 3. Recommended Project Structure

Create this folder:

```text
supermarket_inventory/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── sale.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── sale.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── categories.py
│   │   ├── products.py
│   │   └── sales.py
│   │
│   └── services/
│       ├── __init__.py
│       └── inventory.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

Do not try to build everything at once.

Build it in this order:

```text
Step 1 → Supabase
Step 2 → Database connection
Step 3 → Category
Step 4 → Product
Step 5 → Inventory
Step 6 → Sales
Step 7 → Low-stock logic
Step 8 → Validation/error handling
Step 9 → Testing
```

---

# 4. Install Packages

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic
```

Create `requirements.txt`:

```text
fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-dotenv
pydantic
```

---

# 5. Create Supabase Project

Create a Supabase project.

Supabase will provide a PostgreSQL database.

You will need the PostgreSQL connection string.

Put the connection string in `.env`.

Example:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@YOUR_HOST:5432/postgres
```

Do not commit `.env` to GitHub.

Create `.gitignore`:

```text
venv/
.env
__pycache__/
*.pyc
```

---

# 6. Understand the Database Design

We need three main tables.

```text
categories
    |
    | 1
    |
    | many
products
    |
    | 1
    |
    | many
sales
```

## Category Table

```text
categories
-------------------------
id
name
description
created_at
```

Example:

```text
1 | Beverages
2 | Groceries
3 | Dairy
```

## Product Table

```text
products
-------------------------
id
name
category_id
price
stock_quantity
low_stock_threshold
created_at
```

Example:

```text
1 | Coca-Cola 500ml | 1 | 40 | 100 | 10
2 | Milk 1L         | 3 | 60 | 50  | 5
```

## Sales Table

```text
sales
-------------------------
id
product_id
quantity
unit_price
total_price
created_at
```

Example:

```text
1 | 1 | 3 | 40 | 120
```

This means:

```text
Product:
Coca-Cola

Quantity sold:
3

Price:
40

Total:
3 × 40 = 120
```

---

# 7. Database Relationships

A category can contain many products.

```text
Beverages
    |
    ├── Coca-Cola
    ├── Pepsi
    └── Sprite
```

Therefore:

```text
Category 1 → Many Products
```

A product can have many sales.

```text
Coca-Cola
    |
    ├── Sale 1
    ├── Sale 2
    └── Sale 3
```

Therefore:

```text
Product 1 → Many Sales
```

---

# 8. Database Connection

Create:

```text
app/database.py
```

Purpose:

This file is responsible for connecting FastAPI to Supabase PostgreSQL.

Conceptually:

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL Driver
   ↓
Supabase PostgreSQL
```

You will create:

```python
engine
SessionLocal
Base
get_db()
```

Understand these carefully.

### engine

Responsible for communicating with PostgreSQL.

### SessionLocal

Creates a database session.

### Base

Parent class used by SQLAlchemy models.

### get_db()

Provides a database session to API endpoints.

---

# 9. Category Model

Create:

```text
app/models/category.py
```

Create a SQLAlchemy model:

```text
Category
```

Fields:

```text
id
name
description
created_at
```

Important:

```text
Category.id
```

will be the primary key.

---

# 10. Product Model

Create:

```text
app/models/product.py
```

Fields:

```text
id
name
category_id
price
stock_quantity
low_stock_threshold
created_at
```

Important:

```text
category_id
```

is a foreign key.

It connects:

```text
products.category_id
        ↓
categories.id
```

Example:

```text
Product:
Coca-Cola

category_id = 1
```

means:

```text
Coca-Cola belongs to category 1
```

---

# 11. Sale Model

Create:

```text
app/models/sale.py
```

Fields:

```text
id
product_id
quantity
unit_price
total_price
created_at
```

Relationships:

```text
sale.product_id
       ↓
product.id
```

---

# 12. Pydantic Schemas

Schemas define what data the API accepts and returns.

Create:

```text
app/schemas/category.py
app/schemas/product.py
app/schemas/sale.py
```

Example category input:

```json
{
    "name": "Beverages",
    "description": "Cold and hot beverages"
}
```

Example product input:

```json
{
    "name": "Coca-Cola 500ml",
    "category_id": 1,
    "price": 40,
    "stock_quantity": 100,
    "low_stock_threshold": 10
}
```

Example sale input:

```json
{
    "product_id": 1,
    "quantity": 3
}
```

---

# 13. API Design

Your API should eventually contain:

## Categories

```text
POST   /categories
GET    /categories
GET    /categories/{category_id}
PUT    /categories/{category_id}
DELETE /categories/{category_id}
```

## Products

```text
POST   /products
GET    /products
GET    /products/{product_id}
GET    /categories/{category_id}/products
PUT    /products/{product_id}
DELETE /products/{product_id}
```

## Inventory

```text
GET  /inventory
POST /inventory/{product_id}/add
```

## Sales

```text
POST /sales
GET  /sales
GET  /sales/{sale_id}
```

## Reports

Later add:

```text
GET /inventory/low-stock
GET /reports/sales
GET /reports/top-products
```

---

# 14. Main Business Logic

The most important part of this project is the sale process.

Suppose:

```text
Product:
Rice 5kg

Current stock:
20
```

Customer buys:

```text
quantity = 3
```

Backend performs:

```text
20 - 3
```

New stock:

```text
17
```

Then create a sale record.

---

# 15. Sale Algorithm

Your backend logic should be approximately:

```text
Receive sale request
        ↓
Get product
        ↓
Does product exist?
        ↓
No → return 404
        ↓
Yes
        ↓
Is requested quantity > 0?
        ↓
No → return 400
        ↓
Yes
        ↓
Is stock sufficient?
        ↓
No → return 400
        ↓
Yes
        ↓
Calculate total price
        ↓
Reduce stock
        ↓
Create sale record
        ↓
Commit transaction
        ↓
Return sale
```

Example:

```text
Stock = 10
Customer buys = 4

10 - 4 = 6
```

Database becomes:

```text
stock_quantity = 6
```

---

# 16. Never Allow Negative Stock

This is an important business rule.

Suppose:

```text
Stock = 5
```

Customer requests:

```text
Quantity = 8
```

Do NOT allow:

```text
5 - 8 = -3
```

Instead return an error:

```json
{
    "detail": "Insufficient stock"
}
```

---

# 17. Low Stock Logic

Each product has:

```text
low_stock_threshold
```

Example:

```text
Stock = 8
Threshold = 10
```

Then:

```text
8 <= 10
```

Product should be considered low stock.

API:

```text
GET /inventory/low-stock
```

Could return:

```json
[
    {
        "id": 1,
        "name": "Coca-Cola 500ml",
        "stock_quantity": 8,
        "low_stock_threshold": 10
    }
]
```

---

# 18. Add Stock

You should also support purchasing/restocking.

Example:

```text
Current stock = 20

New shipment = 50
```

Backend:

```text
20 + 50 = 70
```

API:

```text
POST /inventory/1/add
```

Request:

```json
{
    "quantity": 50
}
```

Result:

```text
Stock = 70
```

Validate that quantity is greater than zero.

---

# 19. Main.py

`app/main.py` should:

1. Create FastAPI application.
2. Import models.
3. Create/register routers.
4. Start the application.

Conceptually:

```text
main.py
   |
   ├── category router
   ├── product router
   └── sales router
```

Do not put all business logic into `main.py`.

Keep it clean.

---

# 20. Router Responsibility

## categories.py

Only category-related APIs.

```text
POST /categories
GET /categories
GET /categories/{id}
PUT /categories/{id}
DELETE /categories/{id}
```

## products.py

Only product-related APIs.

```text
POST /products
GET /products
GET /products/{id}
PUT /products/{id}
DELETE /products/{id}
```

## sales.py

Sales-related APIs.

```text
POST /sales
GET /sales
```

---

# 21. Service Layer

Create:

```text
app/services/inventory.py
```

Put important inventory business logic here.

For example:

```text
sell_product()
add_stock()
check_stock()
get_low_stock_products()
```

This is useful because business logic should not become mixed with API routing.

Architecture:

```text
Client
  ↓
FastAPI Router
  ↓
Service Layer
  ↓
SQLAlchemy
  ↓
Supabase PostgreSQL
```

---

# 22. Example Complete Business Flow

Imagine your supermarket has:

```text
Category:
Beverages

Product:
Coca-Cola 500ml

Price:
40

Stock:
100
```

Customer buys:

```text
3 Coca-Cola
```

Request:

```http
POST /sales
```

Body:

```json
{
    "product_id": 1,
    "quantity": 3
}
```

Backend:

```text
Find product 1
       ↓
Stock = 100
       ↓
Requested = 3
       ↓
100 >= 3
       ↓
Total = 40 × 3
       ↓
Total = 120
       ↓
Stock = 100 - 3
       ↓
Stock = 97
       ↓
Create sale
       ↓
Commit
```

Response should contain something like:

```json
{
    "sale_id": 1,
    "product_id": 1,
    "quantity": 3,
    "unit_price": 40,
    "total_price": 120
}
```

---

# 23. Testing With Swagger

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI will show your APIs.

Test in this order.

### Step 1

Create category:

```json
{
    "name": "Beverages",
    "description": "Drinks"
}
```

### Step 2

Create product:

```json
{
    "name": "Coca-Cola 500ml",
    "category_id": 1,
    "price": 40,
    "stock_quantity": 100,
    "low_stock_threshold": 10
}
```

### Step 3

Check product:

```text
Stock = 100
```

### Step 4

Create sale:

```json
{
    "product_id": 1,
    "quantity": 3
}
```

### Step 5

Check product again.

Expected:

```text
Stock = 97
```

---

# 24. Test Edge Cases

Do not test only the happy path.

Test:

### Product does not exist

```text
product_id = 999
```

Expected:

```text
404
```

### Quantity is zero

```json
{
    "product_id": 1,
    "quantity": 0
}
```

Expected:

```text
400
```

### Quantity is negative

```json
{
    "product_id": 1,
    "quantity": -5
}
```

Expected:

```text
400
```

### Insufficient stock

If:

```text
stock = 5
```

Request:

```text
quantity = 10
```

Expected:

```text
400 Insufficient stock
```

### Low stock

If:

```text
stock = 8
threshold = 10
```

Product should appear in:

```text
GET /inventory/low-stock
```

---

# 25. Important Database Concept: Transaction

The sale operation involves two database changes:

```text
1. Reduce product stock
2. Create sale record
```

These should be treated as one transaction.

Example:

```text
Reduce stock
     +
Create sale
```

If something fails before commit:

```text
ROLLBACK
```

so you don't end up with inconsistent data.

Desired flow:

```text
BEGIN
   ↓
Check stock
   ↓
Reduce stock
   ↓
Create sale
   ↓
COMMIT
```

If an error occurs:

```text
ROLLBACK
```

---

# 26. Important Improvement: Concurrency

Later, learn why this can be dangerous:

```text
Stock = 1
```

Two customers purchase at almost the same time.

Request A:

```text
Buy 1
```

Request B:

```text
Buy 1
```

If both requests read:

```text
Stock = 1
```

you could accidentally sell two items when only one exists.

For the first version, understand the problem.

For the advanced version, use proper PostgreSQL transaction/row-locking or an atomic stock update.

This should be an advanced stage, not your first implementation.

---

# 27. Suggested Development Phases

## Phase 1 — Setup

Learn:

```text
FastAPI
Supabase
PostgreSQL
SQLAlchemy
Environment variables
```

Goal:

```text
FastAPI → Supabase
```

---

## Phase 2 — Category CRUD

Build:

```text
POST /categories
GET /categories
GET /categories/{id}
PUT /categories/{id}
DELETE /categories/{id}
```

Goal:

Understand CRUD.

---

## Phase 3 — Product CRUD

Build:

```text
POST /products
GET /products
GET /products/{id}
PUT /products/{id}
DELETE /products/{id}
```

Goal:

Understand:

```text
Foreign key
Category → Products
```

---

## Phase 4 — Inventory

Build:

```text
GET /inventory
POST /inventory/{id}/add
GET /inventory/low-stock
```

Goal:

Understand stock management.

---

## Phase 5 — Sales

Build:

```text
POST /sales
GET /sales
```

Most important logic:

```text
sale quantity
      ↓
check stock
      ↓
reduce stock
      ↓
create sale
```

---

## Phase 6 — Validation

Handle:

```text
Invalid product
Invalid category
Negative quantity
Zero quantity
Insufficient stock
Negative price
Duplicate category
Duplicate product
```

---

## Phase 7 — Advanced Features

After the basic project works, add:

```text
Authentication
Users
Admin role
Supplier management
Purchase orders
Stock movement history
Sales reports
Top-selling products
Daily sales
Monthly sales
Low-stock alerts
Pagination
Search
Filtering
Sorting
```

---

# 28. Final Architecture

Your final beginner version should look like:

```text
                    Client
                      |
                      ↓
                  FastAPI
                      |
          +-----------+-----------+
          |           |           |
          ↓           ↓           ↓
      Categories   Products      Sales
          |           |           |
          +-----------+-----------+
                      |
                      ↓
                 Service Layer
                      |
                      ↓
                  SQLAlchemy
                      |
                      ↓
             PostgreSQL / Supabase
```

---

# 29. Features You Should Eventually Have

```text
CATEGORY
--------
Create category
Update category
Delete category
List categories


PRODUCT
-------
Create product
Update product
Delete product
List products
Filter by category
Search product


INVENTORY
---------
View stock
Add stock
Reduce stock
Low stock detection


SALES
-----
Create sale
View sales
View sale details
Calculate total
Automatically reduce stock


REPORTS
-------
Daily sales
Monthly sales
Top products
Low-stock products
Total inventory value
```

---

# 30. Learning Objectives

By completing this project, you should understand:

### Backend

```text
What is an API?
What is FastAPI?
What is a router?
What is a service layer?
What is dependency injection?
```

### Database

```text
What is PostgreSQL?
What is Supabase?
What is a table?
Primary key
Foreign key
One-to-many relationship
Transactions
```

### SQLAlchemy

```text
Engine
Session
Base
Model
Query
Commit
Rollback
Relationship
```

### API

```text
GET
POST
PUT
DELETE
HTTP status codes
Request body
Path parameters
Query parameters
```

### Business Logic

```text
Stock management
Sales
Inventory
Validation
Transactions
```

---

# 31. Most Important Rule For Building This Project

Do NOT copy the entire project from ChatGPT and paste it at once.

Build it step-by-step.

Recommended order:

```text
1. Create Supabase database
        ↓
2. Connect FastAPI to Supabase
        ↓
3. Create Category model
        ↓
4. Create Category APIs
        ↓
5. Test Category CRUD
        ↓
6. Create Product model
        ↓
7. Create Product APIs
        ↓
8. Test Product CRUD
        ↓
9. Create Sale model
        ↓
10. Build sale logic
        ↓
11. Automatically reduce stock
        ↓
12. Add low-stock logic
        ↓
13. Add validation
        ↓
14. Add transactions
        ↓
15. Add reports
```

The **core project milestone** is:

```text
Create Product
      ↓
Stock = 100
      ↓
Customer buys 5
      ↓
POST /sales
      ↓
Stock automatically becomes 95
      ↓
Sale stored in database
```

Once you can build this flow yourself and explain why every line of code exists, you will have a strong practical understanding of a real backend CRUD + business-logic project.
