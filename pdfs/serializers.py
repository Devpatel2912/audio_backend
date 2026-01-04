from rest_framework import serializers
from .models import Pdf
from folders.models import Folder

class PdfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pdf
        fields = ['id', 'title', 'pdf_file', 'folder', 'user', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class FolderPdfUploadSerializer(serializers.Serializer):
    folder_name = serializers.CharField(max_length=255, required=False)
    folder = serializers.IntegerField(required=False)
    pdf_files = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    def validate(self, attrs):
        if not attrs.get('folder') and not attrs.get('folder_name'):
             # If no folder ID and no folder Name, maybe upload to root?
             # For now require at least one or root logic.
             # Actually Audio allows root.
             pass
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        folder_id = validated_data.get('folder')
        folder_name = validated_data.get('folder_name')
        pdf_files = validated_data.get('pdf_files')

        if folder_id:
            folder = Folder.objects.get(id=folder_id, user=user)
        elif folder_name:
            folder = Folder.objects.create(name=folder_name, user=user, folder_type='pdf')
        else:
            folder = None

        created_pdfs = []
        for file in pdf_files:
            pdf = Pdf.objects.create(
                title=file.name,
                pdf_file=file,
                folder=folder,
                user=user
            )
            created_pdfs.append(pdf)

        return {
            'folder': folder,
            'uploaded_pdfs': created_pdfs
        }
