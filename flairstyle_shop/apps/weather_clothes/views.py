from .utils import fetch_current_temperature
from apps.store.models import Product
from django.http import JsonResponse
from django.views import View


class SuitableClothesView(View):
    def get(self, request) -> JsonResponse:
        temperature = fetch_current_temperature()

        if isinstance(temperature, dict):
            return JsonResponse(temperature)

        suitable_clothes = Product.objects.filter(
            suitable_temperature_min__lte=temperature,
            suitable_temperature_max__gte=temperature,
        )

        suitable_clothes_list = list(suitable_clothes.values())

        return JsonResponse(suitable_clothes_list, safe=False)
