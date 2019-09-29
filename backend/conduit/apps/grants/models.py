from django.db import models

from conduit.apps.core.models import TimestampedModel


class Grant(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    amount = models.IntegerField()
    grantees = models.IntegerField()

    description = models.TextField()
    body = models.TextField()

    # Every grant must have a foundation. This will answer questions like "Who
    # gets credit for creating this grant?" and "Who can edit this grant?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Foundation` can have
    # many `Grant`s.

    # TODO: author -> foundation (when foundation is ready).
    # foundation = models.ForeignKey(
    #       'foundations.Foundation', on_delete=models.CASCADE, related_name='grants'
    # (
    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='grants'
    )

    tags = models.ManyToManyField(
        'grants.Tag', related_name='grants'
    )

    def __str__(self):
        return self.title


class Tag(TimestampedModel):  # TODO: Defining this class twice (in grant and foundation).
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
