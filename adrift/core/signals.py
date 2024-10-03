from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LogEntry
from .middlewares import get_current_request
from .utils import serialize, safe_get
from django.db.migrations.recorder import MigrationRecorder

@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    if sender in [LogEntry, MigrationRecorder.Migration]:  # Avoid logging changes to the LogEntry model itself
        return

    request = get_current_request()
    new_data = serialize(instance.__dict__)
    user = safe_get(request, "user")
    created_by = None if user and user.is_anonymous else user
    log_data = {
        'table_name': sender._meta.db_table,
        'action': 'create' if created else 'update',
        'data_id': safe_get(new_data, "id"),
        'new_data': new_data,
        'old_data': None,
        'created_by': created_by,
        'ip_address': safe_get(request, "ip_address")
    }

    if not created:
        old_instance = sender.objects.get(pk=instance.pk)
        log_data['old_data'] = serialize(old_instance.__dict__)

    # Remove non-serializable fields
    log_data['new_data'].pop('_state', None)
    if log_data['old_data']:
        log_data['old_data'].pop('_state', None)

    LogEntry.objects.create(**log_data)

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender in [LogEntry, MigrationRecorder.Migration]:  # Avoid logging changes to the LogEntry model itself
        return

    request = get_current_request()
    old_data = serialize(instance.__dict__)
    user = safe_get(request, "user")
    created_by = None if user and user.is_anonymous else user
    log_data = {
        'table_name': sender._meta.db_table,
        'action': 'delete',
        'data_id': safe_get(old_data, "id"),
        'new_data': None,
        'old_data': old_data,
        'created_by': created_by,
        'ip_address': safe_get(request, "ip_address")
    }

    # Remove non-serializable fields
    log_data['old_data'].pop('_state', None)

    LogEntry.objects.create(**log_data)

