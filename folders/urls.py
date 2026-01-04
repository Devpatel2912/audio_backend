from django.urls import path
from .views import FolderCreateView, FolderListView, FolderDetailView

urlpatterns = [
    path('create/', FolderCreateView.as_view()),
    path('list/', FolderListView.as_view()),
    path('<int:pk>/', FolderDetailView.as_view()),
]
