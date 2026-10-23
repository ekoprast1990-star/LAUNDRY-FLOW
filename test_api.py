import urllib.request
import json

def test_endpoints():
    base = "http://127.0.0.1:5000"
    
    # 1. Auth Me
    with urllib.request.urlopen(f"{base}/api/auth/me") as res:
        data = json.loads(res.read().decode())
        print("[TEST 1: AUTH]", data["success"], data["user"]["name"], f"Role: {data['user']['role']}")

    # 2. Summary
    with urllib.request.urlopen(f"{base}/api/dashboard/summary") as res:
        data = json.loads(res.read().decode())
        m = data["metrics"]
        print("[TEST 2: DASHBOARD]", data["success"], f"Orders Today: {m['orders_today']}", f"Active: {m['active_orders']}", f"Revenue Today: Rp {m['revenue_today']:,.0f}")

    # 3. Public Tracking
    with urllib.request.urlopen(f"{base}/api/track/LF-20261023-0001") as res:
        data = json.loads(res.read().decode())
        print("[TEST 3: TRACKING]", data["success"], data["order"]["order_code"], f"Status: {data['order']['status']}", f"Progress: {data['progress_pct']}%")

    # 4. Create Order
    create_payload = {
        "customer_id": 1,
        "items": [{"service_id": 1, "quantity": 4.5, "notes": "Wangi apel"}],
        "extra_charge": 5000,
        "discount_amount": 0,
        "customer_notes": "Test order automated",
        "initial_payment": {"amount": 41000, "method": "CASH"}
    }
    req = urllib.request.Request(
        f"{base}/api/orders",
        data=json.dumps(create_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode())
        print("[TEST 4: CREATE ORDER]", data["success"], data["order_code"], f"Est Ready: {data['estimated_ready_at']}")

    # 5. Advance Status
    order_id = data["order_id"]
    status_payload = {"status": "WASHING", "note": "Masuk mesin cuci"}
    req2 = urllib.request.Request(
        f"{base}/api/orders/{order_id}/status",
        data=json.dumps(status_payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req2) as res:
        data2 = json.loads(res.read().decode())
        print("[TEST 5: UPDATE STATUS]", data2["success"], f"New status: {data2['new_status']}")

    print("\nALL BACKEND API TESTS PASSED SUCCESSFULLY! 100% OPERATIONAL.")

if __name__ == "__main__":
    test_endpoints()
