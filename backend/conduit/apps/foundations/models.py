from django.db import models
import uuid

from conduit.apps.core.models import TimestampedModel


class Foundation(TimestampedModel):
    name = models.CharField(db_index=True, max_length=255, unique=True)
    description = models.TextField()

    # Every foundation must have at least one founder.
    founder = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='org'
    )

    grantees = models.ManyToManyField(
        'profiles.Profile', related_name='foundations'
    )

    tags = models.ManyToManyField(
        'foundations.Tag', related_name='foundations'
    )

    def __str__(self):
        return self.name


# TODO: Tag class is both in grant and foundation app (fix this).
# TODO: Also, there should be some sort of relationship between the tags of a foundations and its grants.
class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    # TODO: Is this the slug of the tag?
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
