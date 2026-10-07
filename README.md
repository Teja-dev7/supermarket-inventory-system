# 🛒 Supermarket Inventory Management System (FastAPI & Supabase)

A complete, beginner-friendly backend and POS frontend for a **Supermarket Inventory Management System** built with **FastAPI**, **SQLAlchemy**, and **Supabase PostgreSQL**.

---

## 🌟 Key Features

- **Category Management**: Full CRUD operations for categories (`/categories`).
- **Product Management**: Create, update, search, and categorize products with price and stock levels (`/products`).
- **Real-time Sales Processing**: Atomic transactions that calculate bill totals, reduce product stock, and prevent negative inventory (`/sales`).
- **Inventory & Restocking**: Restock shipments, track live warehouse stock, and trigger low-stock alerts (`/inventory`).
- **Interactive POS Frontend**: Clean HTML/JS Point of Sale (POS) and Store Manager dashboard (`index.html`).
- **Interactive API Docs**: Built-in Swagger UI at `/docs`.

---

## 🏗️ Architecture

```text
Frontend (index.html / Postman)
       │
       ▼
FastAPI Routers (categories, products, inventory, sales)
       │
       ▼
Service Layer (Validation, Transaction, Stock Deduction)
       │
       ▼
SQLAlchemy ORM (Models & Sessions)
       │
       ▼
Supabase (Cloud PostgreSQL Database)
```

---

## 🚀 Getting Started

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/Teja-dev7/supermarket-inventory-system.git
cd supermarket-inventory-system
python -m venv venv
```

Activate virtual environment:
- **Windows**: `venv\Scripts\activate`
- **Linux/macOS**: `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Supabase Database
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your Supabase PostgreSQL connection string to `.env`:
```env
DATABASE_URL=postgresql+psycopg2://postgres.[REF]:[PASSWORD]@[HOST]:5432/postgres
```

### 3. Run the Backend Server
```bash
python -m uvicorn app.main:app --reload --port 8080
```

- **Swagger UI Docs**: [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
- **POS Web Interface**: Open `index.html` in your browser.

---

## 📂 Project Structure

```text
supermarket/
├── app/
│   ├── database.py       # SQLAlchemy engine & session dependency
│   ├── main.py           # FastAPI app entrypoint & table auto-creation
│   ├── models/           # Database tables (Category, Product, Sale)
│   ├── schemas/          # Pydantic validation schemas
│   ├── services/         # Business logic (sales & inventory)
│   └── routers/          # API endpoints
├── index.html            # Point of Sale & Manager Web UI
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── .gitignore            # Git exclusion rules
```
