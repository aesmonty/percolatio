from django.db import models
from conduit.apps.core.models import TimestampedModel

DEFAULT_NUMBER_OF_APPLICANTS = 1


class Grant(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(max_length=255)

    isPreFunded = models.BooleanField()
    numberOfGrantees = models.IntegerField(
        default=1)
    amountPerGrantee = models.IntegerField()
    nonFinancialRewards = models.BooleanField(default=False)

    applicationsStartDate = models.DateTimeField()
    applicationsEndDate = models.DateTimeField()

    description = models.TextField()
    externalWebsite = models.TextField(default='')
    otherDetails = models.TextField(default='')

    # TODO: use s3
    supportingData = models.TextField(default='')

    foundation = models.ForeignKey(
        'foundations.Foundation', on_delete=models.CASCADE, related_name='grants'
    )

    tags = models.ManyToManyField(
        'grants.Tag', related_name='grants'
    )

    body = models.TextField()

    def __str__(self):
        return self.title


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
