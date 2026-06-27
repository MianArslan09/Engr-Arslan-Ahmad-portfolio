from django.urls import path
from .views import HomeView, ContactFormView

app_name = "portfolio"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactFormView.as_view(), name="contact"),
]