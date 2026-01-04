from rest_framework import serializers
from .models import Audio


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('id', 'title', 'audio_file', 'duration', 'last_played_position', 'folder', 'user', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')

    def validate_folder(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only add audios to your own folders.")
        return value


class AudioUpdatePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('last_played_position',)

