from rest_framework import serializers
from .models import YoutubeFeed


# This function serializes the YoutubeFeed model, all fields
class YoutubeFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeFeed
        fields = '__all__'
