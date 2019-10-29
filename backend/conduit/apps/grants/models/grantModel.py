from django.db import models
from conduit.apps.core.models import TimestampedModel


class Grant(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(max_length=255)
    amount = models.IntegerField()

    description = models.TextField()
    body = models.TextField()

    foundation = models.ForeignKey(
        'foundations.Foundation', on_delete=models.CASCADE, related_name='grants'
    )

    tags = models.ManyToManyField(
        'grants.Tag', related_name='grants'
    )

    def __str__(self):
        return self.title

# TODO: Defining this class twice (in grant and foundation).


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
