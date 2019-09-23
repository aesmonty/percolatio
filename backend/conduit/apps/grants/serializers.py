from rest_framework import serializers

from conduit.apps.profiles.serializers import ProfileSerializer

from .models import Grant, Tag
from .relations import TagRelatedField


class GrantSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    amount = serializers.IntegerField(required=False)
    grantees = serializers.IntegerField(required=False)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )

    tagList = TagRelatedField(many=True, required=False, source='tags')

    # Django REST Framework makes it possible to create a read-only field that
    # gets it's value by calling a function. In this case, the client expects
    # `created_at` to be called `createdAt` and `updated_at` to be `updatedAt`.
    # `serializers.SerializerMethodField` is a good way to avoid having the
    # requirements of the client leak into our API.
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Grant
        fields = (
            'author',
            'body',
            'amount',
            'grantees',
            'createdAt',
            'description',
            'favorited',
            'favoritesCount',
            'slug',
            'tagList',
            'title',
            'updatedAt',
        )

    def create(self, validated_data):
        author = self.context.get('author', None)

        tags = validated_data.pop('tags', [])

        grant = Grant.objects.create(author=author, **validated_data)

        for tag in tags:
            grant.tags.add(tag)

        return grant

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated():
            return False

        return request.user.profile.has_favorited_grant(instance)

    def get_favorites_count(self, instance):
        return instance.favorited_grants_by.count()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

    def to_representation(self, obj):
        return obj.tag
