from django.db import models
from core.models import BaseModel, Address
from django_countries.fields import CountryField
from theaters.enums import Screen as ScreenEnum, Seat as SeatEnum

class Theater(BaseModel):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="theaters")

    class Meta:
        ordering = ["name"]

class Experience(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

class ExperienceImage(BaseModel):
    url = models.URLField()
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ["experience"]

class Hall(BaseModel):
    name = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    screen_type = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in ScreenEnum]
    )
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name="halls")

    class Meta:
        ordering = ["name"]

class Seat(BaseModel):
    number = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    type = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in SeatEnum]
    )
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="seats")

    class Meta:
        ordering = ["number"]

