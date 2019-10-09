from rest_framework import serializers

from conduit.apps.profiles.serializers import ProfileSerializer

from .models import Foundation, Tag
from .relations import TagRelatedField


class FoundationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()  # TODO: Not sure if this should be read_only
    description = serializers.CharField(required=False)

    # TODO: Update to List of Profiles!!!
    grantees = serializers.CharField(required=False)

    tagList = TagRelatedField(many=True, required=False, source='tags')

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    followed = serializers.SerializerMethodField()
    followersCount = serializers.SerializerMethodField(
        method_name='get_followers_count'
    )

    founder = ProfileSerializer(read_only=True)

    # TODO: Serialize grantees field in Foundation? Maybe need to create smth like TagRelatedField

    class Meta:
        model = Foundation
        fields = (
            'name',
            'description',
            'createdAt',
            'founder',
            'grantees',
            'followed',
            'followersCount',
            'tagList',
            'updatedAt',
        )

    def create(self, validated_data):
        founder = self.context.get('founder', None)
        tags = validated_data.pop('tags', [])
        foundation = Foundation.objects.create(
            founder=founder, **validated_data)

        for tag in tags:
            foundation.tags.add(tag)

        return foundation

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_followed(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        return request.user.profile.is_following_foundation(instance)

    def get_followers_count(self, instance):
        return instance.followed_by.count()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

    def to_representation(self, obj):
        return obj.tag
