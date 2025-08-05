from django.conf import settings
from rest_framework import serializers
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

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
        token = str(RefreshToken.for_user(user).access_token)
        verify_url = f"http://localhost:8000/api/account/verify-email/?token={token}"

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
