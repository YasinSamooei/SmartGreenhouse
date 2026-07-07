from django.urls import path
from panel.views import (
    AdminDashboardHomeView, LoginView, PlantListView,
    PlantDeleteView, PlantDetailView
)
from django.contrib.auth.views import LogoutView

app_name = "panel"

urlpatterns = [
    path("", AdminDashboardHomeView.as_view(), name="home"),
    path("panel/login", LoginView.as_view(), name="panel-login"),
    path("logout/", LogoutView.as_view(next_page="panel:home"), name="panel-logout"),
    path("plant/list", PlantListView.as_view(), name="plant-list"),
    path("plant/delete/<int:pk>", PlantDeleteView.as_view(), name="plant-delete"),
    path("plant/detail/<int:pk>", PlantDetailView.as_view(), name="plant-detail"),
]
