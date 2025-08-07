from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken,TokenError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import User
from account.serializers import UserSerializer,RegisterSerializer,UserLoginSerializer
from account.token import account_activation_token



# user registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# verify email 
class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        uid = request.GET.get('uid')
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)

            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

            refresh = RefreshToken.for_user(user)
            # serialize user data
            user_data = UserSerializer(user).data
            return Response({
                "message": "Email verified, login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh), 
                "user": user_data,
            })

        except Exception as e:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


# USER LOGIN VIEW
class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # requires valid access token

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # marks the refresh token as invalid
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)