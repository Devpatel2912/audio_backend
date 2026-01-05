from rest_framework import generics, status
from rest_framework.response import Response
import os
from .models import Audio
from .serializers import AudioSerializer, AudioUpdatePositionSerializer
from folders.models import Folder
from folders.serializers import FolderSerializer


class AudioUploadView(generics.CreateAPIView):
    serializer_class = AudioSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AudioListView(generics.ListAPIView):
    serializer_class = AudioSerializer

    def get_queryset(self):
        user = self.request.user
        folder_id = self.request.query_params.get('folder', None)
        queryset = Audio.objects.filter(user=user)
        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
        else:
            queryset = queryset.filter(folder__isnull=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Filter out audios where file does not exist
        valid_audios = []
        for audio in queryset:
            try:
                if audio.audio_file and os.path.exists(audio.audio_file.path):
                    valid_audios.append(audio)
            except Exception:
                # If path access fails (e.g. storage issue), skip it
                continue
        
        page = self.paginate_queryset(valid_audios)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(valid_audios, many=True)
        return Response(serializer.data)


class AudioDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AudioSerializer

    def get_queryset(self):
        return Audio.objects.filter(user=self.request.user)


class AudioUpdatePositionView(generics.UpdateAPIView):
    serializer_class = AudioUpdatePositionSerializer

    def get_queryset(self):
        return Audio.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions

class AudioUploadMultipleView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):

        folder_id = request.data.get('folder')
        folder_name = request.data.get('folder_name')

        if not folder_id and not folder_name:
             return Response({"error": "Folder ID or Folder Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        files = request.FILES.getlist('audio_files')
        if not files:
            return Response({"error": "No audio files provided"}, status=status.HTTP_400_BAD_REQUEST)

        if len(files) > 10:
            return Response({"error": "You can only upload up to 10 audio files at a time."}, status=status.HTTP_400_BAD_REQUEST)

        if folder_id:
             try:
                 folder = Folder.objects.get(id=folder_id, user=request.user)
             except Folder.DoesNotExist:
                 return Response({"error": "Folder not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
             folder = Folder.objects.create(name=folder_name, user=request.user)

        uploaded_audios = []
        for file in files:
            title = file.name if file.name else 'Audio File'
            audio = Audio.objects.create(
                title=title,
                audio_file=file,
                user=request.user,
                folder=folder
            )
            uploaded_audios.append(audio)

        folder_data = FolderSerializer(folder).data
        audio_data = AudioSerializer(uploaded_audios, many=True).data

        return Response({
            "folder": folder_data,
            "uploaded_audios": audio_data
        }, status=status.HTTP_201_CREATED)

