import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents
from schemas import MenuItem, Location, Highlight

app = FastAPI(title="Divines Fast Food API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Divines API is running"}

# Public endpoints to fetch content
@app.get("/api/menu", response_model=List[MenuItem])
def list_menu(category: Optional[str] = None, featured: Optional[bool] = None, limit: Optional[int] = 100):
    try:
        query = {}
        if category:
            query["category"] = category
        if featured is not None:
            query["is_featured"] = featured
        docs = get_documents("menuitem", query or {}, limit)
        # Normalize Mongo _id to string and map to Pydantic
        items = []
        for d in docs:
            d.pop("_id", None)
            items.append(MenuItem(**d))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/menu", status_code=201)
def add_menu_item(item: MenuItem):
    try:
        inserted_id = create_document("menuitem", item)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/locations", response_model=List[Location])
def list_locations(limit: Optional[int] = 50):
    try:
        docs = get_documents("location", {}, limit)
        for d in docs:
            d.pop("_id", None)
        return [Location(**d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/locations", status_code=201)
def add_location(location: Location):
    try:
        inserted_id = create_document("location", location)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/highlights", response_model=List[Highlight])
def list_highlights(limit: Optional[int] = 10):
    try:
        docs = get_documents("highlight", {}, limit)
        for d in docs:
            d.pop("_id", None)
        return [Highlight(**d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/highlights", status_code=201)
def add_highlight(highlight: Highlight):
    try:
        inserted_id = create_document("highlight", highlight)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
