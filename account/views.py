from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout
from account.models import User

from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
# verify email 
# accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# user registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)

            if not user.is_active:
                user.is_active = True
                user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Email verified, login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        except Exception as e:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
    
