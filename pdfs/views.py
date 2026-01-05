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
        file = request.FILES.get('pdf')
        if not file:
            return Response({'error': 'No PDF file provided. Key must be "pdf".'}, status=400)

        title = request.data.get('title', file.name)
        folder_id = request.data.get('folder')
        
        from folders.models import Folder
        folder = None
        if folder_id:
             try:
                 folder = Folder.objects.get(id=folder_id, user=request.user)
             except Folder.DoesNotExist:
                 pass

        pdf = Pdf.objects.create(
            file=file,
            title=title,
            user=request.user,
            folder=folder
        )
        serializer = PdfSerializer(pdf)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='upload-multiple')
    def upload_multiple(self, request):
        # We can reuse FolderPdfUploadSerializer if updated, or allow manual handling like audio
        # Using Serializer is cleaner for multiple files if logic is complex, 
        # but manual is more robust against DRF parser confusion.
        
        folder_id = request.data.get('folder')
        folder_name = request.data.get('folder_name')
        
        files = request.FILES.getlist('pdf_files')
        if not files:
             files = request.FILES.getlist('pdf')
        
        if not files:
             return Response({"error": "No PDF files provided"}, status=status.HTTP_400_BAD_REQUEST)
             
        from folders.models import Folder
        folder = None
        if folder_id:
            try:
                folder = Folder.objects.get(id=folder_id, user=request.user)
            except Folder.DoesNotExist:
                return Response({'error': 'Folder not found'}, status=404)
        elif folder_name:
             folder = Folder.objects.create(name=folder_name, user=request.user, folder_type='pdf')

        created_pdfs = []
        for f in files:
            title = f.name
            pdf = Pdf.objects.create(
                title=title,
                file=f,
                user=request.user,
                folder=folder
            )
            created_pdfs.append(pdf)

        response_data = {
            'folder': FolderSerializer(folder).data if folder else None,
            'uploaded_pdfs': PdfSerializer(created_pdfs, many=True).data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            result = serializer.save()
            response_data = {
                'folder': FolderSerializer(result['folder']).data if result['folder'] else None,
                'uploaded_pdfs': PdfSerializer(result['uploaded_pdfs'], many=True).data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
