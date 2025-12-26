from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from core.models import (
    IndexPage,
    BookCategory,
    CategorySection,
    AboutPage,
    ContactMessage, Product,
)
from core.forms import ContactForm, LoginForm, RegisterForm
from django.contrib import messages

# Create your views here.


def index(request):
    about = AboutPage.objects.first()
    section = CategorySection.objects.first()
    categories = BookCategory.objects.all()
    content = {
        "index_pages": IndexPage.objects.all(),
        "about": about,
        "section": section,
        "categories": categories,
    }
    return render(request, "index.html", content)


def about(request):
    content = {"about": AboutPage.objects.first()}
    return render(request, "about.html", content)


def categories(request):
    section = CategorySection.objects.first()
    content = {
        "section": section,
        "categories": BookCategory.objects.all(),
    }
    return render(request, "categories.html", content)


def blog(request):
    return render(request, "blog.html")


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesaj göndərildi.")
            return redirect("contact")
        else:
            messages.error(request, "Formda səhv var. Zəhmət olmasa yenidən yoxlayın.")
    content = {
        "form": form,
    }
    return render(request, "contact.html", content)


def card(request):
    return render(request, "card.html")

def product_list(request):
    products = Product.objects.all()
    return render(request, "products.html", {"products": products})

def product_detail(request, product_id):
    return render(request, "product_detail.html", {
        "product_id": product_id
    })


def checkout_page(request):
    return render(request, "checkout_page.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    context = {"form": LoginForm()}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context["form"] = form
                context["error"] = "Istifadechi adi ve ya shifre yanlishdir."
    return render(request, "login.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("index")
    context = {"form": RegisterForm()}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            user = form.save()
            user.set_password(password)
            user.save()
            messages.success(request, f"{user.username} Uğurla qeydiyyatdan keçdiniz.")
            return redirect("login")
        else:
            context["form"] = form
    return render(request, "register.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def search(request):
    query = request.GET.get("q")
    context = {}
    if query:
        context["products"] = Product.objects.filter(title__icontains=query)
    else:
        context["products"] = Product.objects.all()
    return render(request, "search.html", context)
