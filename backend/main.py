from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Hotel Review Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    hotel_id: int
    reviewer_name: str
    rating: int
    review_text: str
    sentiment_score: float
    tags: List[str]
    timestamp: str

# In-memory seed data
reviews_db = [
    Review(id=1, hotel_id=101, reviewer_name="Alice", rating=5, review_text="Excellent stay!", sentiment_score=0.9, tags=["clean", "quiet"], timestamp="2023-10-01T10:00:00Z"),
    Review(id=2, hotel_id=102, reviewer_name="Bob", rating=2, review_text="Too noisy.", sentiment_score=-0.4, tags=["noisy"], timestamp="2023-10-02T11:00:00Z")
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/api/analytics/summary")
def get_analytics():
    avg_sentiment = sum(r.sentiment_score for r in reviews_db) / len(reviews_db)
    return {"total_reviews": len(reviews_db), "average_sentiment": avg_sentiment}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews(limit: int = 10, offset: int = 0):
    return reviews_db[offset : offset + limit]

@app.post("/api/reviews/analyze")
def trigger_analysis():
    return {"status": "processing", "message": "Batch analysis triggered"}

@app.get("/api/export/csv")
def export_csv():
    return {"download_url": "/exports/reviews_export.csv"}