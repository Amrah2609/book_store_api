from ninja import Schema
from typing import List
from datetime import datetime


class CategoryOut(Schema):
    id: int
    name: str
    title: str


class AuthorOut(Schema):
    id: int
    name: str


class ProductOut(Schema):
    id: int
    title: str
    author: AuthorOut
    price: float
    currency: str
    description: str
    categories: List[CategoryOut]
    images: List[str]


class ProductIn(Schema):
    title: str
    author_id: int
    category_ids: List[int]
    price: float
    currency: str = "AZN"
    description: str


class ReviewIn(Schema):
    stars: int
    review: str


class ContactIn(Schema):
    name: str
    email: str
    phone: str
    message: str
