from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PdfViewSet

router = DefaultRouter()
router.register(r'', PdfViewSet, basename='pdf')

urlpatterns = [
    path('', include(router.urls)),
]
