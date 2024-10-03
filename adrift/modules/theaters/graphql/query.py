import graphene
from graphene import relay
from core.api.graphql.types import RelayFilterConnectionField, RelayNode
from .types import *

class Query(graphene.ObjectType):
    all_theaters = RelayFilterConnectionField(TheaterNode)
