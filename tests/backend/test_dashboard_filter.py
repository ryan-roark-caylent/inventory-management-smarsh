def test_inventory_count_respects_filter(client):
    # total_inventory_items must reflect the SAME filters as the rest of the summary
    all_resp = client.get("/api/dashboard/summary")
    filtered = client.get("/api/dashboard/summary", params={"warehouse": "San Francisco"})
    assert all_resp.status_code == 200
    assert filtered.status_code == 200
    # the filtered inventory count must be strictly less than the global count
    # San Francisco owns 12 of 32 inventory items — a real strict subset
    assert filtered.json()["total_inventory_items"] < all_resp.json()["total_inventory_items"]
