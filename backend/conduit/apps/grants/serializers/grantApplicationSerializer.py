from rest_framework import serializers

from conduit.apps.profiles.serializers import ProfileSerializer

from ..models import GrantApplication
from ..relations import TagRelatedField


class GrantApplicationSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = GrantApplication
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):

        if self.context['grant'] is None:
            raise ValueError(
                'grant should be in the context when creating a grant application')

        if self.context['author'] is None:
            raise ValueError(
                'author should be in the context when creating a grant application')

        grant = self.context['grant']
        author = self.context['author']

        return GrantApplication.objects.create(
            author=author, grant=grant, **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
