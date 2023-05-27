from .forms import OrderForm
from .models import Order
from .models import OrderProduct
from .models import Payment
from apps.carts.models import CartItem
from apps.store.models import Product
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string

import datetime


def custom_redirect(url_name, *args, **kwargs) -> HttpResponseRedirect:
    from django.urls import reverse

    import urllib

    url = reverse(url_name, args=args)
    # TODO: Fix this
    # ERROR: "parse" is not a known member of module "urllib"
    params = urllib.parse.urlencode(kwargs)  # type: ignore
    return HttpResponseRedirect(url + "?%s" % params)


def place_order(
    request, total=0, quantity=0, grand_total=0, tax=0
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("store")

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data["first_name"]
            data.last_name = form.cleaned_data["last_name"]
            data.phone = form.cleaned_data["phone"]
            data.email = form.cleaned_data["email"]
            data.address_line_1 = form.cleaned_data["address_line_1"]
            data.address_line_2 = form.cleaned_data["address_line_2"]
            data.country = form.cleaned_data["country"]
            data.state = form.cleaned_data["state"]
            data.city = form.cleaned_data["city"]
            data.order_note = form.cleaned_data["order_note"]
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get("REMOTE_ADDR")
            data.save()
            yr = int(datetime.date.today().strftime("%Y"))
            dt = int(datetime.date.today().strftime("%d"))
            mt = int(datetime.date.today().strftime("%m"))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            # TODO: Fix this
            # ERROR: Cannot access member "id" for type "Order"
            order_number = current_date + str(data.id)  # type: ignore
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "tax": tax,
                "grand_total": grand_total,
            }
            return render(request, "orders/payments.html", context)

        else:
            return redirect("checkout")
    else:
        return redirect("checkout")


def payments(request) -> HttpResponseRedirect:
    # body = json.loads(request.body)
    # order = Order.objects.get(
    #     user=request.user, is_ordered=False, order_number=body["orderID"]
    # )
    # payment = Payment(
    #     user=request.user,
    #     payment_id=body["transactionID"],
    #     payment_method=body["transactionID"],
    #     amount_paid=order.order_total,
    #     status=body["status"],
    # )
    # payment.save()
    # order.payment = payment
    # order.is_ordered = True
    # order.save()

    latest_order = Order.objects.latest("id").order_number
    order = get_object_or_404(
        Order,
        user=request.user,
        is_ordered=False,
        order_number=latest_order,
    )

    payment = Payment(
        user=request.user,
        # TODO: Fix this
        # ERROR: Cannot access member "id" for type "Order"
        payment_id=f"ORDERID{order.id}",  # type: ignore
        payment_method="PayPal",
        amount_paid=order.order_total,
        status="SUCCESS",
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct()
        # TODO: Fix this
        # ERROR: Cannot access member "order_id" for type "OrderProduct"
        # ERROR: Cannot access member "user_id" for type "OrderProduct"
        # ERROR: Cannot access member "product_id" for type "OrderProduct"
        order_product.order_id = order.id  # type: ignore
        order_product.payment = payment
        order_product.user_id = request.user.id  # type: ignore
        order_product.product_id = item.product_id  # type: ignore
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        # TODO: Fix this
        # ERROR: Cannot access member "id" for type "CartItem"
        cart_item = CartItem.objects.get(id=item.id)  # type: ignore
        product_variation = cart_item.variations.all()
        # TODO: Fix this
        # ERROR: Cannot access member "id" for type "OrderProduct"
        order_product = OrderProduct.objects.get(id=order_product.id)  # type: ignore
        order_product.variations.set(product_variation)
        order_product.save()

        # TODO: Fix this
        # ERROR: Cannot access member "product_id" for type "CartItem"
        product = Product.objects.get(id=item.product_id)  # type: ignore
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    mail_subject = "Thank you for order!"
    message = render_to_string(
        "orders/order_received_mail.html",
        {
            "user": request.user,
            "order": order,
        },
    )
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, from_email="noreply@gmail.com", to=[to_email])
    send_email.send()

    data = {
        "order_number": order.order_number,
        "transactionID": payment.payment_id,
    }
    return custom_redirect(
        "order_complete",
        order_number=data["order_number"],
        transactionID=data["transactionID"],
    )


def order_complete(request) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    order_number = request.GET.get("order_number")
    transactionID = request.GET.get("transactionID")
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        # TODO: Fix this
        # ERROR: Cannot access member "id" for type "Order"
        ordered_products = OrderProduct.objects.filter(order_id=order.id)  # type: ignore

        payment = Payment.objects.get(payment_id=transactionID)

        sub_total = order.order_total - order.tax

        context = {
            "order": order,
            "ordered_products": ordered_products,
            "transactionID": payment.payment_id,
            "payment": payment,
            "sub_total": sub_total,
        }
        return render(request, "orders/order_complete.html", context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect("home")
