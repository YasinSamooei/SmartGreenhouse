from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    image = models.ImageField(upload_to="plant/image")
    created = models.DateTimeField(auto_now_add=True)


class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="numbers")
    image = models.ImageField()
    name = models.CharField(max_length=50)
    healthy = models.BooleanField(default=False)
    problem = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    accuracy = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.created}"
