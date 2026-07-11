def test_create_purchase_order(client):
    body = {"backlog_item_id": "3", "supplier_name": "Acme",
            "quantity": 500, "unit_cost": 24.99, "expected_delivery_date": "2026-08-01"}
    r = client.post("/api/purchase-orders", json=body)
    assert r.status_code == 200
    assert "unit_cost" not in r.json()      # the point-step assertion

def test_rejects_nonpositive_quantity(client):
    body = {"backlog_item_id": "3", "supplier_name": "Acme",
            "quantity": 0, "unit_cost": 1.0, "expected_delivery_date": "2026-08-01"}
    assert client.post("/api/purchase-orders", json=body).status_code == 422

def test_unknown_backlog_item_404(client):
    body = {"backlog_item_id": "NOPE", "supplier_name": "Acme",
            "quantity": 5, "unit_cost": 1.0, "expected_delivery_date": "2026-08-01"}
    assert client.post("/api/purchase-orders", json=body).status_code == 404
