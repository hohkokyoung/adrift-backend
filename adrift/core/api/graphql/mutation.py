import graphene
from core.enums import Country as CountryEnum

class AddressInput(graphene.InputObjectType):
    country = graphene.Enum.from_enum(CountryEnum)()
    state = graphene.String(required=True)
    city = graphene.String(required=True)
    line_address_one = graphene.String(required=True)
    line_address_one = graphene.String()