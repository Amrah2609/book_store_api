from django.urls import path
from .views import (
    index,
    about,
    categories,
    blog,
    contact,
    card,
    product_detail,
    checkout_page,
    login_view,
    register,
    logout_view,
    search,
    product_list
)

urlpatterns = [
    path("", index, name="index"),
    path("index/", index, name="index"),
    path("about/", about, name="about"),
    path("categories/", categories, name="categories"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),
    path("card/", card, name="card"),
    path("products/", product_list, name="product_list"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("checkout_page/", checkout_page, name="checkout_page"),
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("logout_view/", logout_view, name="logout_view"),
    path("search/", search, name="search"),
]
