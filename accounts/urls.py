from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login, UserProfileView, RecentItemsView, send_otp, verify_otp

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('send-otp/', send_otp, name='send-otp'),
    path('verify-otp/', verify_otp, name='verify-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('recent/', RecentItemsView.as_view(), name='recent-items'),
]

