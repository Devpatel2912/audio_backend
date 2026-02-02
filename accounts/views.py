from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP
import random
from .serializers import UserRegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register(request):
    print(f"Server: Register attempt with data: {request.data}")
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    print(f"Server: Register failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    print(f"Server: Login attempt with data: {request.data}")
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response(
            {'error': 'Please provide both email and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'Account is inactive'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    user = authenticate(username=email, password=password)
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    otp_code = str(random.randint(100000, 999999))
    
    # Delete old OTPs for this email to prevent clutter and potential reuse issues
    OTP.objects.filter(email=email).delete()
    
    OTP.objects.create(email=email, otp_code=otp_code)
    
    # Send email
    subject = 'Your Login OTP'
    message = f'Your OTP for login is {otp_code}. It expires in 10 minutes.'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")
        return Response({'error': 'Failed to send OTP email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def verify_otp(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp')
    
    if not email or not otp_code:
        return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        otp_entry = OTP.objects.filter(email=email).last()
        if not otp_entry:
             return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
             
        if otp_entry.otp_code != otp_code:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not otp_entry.is_valid():
            return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
            
        # OTP is valid, log the user in
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete used OTP
        otp_entry.delete()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from audios.models import Audio
from audios.serializers import AudioSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecentItemsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_audios = Audio.objects.filter(user=request.user).order_by('-created_at')[:3]
        return Response({
            'audios': AudioSerializer(recent_audios, many=True, context={'request': request}).data
        })
