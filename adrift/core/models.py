import uuid
from django.db import models
from django.conf import settings
from .enums import LogAction
from django_countries.fields import CountryField

class BaseModel(models.Model):
    class Meta:
        abstract = True

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(class)s_created_by', on_delete=models.CASCADE, db_column="created_by")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='%(class)s_updated_by', on_delete=models.CASCADE, db_column="updated_by")
    is_deleted = models.BooleanField(default=False)


class LogEntry(BaseModel):
    table_name = models.CharField(max_length=255)
    action = models.CharField(max_length=6, choices=[(enum.name, enum.value) for enum in LogAction])
    data_id = models.BigIntegerField(null=True, blank=True)
    old_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(
        protocol='both',  # 'IPv4' or 'IPv6' or 'both' (default)
        unpack_ipv4=True,  # If True, store IPv4 addresses as IPv6-mapped IPv6 addresses
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.action} on {self.table_name} at {self.created_at}"
    

class Address(BaseModel):
    country = CountryField()
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    line_address_one = models.TextField(null=True, blank=True)
    line_address_two = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["country"]
