from django.urls import path

from core import views

urlpatterns = [
    path("", views.WeatherDataView.as_view(), name="index"),
]
