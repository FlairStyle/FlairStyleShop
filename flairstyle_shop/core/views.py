from apps.store.models import Product
from apps.store.models import ReviewRating
from django.http import HttpResponse
from django.shortcuts import render


def home(request) -> HttpResponse:
    products = (
        Product.objects.select_related("category")
        .all()
        .filter(is_available=True)
        .only(
            "id",
            "slug",
            "category__id",
            "product_name",
            "category__slug",
            "images",
            "price",
        )
        .order_by("created_date")
    )
    for single_product in products:
        reviews = ReviewRating.objects.filter(product_id=single_product, status=True)
    # TODO: Fix this
    # ERROR: "reviews" is possibly unbound
    reviews = None
    context = {
        "products": products,
        "reviews": reviews,  # type: ignore
    }
    return render(request, "home.html", context)
