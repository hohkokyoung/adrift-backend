import graphene
from core.api.graphql.types import RelayObjectType
from theaters.models import (
    Theater, Experience, ExperienceImage,
    Hall, Seat
)

class TheaterNode(RelayObjectType):
    class Meta:
        model = Theater
        filter_fields = ["name"]
        fields = "__all__"

class ExperienceNode(RelayObjectType):
    class Meta:
        model = Experience
        filter_fields = ["description"]
        fields = "__all__"

class ExperienceImageNode(RelayObjectType):
    class Meta:
        model = ExperienceImage
        filter_fields = ["experience"]
        fields = "__all__"

class HallNode(RelayObjectType):
    class Meta:
        model = Hall
        filter_fields = ["name"]
        fields = "__all__"

class SeatNode(RelayObjectType):
    class Meta:
        model = Seat
        filter_fields = ["type"]
        fields = "__all__"
