import graphene
from graphene import relay
from core.api.graphql.types import RelayFilterConnectionField, RelayNode
from core.utils import handle_error
from .types import ShowtimeNode, BookingNode, PaymentNode, PromotionNode

class Query(graphene.ObjectType):
    all_showtimes = RelayFilterConnectionField(ShowtimeNode)
    all_bookings = RelayFilterConnectionField(BookingNode)
    all_payments = RelayFilterConnectionField(PaymentNode)
    all_promotions = RelayFilterConnectionField(PromotionNode)
