import graphene
from graphql_auth import relay
from core.api.graphql.types import RelayMutation, eval_permission
from core.api.graphql.mutation import AddressInput
from .types import TheaterNode
from ..models import Theater
from graphql_jwt.decorators import user_passes_test

class CreateTheaterMutation(RelayMutation):
    class Input:
        name = graphene.String(required=True)
        location = AddressInput(required=True)

    theater = graphene.Field(TheaterNode)

    @classmethod
    @user_passes_test(lambda user: eval_permission(user, login_required=True))
    def resolve_mutation(cls, root, info, **kwargs):
        # theater_data = {
        #     "name": kwargs.get("name"),
        #     "location": kwargs.get("location")
        # }

        # theater = Theater(**theater_data)

        return cls(success=True)

class Mutation(graphene.ObjectType):
    create_theater = CreateTheaterMutation.Field()