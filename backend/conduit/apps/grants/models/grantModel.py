from django.db import models
from conduit.apps.core.models import TimestampedModel
from django.utils.timezone import now


DEFAULT_NUMBER_OF_APPLICANTS = 1


def upload_image_to(instance, filename):
    return 'grant/%s/%s' % (
        now().strftime("%Y%m%d"),
        instance.slug
    )


class Grant(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(max_length=255)

    img = models.FileField(
        upload_to=upload_image_to,
        blank=True,
        editable=True)

    isPreFunded = models.BooleanField(default=False)
    numberOfGrantees = models.IntegerField(
        default=1)
    amountPerGrantee = models.IntegerField()
    nonFinancialRewards = models.BooleanField(default=False)

    applicationsStartDate = models.DateField()
    applicationsEndDate = models.DateField()

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
