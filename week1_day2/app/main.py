"""FastAPI application for Week1-Day2 with path, query, and enum examples."""

from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI(title="Week1-Day2 App", version="1.0.0")


@app.get("/")
async def root():
    """Root endpoint for a friendly message."""
    return {"message": "Hello from Week1-Day2"}


# --- Path params with types and constraints ---
@app.get("/items/{item_id}")
async def get_item(item_id: Annotated[int, Path(ge=1, le=1_00_000)]):
    """Read an item by its ID."""
    return {"item_id": item_id}


# --- Query params with types and constraints ---
@app.get("/search")
async def search_items(
    # Important: set defaults with "=" (outside query) to avoid the assertion you saw
    q: Annotated[str | None, Query(min_length=1, max_length=100, alias="query")] = None,
    tags: Annotated[list[str] | None, Query(alias="tags")] = None,  # repeated tags=...values
    exact: Annotated[bool, Query()] = False,
):
    """Search for items."""
    if tags is None:
        tags = []
    return {"q": q, "tags": tags, "exact": exact}


class ItemCategory(str, Enum):
    """Enumeration for item categories."""

    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    TOYS = "toys"
    BOOKS = "books"


@app.get("/categories/{category}")
async def list_items_by_category(category: ItemCategory):
    """List items by category."""
    return {"category": category.value, "sample": ["example1", "example2", "example3"]}
