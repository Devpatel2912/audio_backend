from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Pdf
from .serializers import PdfSerializer, FolderPdfUploadSerializer
from folders.serializers import FolderSerializer

class PdfViewSet(viewsets.ModelViewSet):
    serializer_class = PdfSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']

    def get_queryset(self):
        user = self.request.user
        queryset = Pdf.objects.filter(user=user)
        
        folder = self.request.query_params.get('folder')
        if folder:
             queryset = queryset.filter(folder_id=folder)
        else:
             # Default: show root PDFs? Or all?
             # AudioListView shows root if no folder provided.
             # "if folder_id: ... else: filter(folder__isnull=True)"
             queryset = queryset.filter(folder__isnull=True)
             
        return queryset
    
    # Actually, let's stick to standard filtering. Client should send folder__isnull=True if they want root.
    # But usually clients just want "List everything in folder X".
    # And "List everything at Root" -> folder=null.

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_single(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='upload-multiple')
    def upload_multiple(self, request):
        serializer = FolderPdfUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            response_data = {
                'folder': FolderSerializer(result['folder']).data if result['folder'] else None,
                'uploaded_pdfs': PdfSerializer(result['uploaded_pdfs'], many=True).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
