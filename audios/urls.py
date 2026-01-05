from django.urls import path
from .views import upload_audio, AudioListView, AudioDetailView, AudioUpdatePositionView, AudioUploadMultipleView

urlpatterns = [
    path('', AudioListView.as_view(), name='audio-list'),
    path('upload/', upload_audio, name='audio-upload'),
    path('upload-multiple/', AudioUploadMultipleView.as_view(), name='audio-upload-multiple'),
    path('<int:pk>/', AudioDetailView.as_view(), name='audio-detail'),
    path('<int:pk>/position/', AudioUpdatePositionView.as_view(), name='audio-update-position'),
]

