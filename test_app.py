import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from app import app


def test_find_cheapest_rejects_zero_amount():
    client = app.test_client()
    response = client.get("/api/find-cheapest?from=MYR&to=USD&amount=0")

    assert response.status_code == 400
    assert response.get_json() == {"error": "amount must be positive"}


def test_find_cheapest_rejects_negative_amount():
    client = app.test_client()
    response = client.get("/api/find-cheapest?from=MYR&to=USD&amount=-1000")

    assert response.status_code == 400
    assert response.get_json() == {"error": "amount must be positive"}
