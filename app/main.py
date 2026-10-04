from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

from app.tilltalk import answer_price_query


app = FastAPI(
    title="TillTalk AI",
    description="AI-powered supermarket price lookup assistant",
    version="0.2.0"
)


class PriceQuery(BaseModel):
    query: str
    store_id: int = 1


class PriceQueryResponse(BaseModel):
    status: str

    message: Optional[str] = None

    product_name: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    aisle: Optional[str] = None

    price: Optional[float] = None
    price_type: Optional[str] = None
    promotion_description: Optional[str] = None

    requested_size: Optional[str] = None
    available_sizes: Optional[List[str]] = None


@app.get("/")
def root():
    return {
        "service": "TillTalk AI",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TillTalk AI"
    }


@app.post(
    "/price-query",
    response_model=PriceQueryResponse
)
def price_query(request: PriceQuery):
    return answer_price_query(
        query=request.query,
        store_id=request.store_id
    )