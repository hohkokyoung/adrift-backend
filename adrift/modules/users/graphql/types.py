import graphene
from django.contrib.auth import get_user_model
from core.api.graphql.types import RelayObjectType
from core.utils import safe_get
from core.middlewares import get_current_request
from users.models import Role, UserLogin
import graphql_jwt
from graphql_auth.bases import RelayMutationMixin
from graphql_auth.mixins import ObtainJSONWebTokenMixin
from graphql_auth.settings import graphql_auth_settings as app_settings

User = get_user_model()

class RoleNode(RelayObjectType):
    class Meta:
        model = Role
        filter_fields = ["name"]
        fields = "__all__"

class UserNode(RelayObjectType):
    class Meta:
        model = User
        filter_fields = ["username", "roles__name"]
        skip_registry = True
        fields = "__all__"

    pk = graphene.Int()
    full_name = graphene.String()
    archived = graphene.Boolean(default_value=False)
    verified = graphene.Boolean(default_value=False)
    secondary_email = graphene.String(default_value=None)

    def resolve_pk(self, info):
        return self.pk
    
    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}"

    def resolve_archived(self, info):
        return self.status.archived

    def resolve_verified(self, info):
        return self.status.verified

    def resolve_secondary_email(self, info):
        return self.status.secondary_email

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.prefetch_related("roles").select_related("status")

# https://github.dev/PedroBern/django-graphql-auth/tree/master/graphql_auth
class RelayObtainJSONWebToken(
    RelayMutationMixin, ObtainJSONWebTokenMixin, graphql_jwt.relay.JSONWebTokenMutation
):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments["input"]._meta.fields.update(
            {"password": graphene.InputField(graphene.String, required=True)}
        )
        for field in app_settings.LOGIN_ALLOWED_FIELDS:
            cls._meta.arguments["input"]._meta.fields.update(
                {field: graphene.InputField(graphene.String)}
            )

        result = super(graphql_jwt.relay.JSONWebTokenMutation, cls).Field(*args, **kwargs)

        # purposely make token and refresh token field to be nullable
        cls._meta.fields["token"] = graphene.Field(graphene.String)
        cls._meta.fields["refresh_token"] = graphene.Field(graphene.String)
        return result

    # before login
    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        result = super().resolve_mutation(root, info, **kwargs)
        
        request = get_current_request()
        login_data = {
            'identifier': safe_get(kwargs, "username"),
            'is_success': False,
            'ip_address': safe_get(request, "ip_address"),
        }

        if result.success:
            login_data["is_success"] = True
            login_data["created_by"] = result.user

        UserLogin.objects.create(**login_data)
            
        return result
    
