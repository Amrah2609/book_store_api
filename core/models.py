from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class IndexPage(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Home Pages"


class AboutPage(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to="about")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "About Pages"


class BookCategory(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    icon = models.ImageField(upload_to="category_icons/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Book Categories"


class CategorySection(models.Model):
    heading = models.CharField(max_length=100, default="Book Category")
    subheading = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.heading

    class Meta:
        verbose_name_plural = "Category Sections"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Messages"


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(BookCategory)
    price = models.FloatField(default=1)
    currency = models.CharField(max_length=3, default="AZN")
    description = models.TextField()

    def __str__(self):
        return self.title

    def product_image(self):
        self.productimage_set.all().first

class ProductImage(models.Model):
    image = models.ImageField(upload_to="book/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return self.image.name



class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    review = models.TextField()

    def __str__(self):
        return self.product.title