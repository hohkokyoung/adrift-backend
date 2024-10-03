import graphene
from core.api.graphql.types import RelayObjectType
from bookings.models import (
    Showtime, Booking, Payment,
    Promotion
)

class ShowtimeNode(RelayObjectType):
    class Meta:
        model = Showtime
        filter_fields = ["movie"]
        fields = "__all__"

class BookingNode(RelayObjectType):
    class Meta:
        model = Booking
        filter_fields = ["showtime"]
        fields = "__all__"

class PaymentNode(RelayObjectType):
    class Meta:
        model = Payment
        filter_fields = ["booking"]
        fields = "__all__"

class PromotionNode(RelayObjectType):
    class Meta:
        model = Promotion
        filter_fields = ["title"]
        fields = "__all__"

