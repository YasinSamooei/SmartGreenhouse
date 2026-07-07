from django.views.generic import TemplateView, View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from panel.permissions import AuthenticatedMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from detect_plant.models import Plant


class AdminDashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/admin/home.html"


class LoginView(AuthenticatedMixin, View):
    def get(self, request):
        return render(request, "dashboard/admin/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user is None or not user.check_password(password):
            messages.add_message(
                request, messages.ERROR, "user is not exists!!!"
            )
            return render(request, "dashboard/admin/login.html")
        if user.is_superuser:
            login(request, user)
            return redirect("panel:home")
        else:
            messages.add_message(
                request, messages.ERROR, "You do not have the required access."
            )
            return render(request, "dashboard/admin/login.html")


class PlantListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/admin/plant/plant-list.html"
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page_size', self.paginate_by)

    def get_queryset(self):
        queryset = Plant.objects.filter(user=self.request.user)
        return queryset


class PlantDeleteView(LoginRequiredMixin, SuccessMessageMixin, View):

    def get(self, request, pk):
        plant = Plant.objects.get(id=pk)
        return render(request, "dashboard/admin/plant/plant-delete.html", context={"object": plant})

    def post(self, request, pk):
        plant = Plant.objects.get(id=pk)
        if plant.user == request.user:
            plant.delete()
            messages.add_message(
                request, messages.SUCCESS, "plant is deleted."
            )
            return redirect("panel:plant-list")
        else:
            messages.add_message(
                request, messages.ERROR, "You do not have the required access."
            )
            return render(request, "dashboard/admin/plant/plant-delete.html", context={"object": plant})


class PlantDetailView(DetailView):
    template_name = "dashboard/admin/plant/plant-detail.html"
    model = Plant
