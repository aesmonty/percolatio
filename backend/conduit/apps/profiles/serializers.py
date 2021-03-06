from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.SerializerMethodField(method_name='get_bio')
    image = serializers.SerializerMethodField(
        method_name='get_image')

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image',)
        read_only_fields = ('username',)

    def get_bio(self, obj):
        if obj.bio:
            return obj.bio
        return None

    def get_image(self, obj):
        if obj.image:
            return obj.image
        return None
