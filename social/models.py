from django.db import models

class Feed(models.Model):
    TYPE_CHOICES = (
        ('TW', 'Twitter'),
        ('FB', 'Facebook'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    origin_id = models.CharField(max_length=25, db_index=True)
    account_name = models.CharField(max_length=50)
    last_update = models.DateTimeField(db_index=True, null=True)
    update_error_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (('type', 'origin_id'),)

class Update(models.Model):
    feed = models.ForeignKey(Feed, db_index=True)
    text = models.CharField(max_length=500)
    created_time = models.DateTimeField(db_index=True)
    origin_id = models.CharField(max_length=25, db_index=True)

    class Meta:
        unique_together = (('feed', 'origin_id'),)
