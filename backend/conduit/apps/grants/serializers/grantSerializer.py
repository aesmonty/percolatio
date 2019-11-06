from rest_framework import serializers
from django.core.validators import MinValueValidator, URLValidator

from conduit.apps.profiles.serializers import ProfileSerializer
from conduit.apps.foundations.serializers import FoundationSerializer

from ..models import Grant, Tag
from ..relations import TagRelatedField


class GrantSerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(required=False)
    foundation = FoundationSerializer(read_only=True)

    title = serializers.CharField(required=True)
    tagList = TagRelatedField(many=True, required=False, source='tags')

    isPreFunded = serializers.BooleanField(required=True)
    numberOfGrantees = serializers.IntegerField(
        required=False, validators=[MinValueValidator(1)])

    amountPerGrantee = serializers.IntegerField(
        required=True, validators=[MinValueValidator(0)])

    nonFinancialRewards = serializers.BooleanField(
        required=False,  default=False)

    # TODO: Add validators
    applicationsStartDate = serializers.DateTimeField(required=True)
    applicationsEndDate = serializers.DateTimeField(required=True)
    description = serializers.CharField(required=False)

    externalWebsite = serializers.CharField(
        required=False, validators=[URLValidator()])

    otherDetails = serializers.CharField(required=False)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Grant
        fields = (
            'slug',
            'foundation',
            'title',
            'tagList',
            'isPreFunded',
            'numberOfGrantees',
            'amountPerGrantee',
            'nonFinancialRewards',
            'applicationsStartDate',
            'applicationsEndDate',
            'description',
            'externalWebsite',
            'otherDetails',
            'favorited',
            'favoritesCount',
            'tagList',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        foundation = self.context.get('foundation', None)
        tags = validated_data.pop('tags', [])
        grant = Grant.objects.create(foundation=foundation, **validated_data)
        for tag in tags:
            grant.tags.add(tag)

        return grant

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
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
