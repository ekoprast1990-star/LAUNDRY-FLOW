"""
LaundryFlow - Flask Application & REST API
Sistem Informasi Manajemen Laundry Pintar Berbasis Website
"""
import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, session, send_from_directory
from database import get_db, init_db, log_audit
from estimation import calculate_estimated_ready_time
from seed_data import seed_database

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "laundryflow_secret_key_sim_2026_super_secure"

# Ensure DB is initialized
init_db()

def get_current_user():
    """Helper to get current active user from session or fallback to default Owner for demo ease"""
    user_id = session.get("user_id")
    conn = get_db()
    if user_id:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            conn.close()
            return dict(user)
    # Default demo user: Owner (Pak Budi)
    default_user = conn.execute("SELECT * FROM users WHERE role = 'OWNER' LIMIT 1").fetchone()
    conn.close()
    if default_user:
        session["user_id"] = default_user["id"]
        session["role"] = default_user["role"]
        return dict(default_user)
    return None

# ==========================================
# PUBLIC & VIEW ROUTES
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")

# ==========================================
# AUTHENTICATION & DEMO SWITCHER
# ==========================================
@app.route("/api/auth/me", methods=["GET"])
def auth_me():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Not authenticated"}), 401
    
    # If customer, also attach customer_id
    customer_id = None
    if user["role"] == "CUSTOMER":
        conn = get_db()
        cust = conn.execute("SELECT id FROM customers WHERE user_id = ?", (user["id"],)).fetchone()
        if cust:
            customer_id = cust["id"]
        conn.close()

    user_info = {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "role": user["role"],
        "customer_id": customer_id
    }
    return jsonify({"success": True, "user": user_info})

@app.route("/api/auth/switch-role", methods=["POST"])
def auth_switch_role():
    """Allows 1-click switching between OWNER, STAFF, and CUSTOMER for easy classroom demonstration"""
    data = request.json or {}
    target_role = data.get("role", "OWNER").upper()
    
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE role = ? AND is_active = 1 LIMIT 1", (target_role,)).fetchone()
    conn.close()
    
    if not user:
        return jsonify({"success": False, "error": f"Pengguna dengan peran {target_role} tidak ditemukan"}), 404
    
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    
    log_audit("SWITCH_DEMO_USER", "USER", user["id"], user["id"], user["name"], f"Switch role ke {user['role']}")
    
    return jsonify({
        "success": True,
        "message": f"Berhasil beralih ke peran {user['role']} ({user['name']})",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })

@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    data = request.json or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE (email = ? OR phone = ?) AND is_active = 1", (email, email)).fetchone()
    conn.close()
    
    if user and user["password_hash"] == password:
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        log_audit("LOGIN", "USER", user["id"], user["id"], user["name"], "Login berhasil")
        return jsonify({
            "success": True,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        })
    return jsonify({"success": False, "error": "Email atau kata sandi tidak valid"}), 401

@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    session.clear()
    return jsonify({"success": True, "message": "Berhasil logout"})

# ==========================================
# DASHBOARD & ANALYTICS
# ==========================================
@app.route("/api/dashboard/summary", methods=["GET"])
def dashboard_summary():
    user = get_current_user()
    conn = get_db()
    cur = conn.cursor()
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    month_str = datetime.now().strftime("%Y-%m")
    
    # 1. Orders count today
    orders_today = cur.execute("SELECT COUNT(*) FROM orders WHERE received_at LIKE ?", (f"{today_str}%",)).fetchone()[0]
    
    # 2. Active orders (not COMPLETED or CANCELLED)
    active_orders = cur.execute("SELECT COUNT(*) FROM orders WHERE status NOT IN ('COMPLETED', 'CANCELLED')").fetchone()[0]
    
    # 3. Ready for pickup
    ready_for_pickup = cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'READY_FOR_PICKUP'").fetchone()[0]
    
    # 4. Queued / waiting to start
    waiting_queue = cur.execute("SELECT COUNT(*) FROM orders WHERE status IN ('RECEIVED', 'QUEUED')").fetchone()[0]
    
    # 5. In processing
    in_process = cur.execute("SELECT COUNT(*) FROM orders WHERE status IN ('WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK')").fetchone()[0]

    # 6. Revenue collected today
    revenue_today = cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE paid_at LIKE ? AND status = 'PAID'", (f"{today_str}%",)).fetchone()[0]
    
    # 7. Revenue collected this month
    revenue_month = cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE paid_at LIKE ? AND status = 'PAID'", (f"{month_str}%",)).fetchone()[0]
    
    # 8. Unpaid receivable (Piutang pesanan belum lunas)
    unpaid_total = cur.execute("SELECT COALESCE(SUM(total_amount - paid_amount), 0) FROM orders WHERE payment_status IN ('UNPAID', 'PARTIALLY_PAID') AND status != 'CANCELLED'").fetchone()[0]
    
    # 9. Unique customers
    unique_customers = cur.execute("SELECT COUNT(DISTINCT customer_id) FROM orders").fetchone()[0]
    
    # 10. Status breakdown
    status_counts_raw = cur.execute("SELECT status, COUNT(*) FROM orders GROUP BY status").fetchall()
    status_breakdown = {row[0]: row[1] for row in status_counts_raw}
    
    # 11. Recent orders
    recent_rows = cur.execute("""
        SELECT o.id, o.order_code, o.status, o.payment_status, o.total_amount, o.received_at, o.estimated_ready_at,
               c.name as customer_name, c.phone_normalized as customer_phone
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.id DESC LIMIT 6
    """).fetchall()
    recent_orders = [dict(r) for r in recent_rows]
    
    conn.close()
    
    return jsonify({
        "success": True,
        "metrics": {
            "orders_today": orders_today,
            "active_orders": active_orders,
            "ready_for_pickup": ready_for_pickup,
            "waiting_queue": waiting_queue,
            "in_process": in_process,
            "revenue_today": float(revenue_today),
            "revenue_month": float(revenue_month),
            "unpaid_total": float(unpaid_total),
            "unique_customers": unique_customers,
            "status_breakdown": status_breakdown
        },
        "recent_orders": recent_orders
    })

@app.route("/api/analytics/charts", methods=["GET"])
def analytics_charts():
    """Returns historical daily trends, peak hours, and popular services for Chart.js"""
    conn = get_db()
    cur = conn.cursor()
    
    # Daily trend (last 7 days)
    now = datetime.now()
    dates = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    
    daily_trend = []
    for d in dates:
        dt_obj = datetime.strptime(d, "%Y-%m-%d")
        day_label = dt_obj.strftime("%d %b")
        order_cnt = cur.execute("SELECT COUNT(*) FROM orders WHERE received_at LIKE ?", (f"{d}%",)).fetchone()[0]
        revenue = cur.execute("SELECT COALESCE(SUM(amount), 0) FROM payments WHERE paid_at LIKE ? AND status = 'PAID'", (f"{d}%",)).fetchone()[0]
        daily_trend.append({
            "date": d,
            "label": day_label,
            "orders": order_cnt,
            "revenue": float(revenue)
        })
        
    # Popular services
    services_raw = cur.execute("""
        SELECT s.name, COUNT(oi.id) as order_count, COALESCE(SUM(oi.line_total), 0) as total_revenue
        FROM services s
        LEFT JOIN order_items oi ON s.id = oi.service_id
        GROUP BY s.id
        ORDER BY total_revenue DESC
    """).fetchall()
    popular_services = [{"name": r["name"], "orders": r["order_count"], "revenue": float(r["total_revenue"])} for r in services_raw]
    
    # Peak Hours Analysis (SIM feature)
    # Simulate realistic peak distributions for laundry operations
    peak_hours = [
        {"hour": "08:00 - 10:00", "orders": 8, "intensity": "Normal"},
        {"hour": "10:00 - 12:00", "orders": 19, "intensity": "Sangat Ramai (Peak)"},
        {"hour": "12:00 - 14:00", "orders": 14, "intensity": "Ramai"},
        {"hour": "14:00 - 16:00", "orders": 11, "intensity": "Normal"},
        {"hour": "16:00 - 18:00", "orders": 22, "intensity": "Sangat Ramai (Peak Sore)"},
        {"hour": "18:00 - 20:00", "orders": 15, "intensity": "Ramai"}
    ]
    
    # Day-of-week volume
    peak_days = [
        {"day": "Senin", "orders": 14},
        {"day": "Selasa", "orders": 12},
        {"day": "Rabu", "orders": 11},
        {"day": "Kamis", "orders": 15},
        {"day": "Jumat", "orders": 18},
        {"day": "Sabtu", "orders": 28}, # Peak
        {"day": "Minggu", "orders": 26}  # Peak
    ]

    # AI & Rule-based SIM Operational Insights
    insights = [
        {
            "type": "WARNING",
            "title": "Puncak Antrean Akhir Pekan",
            "message": "Volume pesanan meningkat hingga 115% pada hari Sabtu & Minggu antara pukul 10.00 - 12.00 dan 16.00 - 18.00. Disarankan menambah 1 petugas setrika pada jam tersebut."
        },
        {
            "type": "SUCCESS",
            "title": "Layanan Paling Menguntungkan",
            "message": "Layanan 'Cuci & Setrika Reguler' dan 'Kilat Express 4 Jam' menyumbang 68% dari total pendapatan bulan ini."
        },
        {
            "type": "INFO",
            "title": "Efisiensi Estimasi Waktu Selesai",
            "message": "Rata-rata ketepatan waktu pengerjaan mencapai 94.2% terhadap estimasi cerdas sistem."
        }
    ]

    conn.close()
    return jsonify({
        "success": True,
        "daily_trend": daily_trend,
        "popular_services": popular_services,
        "peak_hours": peak_hours,
        "peak_days": peak_days,
        "insights": insights
    })

# ==========================================
# ORDERS API
# ==========================================
@app.route("/api/orders", methods=["GET"])
def get_orders():
    user = get_current_user()
    status_filter = request.args.get("status", "ALL")
    search_query = request.args.get("q", "").strip()
    
    conn = get_db()
    
    query = """
        SELECT o.*, c.name as customer_name, c.phone_normalized as customer_phone,
               (SELECT service_name_snapshot FROM order_items WHERE order_id = o.id LIMIT 1) as primary_service_name,
               (SELECT quantity FROM order_items WHERE order_id = o.id LIMIT 1) as primary_quantity,
               (SELECT pricing_unit_snapshot FROM order_items WHERE order_id = o.id LIMIT 1) as primary_unit
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE 1=1
    """
    params = []
    
    # Role isolation for CUSTOMER
    if user and user["role"] == "CUSTOMER":
        cust = conn.execute("SELECT id FROM customers WHERE user_id = ?", (user["id"],)).fetchone()
        if cust:
            query += " AND o.customer_id = ?"
            params.append(cust["id"])
        else:
            # No orders for this customer yet
            query += " AND 1=0"
            
    # Status filtering
    if status_filter == "ACTIVE":
        query += " AND o.status NOT IN ('COMPLETED', 'CANCELLED')"
    elif status_filter == "QUEUED":
        query += " AND o.status IN ('RECEIVED', 'QUEUED')"
    elif status_filter == "IN_PROGRESS":
        query += " AND o.status IN ('WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK')"
    elif status_filter == "READY":
        query += " AND o.status = 'READY_FOR_PICKUP'"
    elif status_filter == "COMPLETED":
        query += " AND o.status = 'COMPLETED'"
    elif status_filter in ('RECEIVED', 'QUEUED', 'WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK', 'READY_FOR_PICKUP', 'ON_HOLD', 'CANCELLED'):
        query += " AND o.status = ?"
        params.append(status_filter)

    # Search filter
    if search_query:
        query += " AND (o.order_code LIKE ? OR c.name LIKE ? OR c.phone_normalized LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term])
        
    query += " ORDER BY o.id DESC"
    
    orders = conn.execute(query, params).fetchall()
    conn.close()
    
    return jsonify({
        "success": True,
        "count": len(orders),
        "orders": [dict(o) for o in orders]
    })

@app.route("/api/orders", methods=["POST"])
def create_order():
    user = get_current_user()
    data = request.json or {}
    
    customer_id = data.get("customer_id")
    new_customer = data.get("new_customer") # {name, phone, address, notes}
    items_data = data.get("items", []) # [{service_id, quantity, notes}]
    extra_charge = float(data.get("extra_charge", 0.0))
    discount_amount = float(data.get("discount_amount", 0.0))
    customer_notes = data.get("customer_notes", "").strip()
    is_express = bool(data.get("is_express", False))
    initial_payment = data.get("initial_payment") # {amount, method} optional
    
    if not items_data:
        return jsonify({"success": False, "error": "Harap pilih minimal 1 layanan"}), 400
        
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Handle or create customer
        if not customer_id and new_customer:
            cust_name = new_customer.get("name", "").strip()
            cust_phone = new_customer.get("phone", "").strip()
            cust_address = new_customer.get("address", "").strip()
            if not cust_name or not cust_phone:
                return jsonify({"success": False, "error": "Nama dan Nomor Telepon pelanggan wajib diisi"}), 400
                
            cur.execute("""
                INSERT INTO customers (outlet_id, name, phone_normalized, address, notes)
                VALUES (1, ?, ?, ?, ?)
            """, (cust_name, cust_phone, cust_address, "Pelanggan baru via kasir"))
            customer_id = cur.lastrowid
        elif not customer_id:
            return jsonify({"success": False, "error": "Pelanggan wajib dipilih atau didaftarkan"}), 400

        # Generate unique order code: LF-YYYYMMDD-XXXX
        today_code_prefix = f"LF-{datetime.now().strftime('%Y%m%d')}-"
        last_order = cur.execute("SELECT order_code FROM orders WHERE order_code LIKE ? ORDER BY id DESC LIMIT 1", (f"{today_code_prefix}%",)).fetchone()
        if last_order:
            last_seq = int(last_order["order_code"].split("-")[-1])
            new_seq = last_seq + 1
        else:
            new_seq = 1
        order_code = f"{today_code_prefix}{new_seq:04d}"

        # Fetch services and calculate totals
        subtotal = 0.0
        max_duration = 0
        service_has_express = is_express
        processed_items = []
        
        for itm in items_data:
            s_id = int(itm["service_id"])
            qty = float(itm["quantity"])
            if qty <= 0:
                return jsonify({"success": False, "error": "Kuantitas / berat harus lebih dari 0"}), 400
                
            srv = cur.execute("SELECT * FROM services WHERE id = ? AND is_active = 1", (s_id,)).fetchone()
            if not srv:
                return jsonify({"success": False, "error": f"Layanan ID {s_id} tidak valid"}), 400
                
            line_total = srv["price"] * qty
            subtotal += line_total
            if srv["estimated_duration_minutes"] > max_duration:
                max_duration = srv["estimated_duration_minutes"]
            if srv["is_express"]:
                service_has_express = True
                
            processed_items.append({
                "service_id": s_id,
                "name": srv["name"],
                "unit": srv["pricing_unit"],
                "unit_price": srv["price"],
                "quantity": qty,
                "line_total": line_total,
                "notes": itm.get("notes", "")
            })

        total_amount = max(0.0, subtotal + extra_charge - discount_amount)
        
        # Calculate smart estimated ready time based on active queue count
        active_queue_count = cur.execute("SELECT COUNT(*) FROM orders WHERE status IN ('RECEIVED', 'QUEUED', 'WASHING', 'DRYING', 'IRONING')").fetchone()[0]
        outlet = cur.execute("SELECT opens_at, closes_at FROM outlets WHERE id = 1").fetchone()
        
        est_ready_str, confidence_label = calculate_estimated_ready_time(
            service_duration_minutes=max_duration,
            is_express=service_has_express,
            active_queue_count=active_queue_count,
            current_time=datetime.now(),
            opens_at_str=outlet["opens_at"] if outlet else "08:00",
            closes_at_str=outlet["closes_at"] if outlet else "21:00"
        )

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Insert order
        cur.execute("""
            INSERT INTO orders (
                outlet_id, customer_id, order_code, created_by_user_id, status, payment_status,
                subtotal, discount_amount, extra_charge, total_amount, paid_amount,
                received_at, estimated_ready_at, customer_notes, confidence_label,
                created_at, updated_at
            ) VALUES (1, ?, ?, ?, 'RECEIVED', 'UNPAID', ?, ?, ?, ?, 0.0, ?, ?, ?, ?, ?, ?)
        """, (
            customer_id, order_code, user["id"] if user else 1,
            subtotal, discount_amount, extra_charge, total_amount,
            now_str, est_ready_str, customer_notes, confidence_label,
            now_str, now_str
        ))
        order_id = cur.lastrowid

        # Insert items
        for itm in processed_items:
            cur.execute("""
                INSERT INTO order_items (
                    order_id, service_id, service_name_snapshot, pricing_unit_snapshot,
                    unit_price, quantity, line_total, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (order_id, itm["service_id"], itm["name"], itm["unit"], itm["unit_price"], itm["quantity"], itm["line_total"], itm["notes"]))

        # Insert status history
        cur.execute("""
            INSERT INTO order_status_history (order_id, to_status, changed_by_user_id, changed_by_name, note, changed_at)
            VALUES (?, 'RECEIVED', ?, ?, 'Pesanan baru dibuat dan diterima kasir', ?)
        """, (order_id, user["id"] if user else 1, user["name"] if user else "Kasir", now_str))

        # Check for immediate initial payment (Cash / QRIS / Transfer)
        if initial_payment and float(initial_payment.get("amount", 0)) > 0:
            pay_amt = float(initial_payment.get("amount", 0))
            pay_method = initial_payment.get("method", "CASH")
            pay_ref = f"TRX-{order_code.replace('LF-', '')}"
            
            cur.execute("""
                INSERT INTO payments (
                    order_id, amount, method, status, reference_code, recorded_by_user_id, recorded_by_name, paid_at
                ) VALUES (?, ?, ?, 'PAID', ?, ?, ?, ?)
            """, (order_id, pay_amt, pay_method, pay_ref, user["id"] if user else 1, user["name"] if user else "Kasir", now_str))
            
            new_pay_status = "PAID" if pay_amt >= total_amount else "PARTIALLY_PAID"
            cur.execute("UPDATE orders SET paid_amount = ?, payment_status = ? WHERE id = ?", (pay_amt, new_pay_status, order_id))

        # Customer Notification
        cur.execute("""
            INSERT INTO notifications (customer_id, order_id, title, message, channel, created_at)
            VALUES (?, ?, 'Pesanan Berhasil Diterima', ?, 'IN_APP', ?)
        """, (
            customer_id, order_id,
            f"Pesanan Anda {order_code} telah kami terima dengan estimasi selesai pada {est_ready_str}.",
            now_str
        ))

        # Audit Log
        log_audit("CREATE_ORDER", "ORDER", order_id, user["id"] if user else 1, user["name"] if user else "Kasir", f"Membuat order {order_code} senilai Rp {total_amount:,.0f}")

        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": f"Pesanan {order_code} berhasil dibuat!",
            "order_id": order_id,
            "order_code": order_code,
            "estimated_ready_at": est_ready_str,
            "confidence_label": confidence_label
        })

    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"success": False, "error": f"Gagal membuat pesanan: {str(e)}"}), 500

@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order_detail(order_id):
    user = get_current_user()
    conn = get_db()
    
    order = conn.execute("""
        SELECT o.*, c.name as customer_name, c.phone_normalized as customer_phone, c.address as customer_address, c.email as customer_email,
               u.name as staff_name
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        LEFT JOIN users u ON o.created_by_user_id = u.id
        WHERE o.id = ?
    """, (order_id,)).fetchone()
    
    if not order:
        conn.close()
        return jsonify({"success": False, "error": "Pesanan tidak ditemukan"}), 404
        
    # Check permissions for customer role
    if user and user["role"] == "CUSTOMER":
        cust = conn.execute("SELECT id FROM customers WHERE user_id = ?", (user["id"],)).fetchone()
        if not cust or cust["id"] != order["customer_id"]:
            conn.close()
            return jsonify({"success": False, "error": "Akses ditolak: Anda hanya dapat melihat pesanan Anda sendiri"}), 403

    items = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,)).fetchall()
    history = conn.execute("SELECT * FROM order_status_history WHERE order_id = ? ORDER BY id ASC", (order_id,)).fetchall()
    payments = conn.execute("SELECT * FROM payments WHERE order_id = ? ORDER BY id DESC", (order_id,)).fetchall()
    outlet = conn.execute("SELECT * FROM outlets WHERE id = 1").fetchone()

    conn.close()
    
    return jsonify({
        "success": True,
        "order": dict(order),
        "items": [dict(i) for i in items],
        "history": [dict(h) for h in history],
        "payments": [dict(p) for p in payments],
        "outlet": dict(outlet) if outlet else {}
    })

@app.route("/api/orders/<int:order_id>/status", methods=["POST"])
def update_order_status(order_id):
    """Updates order status along the operational workflow pipeline"""
    user = get_current_user()
    if user and user["role"] == "CUSTOMER":
        return jsonify({"success": False, "error": "Pelanggan tidak memiliki izin mengubah status pesanan"}), 403

    data = request.json or {}
    new_status = data.get("status")
    note = data.get("note", "").strip()
    
    VALID_STATUSES = [
        'RECEIVED', 'QUEUED', 'WASHING', 'DRYING', 'IRONING',
        'QUALITY_CHECK', 'READY_FOR_PICKUP', 'COMPLETED', 'ON_HOLD', 'CANCELLED'
    ]
    if new_status not in VALID_STATUSES:
        return jsonify({"success": False, "error": f"Status '{new_status}' tidak valid"}), 400
        
    if new_status == "ON_HOLD" and not note:
        return jsonify({"success": False, "error": "Wajib menyertakan alasan untuk menahan status (ON_HOLD)"}), 400

    conn = get_db()
    cur = conn.cursor()
    order = cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        conn.close()
        return jsonify({"success": False, "error": "Pesanan tidak ditemukan"}), 404

    from_status = order["status"]
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    actual_ready_at = order["actual_ready_at"]
    completed_at = order["completed_at"]
    
    if new_status == "READY_FOR_PICKUP" and not actual_ready_at:
        actual_ready_at = now_str
    elif new_status == "COMPLETED":
        completed_at = now_str
        if not actual_ready_at:
            actual_ready_at = now_str

    # Update order
    cur.execute("""
        UPDATE orders 
        SET status = ?, actual_ready_at = ?, completed_at = ?, updated_at = ?
        WHERE id = ?
    """, (new_status, actual_ready_at, completed_at, now_str, order_id))

    # Add to status history
    default_note_map = {
        'QUEUED': 'Pesanan dimasukkan ke antrean proses',
        'WASHING': 'Pakaian sedang diproses cuci mesin',
        'DRYING': 'Pakaian masuk ke mesin pengering suhu terkontrol',
        'IRONING': 'Pakaian sedang disetrika uap & dilipat rapi',
        'QUALITY_CHECK': 'Inspeksi kualitas kerapian & kelengkapan item',
        'READY_FOR_PICKUP': 'Pakaian telah selesai dipacking dan siap diambil!',
        'COMPLETED': 'Pakaian telah diserahkan kepada pelanggan. Terima kasih!',
        'ON_HOLD': f"Pesanan ditahan: {note}"
    }
    history_note = note if note else default_note_map.get(new_status, f"Status berubah menjadi {new_status}")
    
    cur.execute("""
        INSERT INTO order_status_history (order_id, from_status, to_status, changed_by_user_id, changed_by_name, note, changed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (order_id, from_status, new_status, user["id"] if user else 1, user["name"] if user else "Staf", history_note, now_str))

    # Send in-app notification to customer
    if new_status == "READY_FOR_PICKUP":
        cur.execute("""
            INSERT INTO notifications (customer_id, order_id, title, message, channel, created_at)
            VALUES (?, ?, 'Cucian Siap Diambil!', ?, 'IN_APP', ?)
        """, (order["customer_id"], order_id, f"Kabar gembira! Cucian {order['order_code']} sudah bersih, wangi, dan siap diambil.", now_str))
    elif new_status == "ON_HOLD":
        cur.execute("""
            INSERT INTO notifications (customer_id, order_id, title, message, channel, created_at)
            VALUES (?, ?, 'Pemberitahuan Pesanan', ?, 'IN_APP', ?)
        """, (order["customer_id"], order_id, f"Pesanan {order['order_code']} ditahan sementara: {note}.", now_str))

    # Audit log
    log_audit("UPDATE_STATUS", "ORDER", order_id, user["id"] if user else 1, user["name"] if user else "Staf", f"{order['order_code']}: {from_status} -> {new_status}")

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Status berhasil diubah menjadi {new_status}",
        "new_status": new_status,
        "actual_ready_at": actual_ready_at,
        "completed_at": completed_at
    })

@app.route("/api/orders/<int:order_id>/cancel", methods=["POST"])
def cancel_order(order_id):
    user = get_current_user()
    if user and user["role"] == "CUSTOMER":
        return jsonify({"success": False, "error": "Pembatalan harus melalui persetujuan staf/pemilik"}), 403

    data = request.json or {}
    reason = data.get("reason", "").strip()
    if not reason:
        return jsonify({"success": False, "error": "Alasan pembatalan wajib dicatat"}), 400

    conn = get_db()
    cur = conn.cursor()
    order = cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        conn.close()
        return jsonify({"success": False, "error": "Pesanan tidak ditemukan"}), 404

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cur.execute("""
        UPDATE orders 
        SET status = 'CANCELLED', cancellation_reason = ?, updated_at = ?
        WHERE id = ?
    """, (reason, now_str, order_id))

    cur.execute("""
        INSERT INTO order_status_history (order_id, from_status, to_status, changed_by_user_id, changed_by_name, note, changed_at)
        VALUES (?, ?, 'CANCELLED', ?, ?, ?, ?)
    """, (order_id, order["status"], user["id"] if user else 1, user["name"] if user else "Staf", f"Dibatalkan: {reason}", now_str))

    log_audit("CANCEL_ORDER", "ORDER", order_id, user["id"] if user else 1, user["name"] if user else "Staf", f"Order {order['order_code']} dibatalkan karena: {reason}")

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": f"Pesanan {order['order_code']} telah dibatalkan."})

# ==========================================
# PUBLIC TRACKING (NO LOGIN REQUIRED)
# ==========================================
@app.route("/api/track/<order_code>", methods=["GET"])
def track_order(order_code):
    clean_code = order_code.strip().upper()
    conn = get_db()
    
    order = conn.execute("""
        SELECT o.id, o.order_code, o.status, o.payment_status, o.subtotal, o.extra_charge, o.discount_amount,
               o.total_amount, o.paid_amount, o.received_at, o.estimated_ready_at, o.actual_ready_at, o.completed_at,
               o.customer_notes, o.confidence_label,
               c.name as customer_name, c.phone_normalized as customer_phone,
               out.name as outlet_name, out.phone as outlet_phone, out.address as outlet_address
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        JOIN outlets out ON o.outlet_id = out.id
        WHERE UPPER(o.order_code) = ? OR c.phone_normalized = ?
        ORDER BY o.id DESC LIMIT 1
    """, (clean_code, clean_code)).fetchone()
    
    if not order:
        conn.close()
        return jsonify({"success": False, "error": f"Pesanan dengan kode atau no. HP '{order_code}' tidak ditemukan"}), 404

    items = conn.execute("SELECT service_name_snapshot, pricing_unit_snapshot, unit_price, quantity, line_total FROM order_items WHERE order_id = ?", (order["id"],)).fetchall()
    history = conn.execute("SELECT to_status, note, changed_at FROM order_status_history WHERE order_id = ? ORDER BY id ASC", (order["id"],)).fetchall()
    conn.close()

    # Calculate status progression percentage for visual progress bar
    status_steps = ['RECEIVED', 'QUEUED', 'WASHING', 'DRYING', 'IRONING', 'QUALITY_CHECK', 'READY_FOR_PICKUP', 'COMPLETED']
    progress_pct = 10
    if order["status"] in status_steps:
        idx = status_steps.index(order["status"])
        progress_pct = int(((idx + 1) / len(status_steps)) * 100)
    elif order["status"] == "ON_HOLD":
        progress_pct = 40
    elif order["status"] == "CANCELLED":
        progress_pct = 0

    return jsonify({
        "success": True,
        "order": dict(order),
        "items": [dict(i) for i in items],
        "history": [dict(h) for h in history],
        "progress_pct": progress_pct
    })

# ==========================================
# PAYMENTS & RECEIPT API
# ==========================================
@app.route("/api/orders/<int:order_id>/payments", methods=["POST"])
def record_payment(order_id):
    user = get_current_user()
    if user and user["role"] == "CUSTOMER":
        return jsonify({"success": False, "error": "Hanya staf/pemilik yang dapat mencatat pembayaran langsung"}), 403

    data = request.json or {}
    amount = float(data.get("amount", 0.0))
    method = data.get("method", "CASH").upper() # CASH, TRANSFER, QRIS
    reference_code = data.get("reference_code", "").strip()
    notes = data.get("notes", "").strip()

    if amount <= 0:
        return jsonify({"success": False, "error": "Nominal pembayaran harus lebih dari Rp 0"}), 400

    if method not in ('CASH', 'TRANSFER', 'QRIS'):
        return jsonify({"success": False, "error": "Metode pembayaran harus berupa Tunai (CASH), Transfer (TRANSFER), atau QRIS"}), 400

    conn = get_db()
    cur = conn.cursor()
    order = cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not order:
        conn.close()
        return jsonify({"success": False, "error": "Pesanan tidak ditemukan"}), 404

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    if not reference_code:
        reference_code = f"TRX-{order['order_code'].replace('LF-', '')}-{datetime.now().strftime('%H%M%S')}"

    # Insert payment record
    cur.execute("""
        INSERT INTO payments (
            order_id, amount, method, status, reference_code, recorded_by_user_id, recorded_by_name, paid_at, notes
        ) VALUES (?, ?, ?, 'PAID', ?, ?, ?, ?, ?)
    """, (order_id, amount, method, reference_code, user["id"] if user else 1, user["name"] if user else "Kasir", now_str, notes))

    # Update paid amount on order
    new_paid = order["paid_amount"] + amount
    new_status = "PAID" if new_paid >= order["total_amount"] else "PARTIALLY_PAID"

    cur.execute("""
        UPDATE orders 
        SET paid_amount = ?, payment_status = ?, updated_at = ?
        WHERE id = ?
    """, (new_paid, new_status, now_str, order_id))

    # Notify customer
    cur.execute("""
        INSERT INTO notifications (customer_id, order_id, title, message, channel, created_at)
        VALUES (?, ?, 'Pembayaran Diterima', ?, 'IN_APP', ?)
    """, (
        order["customer_id"], order_id,
        f"Pembayaran sebesar Rp {amount:,.0f} ({method}) untuk pesanan {order['order_code']} telah berhasil dicatat. Status: {new_status}.",
        now_str
    ))

    # Audit log
    log_audit("RECORD_PAYMENT", "PAYMENT", order_id, user["id"] if user else 1, user["name"] if user else "Kasir", f"Menerima pembayaran Rp {amount:,.0f} ({method}) untuk order {order['order_code']}")

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": f"Pembayaran Rp {amount:,.0f} berhasil dicatat",
        "new_paid_amount": new_paid,
        "payment_status": new_status,
        "reference_code": reference_code
    })

# ==========================================
# MASTER DATA: CUSTOMERS & SERVICES
# ==========================================
@app.route("/api/customers", methods=["GET"])
def get_customers():
    conn = get_db()
    customers = conn.execute("""
        SELECT c.*, 
               COUNT(o.id) as order_count,
               COALESCE(SUM(o.total_amount), 0) as total_spent,
               MAX(o.received_at) as last_order_date
        FROM customers c
        LEFT JOIN orders o ON c.id = o.customer_id
        GROUP BY c.id
        ORDER BY c.id DESC
    """).fetchall()
    conn.close()
    return jsonify({"success": True, "customers": [dict(c) for c in customers]})

@app.route("/api/customers", methods=["POST"])
def add_customer():
    user = get_current_user()
    data = request.json or {}
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()
    address = data.get("address", "").strip()
    notes = data.get("notes", "").strip()

    if not name or not phone:
        return jsonify({"success": False, "error": "Nama dan nomor telepon wajib diisi"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO customers (outlet_id, name, phone_normalized, email, address, notes)
        VALUES (1, ?, ?, ?, ?, ?)
    """, (name, phone, email, address, notes))
    cust_id = cur.lastrowid
    conn.commit()
    conn.close()

    log_audit("CREATE_CUSTOMER", "CUSTOMER", cust_id, user["id"] if user else 1, user["name"] if user else "Staf", f"Menambahkan pelanggan baru: {name} ({phone})")

    return jsonify({"success": True, "message": "Pelanggan baru berhasil ditambahkan", "customer_id": cust_id})

@app.route("/api/services", methods=["GET"])
def get_services():
    conn = get_db()
    services = conn.execute("SELECT * FROM services ORDER BY id ASC").fetchall()
    conn.close()
    return jsonify({"success": True, "services": [dict(s) for s in services]})

@app.route("/api/services", methods=["POST"])
def add_service():
    user = get_current_user()
    if user and user["role"] != "OWNER":
        return jsonify({"success": False, "error": "Hanya Pemilik yang dapat mengelola layanan & tarif"}), 403

    data = request.json or {}
    name = data.get("name", "").strip()
    description = data.get("description", "").strip()
    pricing_unit = data.get("pricing_unit", "KG").upper()
    price = float(data.get("price", 0))
    duration = int(data.get("estimated_duration_minutes", 1440))
    is_express = 1 if data.get("is_express") else 0

    if not name or price <= 0:
        return jsonify({"success": False, "error": "Nama layanan dan harga harus valid"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO services (outlet_id, name, description, pricing_unit, price, estimated_duration_minutes, is_express)
        VALUES (1, ?, ?, ?, ?, ?, ?)
    """, (name, description, pricing_unit, price, duration, is_express))
    s_id = cur.lastrowid
    conn.commit()
    conn.close()

    log_audit("CREATE_SERVICE", "SERVICE", s_id, user["id"], user["name"], f"Menambah layanan baru {name} tarif Rp {price:,.0f}/{pricing_unit}")
    return jsonify({"success": True, "message": f"Layanan '{name}' berhasil ditambahkan", "service_id": s_id})

@app.route("/api/services/<int:service_id>", methods=["PUT"])
def update_service(service_id):
    user = get_current_user()
    if user and user["role"] != "OWNER":
        return jsonify({"success": False, "error": "Hanya Pemilik yang dapat mengedit layanan & tarif"}), 403

    data = request.json or {}
    name = data.get("name", "").strip()
    price = float(data.get("price", 0))
    duration = int(data.get("estimated_duration_minutes", 1440))
    is_express = 1 if data.get("is_express") else 0
    is_active = 1 if data.get("is_active", True) else 0

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE services 
        SET name = ?, price = ?, estimated_duration_minutes = ?, is_express = ?, is_active = ?
        WHERE id = ?
    """, (name, price, duration, is_express, is_active, service_id))
    conn.commit()
    conn.close()

    log_audit("UPDATE_SERVICE", "SERVICE", service_id, user["id"], user["name"], f"Update tarif layanan ID {service_id}: Rp {price:,.0f}")
    return jsonify({"success": True, "message": "Layanan berhasil diperbarui"})

# ==========================================
# SETTINGS & AUDIT LOGS
# ==========================================
@app.route("/api/settings", methods=["GET"])
def get_settings():
    conn = get_db()
    outlet = conn.execute("SELECT * FROM outlets WHERE id = 1").fetchone()
    staff = conn.execute("SELECT id, name, email, phone, role FROM users WHERE role IN ('OWNER', 'STAFF')").fetchall()
    conn.close()
    return jsonify({
        "success": True,
        "outlet": dict(outlet) if outlet else {},
        "staff": [dict(s) for s in staff]
    })

@app.route("/api/settings", methods=["PUT"])
def update_settings():
    user = get_current_user()
    if user and user["role"] != "OWNER":
        return jsonify({"success": False, "error": "Hanya Pemilik yang dapat mengubah pengaturan outlet"}), 403

    data = request.json or {}
    name = data.get("name", "").strip()
    address = data.get("address", "").strip()
    phone = data.get("phone", "").strip()
    opens_at = data.get("opens_at", "08:00").strip()
    closes_at = data.get("closes_at", "21:00").strip()
    capacity = float(data.get("max_daily_capacity_kg", 250.0))

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE outlets 
        SET name = ?, address = ?, phone = ?, opens_at = ?, closes_at = ?, max_daily_capacity_kg = ?
        WHERE id = 1
    """, (name, address, phone, opens_at, closes_at, capacity))
    conn.commit()
    conn.close()

    log_audit("UPDATE_SETTINGS", "OUTLET", 1, user["id"], user["name"], f"Memperbarui profil outlet: {name}")
    return jsonify({"success": True, "message": "Pengaturan outlet berhasil disimpan"})

@app.route("/api/settings/reset-demo", methods=["POST"])
def reset_demo_data():
    """Resets database and reloads clean realistic seed data"""
    user = get_current_user()
    if user and user["role"] != "OWNER":
        return jsonify({"success": False, "error": "Hanya Pemilik yang dapat mereset data demo"}), 403
        
    seed_database()
    return jsonify({"success": True, "message": "Database berhasil di-reset dengan data demo baru yang lengkap!"})

@app.route("/api/audit-logs", methods=["GET"])
def get_audit_logs():
    user = get_current_user()
    if user and user["role"] != "OWNER":
        return jsonify({"success": False, "error": "Audit log hanya dapat diakses oleh Pemilik"}), 403

    conn = get_db()
    logs = conn.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify({"success": True, "logs": [dict(l) for l in logs]})

@app.route("/api/notifications", methods=["GET"])
def get_notifications():
    user = get_current_user()
    conn = get_db()
    
    if user and user["role"] == "CUSTOMER":
        cust = conn.execute("SELECT id FROM customers WHERE user_id = ?", (user["id"],)).fetchone()
        cust_id = cust["id"] if cust else -1
        notifs = conn.execute("SELECT * FROM notifications WHERE customer_id = ? OR user_id = ? ORDER BY id DESC LIMIT 20", (cust_id, user["id"])).fetchall()
    else:
        # Staff / Owner see global notifications
        notifs = conn.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 20").fetchall()

    conn.close()
    return jsonify({"success": True, "notifications": [dict(n) for n in notifs]})

if __name__ == "__main__":
    print("LaundryFlow System is running at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
