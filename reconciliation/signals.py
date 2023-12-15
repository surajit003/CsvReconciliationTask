import structlog
from django.db.models.signals import post_save
from django.dispatch import receiver

from reconciliation.models import SourceTargetFilePair
from reconciliation.tasks import process_file

logger = structlog.get_logger(__name__)


@receiver(post_save, sender=SourceTargetFilePair)
def on_upload(sender, instance, **kwargs):
    logger.info("Received post_save signal.", instance=instance)
    process_file.delay(instance.id)
    return
