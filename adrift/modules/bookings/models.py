from django.db import models
from core.models import BaseModel
from movies.models import Movie
from theaters.models import Hall, Seat
from django.contrib.auth import get_user_model
from bookings.enums import BookingStatus as BookingStatusEnum, PaymentMethod as PaymentMethodEnum, BookingType as BookingTypeEnum

User = get_user_model()

class Showtime(BaseModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name="showtimes")
    date = models.DateField()
    time = models.TimeField()
    language = models.CharField(max_length=255)
    price = models.IntegerField()

    class Meta:
        ordering = ["date"]

class Booking(BaseModel):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateTimeField()
    status = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in BookingStatusEnum]
    )
    type = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in BookingTypeEnum]
    )

    class Meta:
        ordering = ["date"]

class Payment(BaseModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateTimeField()
    amount = models.IntegerField()
    method = models.CharField(
        max_length=30,
        choices=[(enum.name, enum.value) for enum in PaymentMethodEnum]
    )
    transaction_id = models.CharField(max_length=255)

    class Meta:
        ordering = ["transaction_id"]


class PaymentPromotion(BaseModel):
    promotion = models.ForeignKey('Promotion', on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE)

    class Meta:
        app_label = "bookings"


class Promotion(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    discount_percentage = models.IntegerField()
    condition = models.TextField()
    poster = models.URLField(null=True, blank=True)
    payments = models.ManyToManyField(Payment, related_name="promotions", through=PaymentPromotion, through_fields=("promotion", "payment"))

    class Meta:
        ordering = ["title"]

