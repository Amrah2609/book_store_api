from django.contrib import admin
from django.template.defaultfilters import title
from django.utils.html import format_html
from core.models import (
    IndexPage,
    AboutPage,
    BookCategory,
    CategorySection,
    ContactMessage,
    Author,
    Product,
    ProductImage,
    ProductReview,
)


@admin.register(IndexPage)
class IndexPageAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "image")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_preview")

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="70" height="70" />', obj.icon.url)
        return "-"

    icon_preview.short_description = "Icon Preview"


@admin.register(CategorySection)
class CategorySectionAdmin(admin.ModelAdmin):
    list_display = ("heading", "subheading")


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "message")
    list_filter = ("name", "phone", "email")
    search_fields = ("name", "email", "phone")


admin.site.register(Author)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'description']
    inlines = [ProductImageInline]
