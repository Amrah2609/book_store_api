from ninja import NinjaAPI
from typing import List
from django.shortcuts import get_object_or_404
from ninja.security import django_auth

from core.models import (
    Product, BookCategory, Author,
    ProductReview, ContactMessage, ProductImage
)
from .schemas import (
    ProductOut, ProductIn,
    ReviewIn, ContactIn
)

api = NinjaAPI(title="Book Store API")

# Products

@api.get("/products", response=List[ProductOut])
def list_products(request):
    """
    Bütün məhsulların siyahısı
    """
    products = Product.objects.all()
    result = []
    for product in products:
        result.append(
            ProductOut(
                id=product.id,
                title=product.title,
                author=product.author,
                price=product.price,
                currency=product.currency,
                description=product.description,
                categories=product.categories.all(),
                images=[img.image.url for img in ProductImage.objects.filter(product=product)]
            )
        )
    return result


@api.get("/products/{product_id}", response=ProductOut)
def product_detail(request, product_id: int):
    product = get_object_or_404(Product, id=product_id)

    from core.models import ProductImage
    images = [img.image.url for img in ProductImage.objects.filter(product=product)]

    return ProductOut(
        id=product.id,
        title=product.title,
        author=product.author,
        price=product.price,
        currency=product.currency,
        description=product.description,
        categories=product.categories.all(),
        images=images  # <--- burada olmalıdır
    )



@api.post("/products", auth=django_auth)
def create_product(request, payload: ProductIn):
    """
    Yeni məhsul yarat (auth lazımdır)
    """
    author = get_object_or_404(Author, id=payload.author_id)
    product = Product.objects.create(
        title=payload.title,
        author=author,
        price=payload.price,
        currency=payload.currency,
        description=payload.description
    )
    product.categories.set(
        BookCategory.objects.filter(id__in=payload.category_ids)
    )
    return {"id": product.id}


@api.put("/products/{product_id}", auth=django_auth)
def update_product(request, product_id: int, payload: ProductIn):
    """
    Məhsulu yenilə (auth lazımdır)
    """
    product = get_object_or_404(Product, id=product_id)
    author = get_object_or_404(Author, id=payload.author_id)

    product.title = payload.title
    product.author = author
    product.price = payload.price
    product.currency = payload.currency
    product.description = payload.description
    product.categories.set(
        BookCategory.objects.filter(id__in=payload.category_ids)
    )
    product.save()
    return {"updated": True}


@api.delete("/products/{product_id}", auth=django_auth)
def delete_product(request, product_id: int):
    """
    Məhsulu sil (auth lazımdır)
    """
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return {"deleted": True}


# Reviews

@api.post("/products/{product_id}/reviews", auth=django_auth)
def add_review(request, product_id: int, payload: ReviewIn):
    """
    Məhsula review əlavə et
    """
    product = get_object_or_404(Product, id=product_id)
    ProductReview.objects.create(
        product=product,
        user=request.user,
        stars=payload.stars,
        review=payload.review
    )
    return {"success": True}


@api.get("/products/{product_id}/reviews")
def list_reviews(request, product_id: int):
    """
    Məhsulun bütün review-ları
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = ProductReview.objects.filter(product=product)
    return [
        {
            "user": review.user.username,
            "stars": review.stars,
            "review": review.review
        }
        for review in reviews
    ]


# Contact

@api.post("/contact")
def send_message(request, payload: ContactIn):
    """
    Contact form mesajı
    """
    ContactMessage.objects.create(**payload.dict())
    return {"sent": True}
