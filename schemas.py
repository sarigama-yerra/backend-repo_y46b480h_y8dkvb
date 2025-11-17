"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Divines fast food specific schemas

class MenuItem(BaseModel):
    """
    Fast food restaurant menu item
    Collection name: "menuitem"
    """
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="e.g., Burgers, Sides, Drinks, Desserts")
    image_url: Optional[str] = Field(None, description="Image URL")
    is_featured: bool = Field(False, description="Show as a featured item")
    spicy_level: Optional[int] = Field(None, ge=0, le=3, description="0-3 scale")

class Location(BaseModel):
    """
    Restaurant locations
    Collection name: "location"
    """
    name: str = Field(..., description="Location name")
    address: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    country: str = Field(..., description="Country")
    phone: Optional[str] = Field(None, description="Contact phone")
    hours: Optional[str] = Field(None, description="Opening hours")
    latitude: Optional[float] = Field(None, description="Latitude for map")
    longitude: Optional[float] = Field(None, description="Longitude for map")

class Highlight(BaseModel):
    """
    Highlights for homepage hero or banners
    Collection name: "highlight"
    """
    title: str
    subtitle: Optional[str] = None
    cta_text: Optional[str] = None
    cta_link: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    tags: Optional[List[str]] = None

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
