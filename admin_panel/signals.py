from django.dispatch import receiver
from django.db.models.signals import post_save

from admin_panel.models import Mailing
from asgiref.sync import async_to_sync
from admin_panel.views import get_file_id


MEDIA_TYPES = {
    "no_media": 'no_media',
    "photo": 'image',
    "video": 'video',
    "document": 'document',
}


@receiver(post_save, sender=Mailing)
def make_notification(sender, instance: Mailing, created, **kwargs):
    if not instance.file or instance.file_id or instance.media_type == 'no_media':
        return
    sync_get_file_id = async_to_sync(get_file_id)
    file_type = MEDIA_TYPES.get(instance.media_type)
    if file_type:
        instance.file_id = sync_get_file_id(
            file=instance.file.file,
            file_type=file_type)
        instance.save()
