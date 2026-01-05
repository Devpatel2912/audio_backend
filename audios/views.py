from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics, status
import os
from .models import Audio
from .serializers import AudioSerializer, AudioUpdatePositionSerializer
from folders.models import Folder
from folders.serializers import FolderSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_audio(request):
    file = request.FILES.get('audio')
    title = request.data.get('title', 'Audio')
    duration = request.data.get('duration', 0.0)
    folder_id = request.data.get('folder')

    if not file:
        return Response({'error': 'No audio file provided. Key must be "audio".'}, status=400)

    folder = None
    if folder_id:
        try:
            folder = Folder.objects.get(id=folder_id, user=request.user)
        except Folder.DoesNotExist:
            pass # Or return error

    audio = Audio.objects.create(
        file=file,
        title=title,
        duration=duration,
        user=request.user,
        folder=folder
    )
    
    serializer = AudioSerializer(audio)
    return Response(serializer.data, status=201)

# Keeping list view but adapting
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
                # 'file' is the new field name
                if audio.file and os.path.exists(audio.file.path):
                    valid_audios.append(audio)
            except Exception:
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


# Assuming user doesn't need upload_multiple right now or it needs manual fix too
# Disabling upload_multiple temporarily or adapting?
# Let's adapt it to use manual create for safety
class AudioUploadMultipleView(generics.CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        folder_id = request.data.get('folder')
        folder_name = request.data.get('folder_name')

        files = request.FILES.getlist('audio_files') # Frontend sends 'audio_files' here? Or 'audio'?
        # Let's support both
        if not files:
             files = request.FILES.getlist('audio')

        if not files:
            return Response({"error": "No audio files provided"}, status=status.HTTP_400_BAD_REQUEST)

        # ... (Rest of logic adapted to 'file' field)
        
        if folder_id:
             try:
                 folder = Folder.objects.get(id=folder_id, user=request.user)
             except Folder.DoesNotExist:
                 return Response({"error": "Folder not found"}, status=status.HTTP_404_NOT_FOUND)
        elif folder_name:
             folder = Folder.objects.create(name=folder_name, user=request.user)
        else:
            folder = None

        uploaded_audios = []
        for f in files:
            title = f.name if f.name else 'Audio File'
            audio = Audio.objects.create(
                title=title,
                file=f, # Changed from audio_file
                user=request.user,
                folder=folder
            )
            uploaded_audios.append(audio)

        folder_data = FolderSerializer(folder).data if folder else None
        audio_data = AudioSerializer(uploaded_audios, many=True).data

        return Response({
            "folder": folder_data,
            "uploaded_audios": audio_data
        }, status=status.HTTP_201_CREATED)

