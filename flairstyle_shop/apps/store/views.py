from .models import Product
from .models import ProductGallery
from .models import ReviewRating
from apps.carts.models import CartItem
from apps.carts.views import _cart_id
from apps.category.models import Category
from apps.orders.models import OrderProduct
from apps.store.forms import ReviewForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render


# TODO: simplify this
# TODO: CBV is more appropriate here
def store(request, category_slug=None) -> HttpResponse:
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = (
            Product.objects.select_related("category").filter(category=categories, is_available=True).order_by("id")
        )
        paginator = Paginator(products, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        products = Product.objects.select_related("category").filter(is_available=True).order_by("id")
        paginator = Paginator(products, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "products_count": page_obj.count,
    }
    return render(request, "store/store.html", context)


# TODO: simplify this
def search(request) -> HttpResponse:
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = (
                Product.objects.select_related("category")
                .order_by("-created_date")
                .filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            )
            products_count = products.count()
    # TODO: Fix this
    context = {
        "products": products,  # type: ignore
        "products_count": products_count,  # type: ignore
    }
    return render(request, "store/store.html", context)


# TODO: simplify this
def product_detail(request, category_slug, product_slug) -> HttpResponse:
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id=single_product.pk).exists()
        except OrderProduct.DoesNotExist:
            order_product = None
    else:
        order_product = None

    reviews = ReviewRating.objects.filter(product_id=single_product.pk)

    product_gallery = ProductGallery.objects.filter(product__id=single_product.pk)

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "order_product": order_product,
        "reviews": reviews,
        "product_gallery": product_gallery,
    }

    return render(request, "store/product_detail.html", context)


# TODO: simplify this
# TODO: CBV is more appropriate here
def submit_review(request, product_id: int) -> HttpResponseRedirect | HttpResponsePermanentRedirect | JsonResponse:
    url = request.META.get("HTTP_REFERRER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                # TODO: Fix this
                # ERROR: Cannot assign member "product_id" for type "ReviewRating"
                # ERROR: Cannot assign member "user_id" for type "ReviewRating"
                data.product_id = product_id  # type: ignore
                data.user_id = request.user.id  # type: ignore
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)
    return JsonResponse({"error": "This is a GET request."})
