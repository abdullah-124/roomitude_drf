from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken,TokenError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from account.models import User
from account.serializers import UserSerializer,RegisterSerializer,UserLoginSerializer, UserUpdateSerializer
from account.token import account_activation_token
from cart.serializers import CartItemSerializer
from wishlist.serializers import WishlistSerializer


# user registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    def create(self, request, *args, **kwargs):
        try:
            # Use the serializer’s own create() method
            print(request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()  # This calls your serializer's create()
            return Response(
                {
                    "text":f"Your account has been created. We have sent an email to {user.email}, please verify your account.",
                    "status": "success"
                    
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_409_CONFLICT)

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
            user_serializer = UserSerializer(user, context={'request':request})
            user_data = user_serializer.data
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
        serializer = UserLoginSerializer(data=request.data, context={'request':self.request})
        try:
            serializer.is_valid(raise_exception=True)
            # validated_data returns the user object (from your serializer)
            user = serializer.validated_data  
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            cart = CartItemSerializer(user.cart_items.all().select_related('product'), many=True, context={'request': self.request})
            wishlist = WishlistSerializer(user.wishlist_items.all().select_related('product'), many=True, context={'request': self.request})
        except Exception as e:
            return Response(
                {"message": str(e.detail)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data,
            'cart': cart.data,
            'wishlist': wishlist.data,
        },status=status.HTTP_200_OK)
# 
    
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]  # requires valid access token

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# USER UPDATE VIEW
class UserUpdateView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # allows FormData uploads
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                user = serializer.save()  # save updates
                print(user)
                # Serialize updated user instance to send back
                updated_user_serializer = UserSerializer(user)
                return Response({
                    'user': updated_user_serializer.data,
                    'message': {'text': 'Profile updated successfull', "status":'success'}
                }, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)