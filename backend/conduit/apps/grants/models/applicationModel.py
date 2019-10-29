from django.db import models
from conduit.apps.core.models import TimestampedModel


class GrantApplication(TimestampedModel):

    grant = models.ForeignKey(
        'grants.Grant', related_name='applicants', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'profiles.Profile', related_name='applications', on_delete=models.CASCADE
    )

    body = models.TextField()

    def __str__(self):
        return self.author.user.username
