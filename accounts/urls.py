from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login, UserProfileView, RecentItemsView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('recent/', RecentItemsView.as_view(), name='recent-items'),
    path('api/folders/', include('folders.urls')),
]

