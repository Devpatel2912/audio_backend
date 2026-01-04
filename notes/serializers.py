from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'audio', 'pdf', 'note_text', 'audio_timestamp', 'page_number', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_audio(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only add notes to your own audios.")
        return value

    def validate_pdf(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only add notes to your own pdfs.")
        return value


class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'audio', 'pdf', 'note_text', 'audio_timestamp', 'page_number', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate_audio(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only add notes to your own audios.")
        return value

    def validate_pdf(self, value):
        if value and value.user != self.context['request'].user:
            raise serializers.ValidationError("You can only add notes to your own pdfs.")
        return value

