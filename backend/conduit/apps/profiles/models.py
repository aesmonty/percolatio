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

    favorites = models.ManyToManyField(
        'articles.Article',
        related_name='favorited_by'
    )

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we're following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if `profile` is following us; False otherwise."""
        return self.followed_by.filter(pk=profile.pk).exists()

    def follow_foundation(self, foundation):
        """Follow `foundation` if we're not already following `foundation`."""
        self.follows_foundation.add(foundation)

    def unfollow_foundation(self, foundation):
        """Unfollow `foundation` if we're already following `foundation`."""
        self.follows_foundation.remove(foundation)

    def is_following_foundation(self, foundation):
        """Returns True if we're following `foundation`; False otherwise."""
        return self.follows_foundation.filter(pk=foundation.pk).exists()

    def favorite(self, article):
        """Favorite `article` if we haven't already favorited it."""
        self.favorites.add(article)

    def unfavorite(self, article):
        """Unfavorite `article` if we've already favorited it."""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Returns True if we have favorited `article`; else False."""
        return self.favorites.filter(pk=article.pk).exists()

    def favorite_grant(self, grant):
        """Favorite `grant` if we haven't already favorited it."""
        self.favorite_grants.add(grant)

    def unfavorite_grant(self, grant):
        """Unfavorite `grant` if we've already favorited it."""
        self.favorite_grants.remove(grant)

    def has_favorited_grant(self, grant):
        """Returns True if we have favorited `grant`; else False."""
        return self.favorite_grants.filter(pk=grant.pk).exists()
