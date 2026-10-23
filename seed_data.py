"""
Demo Seed Data for LaundryFlow
Generates realistic Indonesian operational data for demonstration in
Sistem Informasi Manajemen (SIM) coursework.
"""
from datetime import datetime, timedelta
import random
from database import get_db, init_db

def seed_database():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Clear existing demo data
    tables = ["audit_logs", "notifications", "payments", "order_status_history", "order_items", "orders", "customers", "services", "users", "outlets"]
    for table in tables:
        cursor.execute(f"DELETE FROM {table};")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}';")

    # 1. Outlet
    cursor.execute("""
        INSERT INTO outlets (id, name, code, address, phone, timezone, opens_at, closes_at, max_daily_capacity_kg)
        VALUES (1, 'LaundryFlow Smart Clean (Pusat Dipatiukur)', 'LF-BDG-01', 'Jl. Dipati Ukur No. 45, Coblong, Kota Bandung', '0812-3456-7890', 'Asia/Jakarta', '08:00', '21:00', 250.0);
    """)

    # 2. Users
    users_data = [
        (1, "Pak Budi Hartanto (Owner)", "owner@laundryflow.id", "081122334455", "owner123", "OWNER"),
        (2, "Siti Rahayu (Kasir & Operator)", "siti@laundryflow.id", "081234567891", "staff123", "STAFF"),
        (3, "Ahmad Fauzi (Operator Cuci)", "ahmad@laundryflow.id", "081234567892", "staff123", "STAFF"),
        (4, "Rian Pratama (Pelanggan)", "rian@gmail.com", "081298765432", "customer123", "CUSTOMER"),
        (5, "Dewi Lestari (Pelanggan)", "dewi@gmail.com", "085612345678", "customer123", "CUSTOMER"),
        (6, "Farhan Maulana (Pelanggan)", "farhan@gmail.com", "087811223344", "customer123", "CUSTOMER")
    ]
    cursor.executemany("""
        INSERT INTO users (id, name, email, phone, password_hash, role)
        VALUES (?, ?, ?, ?, ?, ?);
    """, users_data)

    # 3. Services
    services_data = [
        (1, 1, "Cuci & Setrika Reguler", "Layanan cuci bersih, wangi pelembut, dan setrika rapi lipat.", "KG", 8000, 1440, 0),
        (2, 1, "Cuci Kering Bersih", "Layanan cuci dan pengeringan mesin tanpa setrika.", "KG", 6000, 720, 0),
        (3, 1, "Setrika Saja Rapi", "Hanya setrika pakaian bersih agar halus dan siap pakai.", "KG", 5000, 720, 0),
        (4, 1, "Kilat Express 4 Jam", "Layanan kilat super prioritas cuci, kering, dan setrika selesai dalam 4 jam.", "KG", 16000, 240, 1),
        (5, 1, "Cuci Bed Cover Besar", "Pencucian mendalam untuk bed cover ukuran Queen / King.", "ITEM", 35000, 1440, 0),
        (6, 1, "Cuci Selimut / Boneka Tebal", "Pembersihan higienis khusus serat kain tebal dan boneka.", "ITEM", 25000, 1440, 0),
        (7, 1, "Cuci Sepatu Sneaker Premium", "Deep cleaning sepatu sneaker dengan sabun khusus non-detergen keras.", "ITEM", 30000, 2880, 0),
        (8, 1, "Cuci Jas / Blazer", "Dry clean perlakuan lembut untuk pakaian formal dan wol.", "ITEM", 35000, 1440, 0)
    ]
    cursor.executemany("""
        INSERT INTO services (id, outlet_id, name, description, pricing_unit, price, estimated_duration_minutes, is_express)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, services_data)

    # 4. Customers
    customers_data = [
        (1, 4, 1, "Rian Pratama", "081298765432", "rian@gmail.com", "Jl. Dago Asri No. 12, Bandung", "Pelanggan langganan, suka pewangi aroma Lavender."),
        (2, 5, 1, "Dewi Lestari", "085612345678", "dewi@gmail.com", "Kost Melati No. 4B, Dipatiukur", "Kemeja kerja mohon digantung."),
        (3, 6, 1, "Farhan Maulana", "087811223344", "farhan@gmail.com", "Apartemen Suites Dago Unit 802", "Baju putih selalu dipisah ya."),
        (4, None, 1, "Ibu Linda Kusuma", "081344556677", "linda.k@yahoo.com", "Jl. Cisitu Indah No. 19", "Bed cover mohon dipacking plastik tebal."),
        (5, None, 1, "Mas Dimas Anggara", "082199887766", "dimas.ang@gmail.com", "Jl. Sekeloa Timur No. 3", "Layanan express untuk seragam kantor."),
        (6, None, 1, "Mbak Anisa Putri", "081900112233", "anisa.p@gmail.com", "Jl. Teuku Umar No. 22", "Pewangi aroma Lily.")
    ]
    cursor.executemany("""
        INSERT INTO customers (id, user_id, outlet_id, name, phone_normalized, email, address, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, customers_data)

    now = datetime.now()
    
    # 5. Orders (Historical + Active orders)
    # Order definitions:
    # (code, cust_id, service_id, qty, status, pay_status, days_ago, hours_offset, extra, notes)
    order_specs = [
        # COMPLETED historical orders (from 1 to 7 days ago)
        ("LF-20261018-0001", 1, 1, 5.0, "COMPLETED", "PAID", 6, 2, 0, "Baju kuliah harian", "CASH"),
        ("LF-20261018-0002", 2, 2, 4.0, "COMPLETED", "PAID", 6, 4, 0, "Pakaian santai", "QRIS"),
        ("LF-20261019-0001", 3, 4, 3.5, "COMPLETED", "PAID", 5, 1, 5000, "Express seragam kerja", "TRANSFER"),
        ("LF-20261019-0002", 4, 5, 2.0, "COMPLETED", "PAID", 5, 3, 0, "Bed cover king size", "CASH"),
        ("LF-20261020-0001", 5, 1, 6.2, "COMPLETED", "PAID", 4, 2, 0, "Pakaian mix katun", "QRIS"),
        ("LF-20261020-0002", 6, 3, 4.5, "COMPLETED", "PAID", 4, 5, 0, "Setrika kemeja batik", "CASH"),
        ("LF-20261021-0001", 1, 7, 2.0, "COMPLETED", "PAID", 3, 1, 0, "Sepatu lari Nike & Adidas", "TRANSFER"),
        ("LF-20261021-0002", 2, 1, 5.5, "COMPLETED", "PAID", 3, 4, 0, "Cuci reguler biasa", "QRIS"),
        ("LF-20261022-0001", 3, 8, 2.0, "COMPLETED", "PAID", 2, 2, 0, "Jas wisuda hitam", "CASH"),
        ("LF-20261022-0002", 4, 1, 7.0, "COMPLETED", "PAID", 2, 6, 0, "Laundry keluarga", "TRANSFER"),

        # ACTIVE ORDERS (Today & Yesterday)
        # 11. Ready for pickup
        ("LF-20261023-0001", 1, 1, 4.5, "READY_FOR_PICKUP", "PAID", 1, 1, 0, "Pewangi Lavender, tolong dipisah.", "QRIS"),
        ("LF-20261023-0002", 2, 4, 3.0, "READY_FOR_PICKUP", "PARTIALLY_PAID", 1, 3, 5000, "Express butuh cepat sore.", "CASH"),

        # 13. Quality Check
        ("LF-20261023-0003", 3, 1, 6.0, "QUALITY_CHECK", "PAID", 1, 4, 0, "Kemeja kerja putih 3 pcs.", "TRANSFER"),

        # 14. Ironing
        ("LF-20261024-0001", 4, 1, 8.5, "IRONING", "UNPAID", 0, 2, 0, "Pakaian seragam sekolah & kantor.", None),

        # 15. Drying
        ("LF-20261024-0002", 5, 2, 5.0, "DRYING", "PAID", 0, 3, 0, "Handuk & sprei.", "QRIS"),

        # 16. Washing
        ("LF-20261024-0003", 6, 1, 4.0, "WASHING", "UNPAID", 0, 4, 0, "Celana jeans 3 pcs tolong hati-hati luntur.", None),

        # 17. Queued
        ("LF-20261024-0004", 1, 4, 2.5, "QUEUED", "PAID", 0, 5, 5000, "Express celana kerja besok pagi.", "QRIS"),

        # 18. Received (Just came in)
        ("LF-20261024-0005", 2, 5, 1.0, "RECEIVED", "UNPAID", 0, 6, 0, "Bed cover queen size motif bunga.", None),

        # 19. On Hold (Kendala teknis/pemberitahuan)
        ("LF-20261024-0006", 3, 7, 1.0, "ON_HOLD", "PAID", 0, 7, 0, "Sepatu kulit butuh konfirmasi warna semir.", "TRANSFER")
    ]

    service_map = {s[0]: s for s in services_data}

    for idx, (code, cust_id, s_id, qty, status, pay_status, days_ago, hours_offset, extra, notes, pay_method) in enumerate(order_specs, 1):
        srv = service_map[s_id]
        unit_price = srv[5]
        subtotal = unit_price * qty
        discount = 0.0
        extra_charge = float(extra)
        total = subtotal + extra_charge - discount
        
        if pay_status == "PAID":
            paid = total
        elif pay_status == "PARTIALLY_PAID":
            paid = total / 2
        else:
            paid = 0.0

        received_dt = now - timedelta(days=days_ago, hours=hours_offset)
        est_dt = received_dt + timedelta(minutes=srv[6] + 60)
        
        actual_ready_dt = None
        completed_dt = None
        if status in ("READY_FOR_PICKUP", "COMPLETED"):
            actual_ready_dt = (received_dt + timedelta(minutes=srv[6])).strftime("%Y-%m-%d %H:%M")
        if status == "COMPLETED":
            completed_dt = (received_dt + timedelta(minutes=srv[6] + 120)).strftime("%Y-%m-%d %H:%M")

        on_hold_reason = "Menunggu konfirmasi pelanggan terkait warna bahan & jenis semir khusus" if status == "ON_HOLD" else None

        cursor.execute("""
            INSERT INTO orders (
                id, outlet_id, customer_id, order_code, created_by_user_id, status, payment_status,
                subtotal, discount_amount, extra_charge, total_amount, paid_amount,
                received_at, estimated_ready_at, actual_ready_at, completed_at, customer_notes,
                cancellation_reason, created_at, updated_at
            ) VALUES (?, 1, ?, ?, 2, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            idx, cust_id, code, status, pay_status,
            subtotal, discount, extra_charge, total, paid,
            received_dt.strftime("%Y-%m-%d %H:%M"), est_dt.strftime("%Y-%m-%d %H:%M"),
            actual_ready_dt, completed_dt, notes, on_hold_reason,
            received_dt.strftime("%Y-%m-%d %H:%M"), received_dt.strftime("%Y-%m-%d %H:%M")
        ))

        # Order Item
        cursor.execute("""
            INSERT INTO order_items (
                order_id, service_id, service_name_snapshot, pricing_unit_snapshot,
                unit_price, quantity, line_total, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            idx, s_id, srv[2], srv[4], unit_price, qty, subtotal, notes
        ))

        # Order Status History
        histories = [("RECEIVED", "Pesanan diterima di kasir", received_dt)]
        if status in ("QUEUED", "WASHING", "DRYING", "IRONING", "QUALITY_CHECK", "READY_FOR_PICKUP", "COMPLETED", "ON_HOLD"):
            histories.append(("QUEUED", "Masuk antrean produksi", received_dt + timedelta(minutes=15)))
        if status in ("WASHING", "DRYING", "IRONING", "QUALITY_CHECK", "READY_FOR_PICKUP", "COMPLETED"):
            histories.append(("WASHING", "Sedang dicuci di mesin cuci #2", received_dt + timedelta(minutes=45)))
        if status in ("DRYING", "IRONING", "QUALITY_CHECK", "READY_FOR_PICKUP", "COMPLETED"):
            histories.append(("DRYING", "Masuk pengering suhu medium", received_dt + timedelta(minutes=90)))
        if status in ("IRONING", "QUALITY_CHECK", "READY_FOR_PICKUP", "COMPLETED"):
            histories.append(("IRONING", "Setrika uap dan pelipatan rapi", received_dt + timedelta(minutes=180)))
        if status in ("QUALITY_CHECK", "READY_FOR_PICKUP", "COMPLETED"):
            histories.append(("QUALITY_CHECK", "Inspeksi kerapian dan kelengkapan item", received_dt + timedelta(minutes=240)))
        if status in ("READY_FOR_PICKUP", "COMPLETED"):
            histories.append(("READY_FOR_PICKUP", "Pakaian selesai dipacking dan siap diambil", received_dt + timedelta(minutes=260)))
        if status == "COMPLETED":
            histories.append(("COMPLETED", "Diserahkan ke pelanggan dan transaksi selesai", received_dt + timedelta(minutes=320)))
        if status == "ON_HOLD":
            histories.append(("ON_HOLD", on_hold_reason, received_dt + timedelta(minutes=30)))

        for h_status, h_note, h_time in histories:
            cursor.execute("""
                INSERT INTO order_status_history (order_id, to_status, changed_by_user_id, changed_by_name, note, changed_at)
                VALUES (?, ?, 2, 'Siti Rahayu', ?, ?);
            """, (idx, h_status, h_note, h_time.strftime("%Y-%m-%d %H:%M")))

        # Payments
        if paid > 0 and pay_method:
            cursor.execute("""
                INSERT INTO payments (
                    order_id, amount, method, status, reference_code, recorded_by_user_id, recorded_by_name, paid_at
                ) VALUES (?, ?, ?, 'PAID', ?, 2, 'Siti Rahayu', ?);
            """, (idx, paid, pay_method, f"TRX-{code.replace('LF-', '')}", received_dt.strftime("%Y-%m-%d %H:%M")))

    # 6. Notifications
    cursor.execute("""
        INSERT INTO notifications (user_id, customer_id, order_id, title, message, channel, created_at)
        VALUES 
        (4, 1, 11, 'Cucian Siap Diambil!', 'Pesanan Anda LF-20261023-0001 sudah wangi, rapi, dan siap diambil di outlet.', 'IN_APP', ?),
        (5, 2, 12, 'Status Cucian Diperbarui', 'Pesanan LF-20261023-0002 telah selesai disetrika dan masuk tahap pengecekan kualitas.', 'IN_APP', ?),
        (1, NULL, 14, 'Antrean Baru Masuk', 'Pesanan LF-20261024-0001 masuk ke antrean setrika dengan total 8.5 kg.', 'IN_APP', ?);
    """, (now.strftime("%Y-%m-%d %H:%M"), (now - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), (now - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M")))

    # 7. Audit Logs
    cursor.execute("""
        INSERT INTO audit_logs (outlet_id, actor_user_id, actor_name, action, entity_type, entity_id, details, created_at)
        VALUES 
        (1, 1, 'Pak Budi Hartanto', 'UPDATE_PRICE', 'SERVICE', 4, 'Penyesuaian tarif kilat express menjadi Rp 16.000/kg', ?),
        (1, 2, 'Siti Rahayu', 'CREATE_ORDER', 'ORDER', 14, 'Membuat pesanan baru LF-20261024-0001 untuk Ibu Linda Kusuma (8.5 kg)', ?),
        (1, 2, 'Siti Rahayu', 'RECORD_PAYMENT', 'PAYMENT', 11, 'Menerima pembayaran QRIS Rp 36.000 untuk LF-20261023-0001', ?);
    """, ((now - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"), (now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"), (now - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")))

    conn.commit()
    conn.close()
    print("Seed data successfully injected into laundryflow.db!")

if __name__ == "__main__":
    seed_database()
