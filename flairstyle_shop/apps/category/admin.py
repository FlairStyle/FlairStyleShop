from .models import Category
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "category_name",
        "slug",
        "description",
        "cat_image",
    )
    prepopulated_fields = {"slug": ("category_name",)}


admin.site.register(Category, CategoryAdmin)
