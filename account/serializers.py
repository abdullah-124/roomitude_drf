from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from account.token import account_activation_token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone_number')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        self.send_verification_email(user)
        return user
    # send verification mail
    def send_verification_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        # localhost5173 is frontend part where user made the registration and frontend will make a request when user click on this link from his email 
        verify_url = f"http://localhost:5173/verify_email/?uid={uid}&token={token}"

        subject = "Verify Your Roomitude Account"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        context = {
            'user': user,
            'verify_url': verify_url,
            'project_name': "Roomitude",
            'support_email': "mdabdullahsakib124@gamil.com",
        }

        html_content = render_to_string("emails/verify_email.html", context)
        text_content = f"Please verify your email by visiting: {verify_url}"

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# user serializer for sending user data to the user account
class UserSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = User
        exclude = ['password']

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return f"{settings.BASE_URL}{obj.profile_image.url}"
        return None
    
# USER UPDATE SERIALIZER
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'profile_image', 'address', 'phone_number','date_of_birth' ]


# user login serializer

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
    # recive 
    # {"username":"admin", "password":"password"}
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        # Authenticate
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user_data,
        }
