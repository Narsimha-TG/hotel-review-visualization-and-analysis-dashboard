import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_analytics():
    response = client.get("/api/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "average_sentiment" in data
    assert data["total_reviews"] > 0

def test_trigger_analysis():
    response = client.post("/api/reviews/analyze")
    assert response.status_code == 200
    assert response.json()["status"] == "processing"

def test_get_reviews_pagination():
    response = client.get("/api/reviews?limit=1&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert "hotel_id" in data[0]