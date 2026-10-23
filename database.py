"""
Database module for LaundryFlow
Provides SQLite connection management, table creation, and seed data initialization.
"""
import sqlite3
import os
from datetime import datetime, timedelta
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "laundryflow.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # 1. Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('OWNER', 'STAFF', 'CUSTOMER')),
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    """)

    # 2. Outlets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outlets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT NOT NULL UNIQUE,
        address TEXT NOT NULL,
        phone TEXT NOT NULL,
        timezone TEXT NOT NULL DEFAULT 'Asia/Jakarta',
        opens_at TEXT NOT NULL DEFAULT '08:00',
        closes_at TEXT NOT NULL DEFAULT '21:00',
        max_daily_capacity_kg REAL NOT NULL DEFAULT 200.0,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    """)

    # 3. Services (Katalog Layanan & Tarif)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        outlet_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        pricing_unit TEXT NOT NULL CHECK(pricing_unit IN ('KG', 'ITEM', 'PACKAGE', 'SERVICE')),
        price REAL NOT NULL,
        estimated_duration_minutes INTEGER NOT NULL,
        is_express INTEGER NOT NULL DEFAULT 0,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (outlet_id) REFERENCES outlets(id)
    );
    """)

    # 4. Customers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        outlet_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        phone_normalized TEXT NOT NULL,
        email TEXT,
        address TEXT,
        notes TEXT,
        is_active INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (outlet_id) REFERENCES outlets(id)
    );
    """)

    # 5. Orders
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        outlet_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        order_code TEXT NOT NULL UNIQUE,
        created_by_user_id INTEGER NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('RECEIVED', 'QUEUED', 'WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK', 'READY_FOR_PICKUP', 'COMPLETED', 'ON_HOLD', 'CANCELLED')),
        payment_status TEXT NOT NULL CHECK(payment_status IN ('UNPAID', 'PARTIALLY_PAID', 'PAID', 'REFUNDED', 'VOID')),
        subtotal REAL NOT NULL DEFAULT 0.0,
        discount_amount REAL NOT NULL DEFAULT 0.0,
        extra_charge REAL NOT NULL DEFAULT 0.0,
        total_amount REAL NOT NULL DEFAULT 0.0,
        paid_amount REAL NOT NULL DEFAULT 0.0,
        received_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        estimated_ready_at TEXT NOT NULL,
        actual_ready_at TEXT,
        completed_at TEXT,
        customer_notes TEXT,
        internal_notes TEXT,
        cancellation_reason TEXT,
        confidence_label TEXT DEFAULT 'Perkiraan Cerdas Berbasis Antrean',
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        updated_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (outlet_id) REFERENCES outlets(id),
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (created_by_user_id) REFERENCES users(id)
    );
    """)

    # 6. Order Items
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        service_id INTEGER NOT NULL,
        service_name_snapshot TEXT NOT NULL,
        pricing_unit_snapshot TEXT NOT NULL,
        unit_price REAL NOT NULL,
        quantity REAL NOT NULL,
        line_total REAL NOT NULL,
        notes TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (service_id) REFERENCES services(id)
    );
    """)

    # 7. Order Status History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_status_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        from_status TEXT,
        to_status TEXT NOT NULL,
        changed_by_user_id INTEGER,
        changed_by_name TEXT,
        note TEXT,
        changed_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (changed_by_user_id) REFERENCES users(id)
    );
    """)

    # 8. Payments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        method TEXT NOT NULL CHECK(method IN ('CASH', 'TRANSFER', 'QRIS')),
        status TEXT NOT NULL DEFAULT 'PAID' CHECK(status IN ('PAID', 'VOID', 'REFUNDED')),
        reference_code TEXT,
        recorded_by_user_id INTEGER NOT NULL,
        recorded_by_name TEXT,
        paid_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        notes TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (recorded_by_user_id) REFERENCES users(id)
    );
    """)

    # 9. Notifications
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        customer_id INTEGER,
        order_id INTEGER,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read INTEGER NOT NULL DEFAULT 0,
        channel TEXT NOT NULL DEFAULT 'IN_APP',
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (order_id) REFERENCES orders(id)
    );
    """)

    # 10. Audit Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        outlet_id INTEGER,
        actor_user_id INTEGER,
        actor_name TEXT,
        action TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id INTEGER,
        details TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    """)

    conn.commit()
    conn.close()

def log_audit(action, entity_type, entity_id=None, actor_user_id=None, actor_name=None, details=None, outlet_id=1):
    """Helper to record audit trail of important operations"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audit_logs (outlet_id, actor_user_id, actor_name, action, entity_type, entity_id, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            outlet_id,
            actor_user_id,
            actor_name or "System",
            action,
            entity_type,
            entity_id,
            json.dumps(details, ensure_ascii=False) if isinstance(details, (dict, list)) else (details or "")
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging audit: {e}")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
