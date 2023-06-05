from . import views
from django.urls import path


urlpatterns = [
    path("", views.SuitableClothesView.as_view(), name="weather_clothes"),
]
