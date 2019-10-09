from django.db import models

from conduit.apps.core.models import TimestampedModel


class Profile(TimestampedModel):

    # Each user has a single profile. The authentication profile and the user profile are seperated.
    # that way we can have different authentication methods.
    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE
    )

    # User Profile
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)

    # User Social Network Aspect
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    follows_foundation = models.ManyToManyField(
        'foundations.Foundation',
        related_name='followed_by',
        symmetrical=False
    )

    favorite_grants = models.ManyToManyField(
        'grants.Grant',
        related_name='favorited_by'
    )

    def __str__(self):
        return self.user.username

    def follow_foundation(self, foundation):
        """Follow `foundation` if we're not already following `foundation`."""
        self.follows_foundation.add(foundation)

    def unfollow_foundation(self, foundation):
        """Unfollow `foundation` if we're already following `foundation`."""
        self.follows_foundation.remove(foundation)

    def is_following_foundation(self, foundation):
        """Returns True if we're following `foundation`; False otherwise."""
        return self.follows_foundation.filter(pk=foundation.pk).exists()

    def favorite_grant(self, grant):
        """Favorite `grant` if we haven't already favorited it."""
        self.favorite_grants.add(grant)

    def unfavorite_grant(self, grant):
        """Unfavorite `grant` if we've already favorited it."""
        self.favorite_grants.remove(grant)

    def has_favorited_grant(self, grant):
        """Returns True if we have favorited `grant`; else False."""
        return self.favorite_grants.filter(pk=grant.pk).exists()
