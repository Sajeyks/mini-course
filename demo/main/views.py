from .serializers import RegistrationSerializer, EmailVerificationSerializer, ResendVerificationEmailSerializer
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.urls import reverse
from .utils import Mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views
from django.conf import settings
import jwt

User = get_user_model()

# Create your views here.

class RegistrationView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        ####  Sending email
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site_domain = get_current_site(request).domain
        relativeLink = reverse('verify-email')

        verification_link = 'http://' + current_site_domain + relativeLink + "?token=" + str(token)
        message = ". Use the link below to verify your email.\n If you were not expecting any account verifivation email, please ignore this \n"
        email_body = "Hi " + user.email+ message + verification_link
        data = {'email_body': email_body,'to_email': user.email,
         'email_subject':'Demo Email Verification'}
        Mail.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerificationView(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
            return Response({'Email Succesfully verified'}, status = status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            

class ResendVerificationEmailView(views.APIView):
    serializer_class = ResendVerificationEmailSerializer

    def post(self, request):
        input = request.data
        Email = input['email']

        try:
            if  User.objects.filter(email=Email).exists:
                user = User.objects.get(email__exact=Email)
                token = RefreshToken.for_user(user).access_token
                current_site_domain = get_current_site(request).domain
                relativeLink = reverse('verify-email')
                verification_link = 'http://' + current_site_domain + relativeLink + "?token=" + str(token)
                message = ". Use the link below to verify your email.\n If you were not were not expecting any account verifivation email, please ignore this \n"
                email_body = "Hi " + Email+ message + verification_link
                data = {'email_body': email_body,'to_email': Email,
                'email_subject':'Demo Email Verification'}
                Mail.send_email(data)
                return Response({'Verification Email sent. Check your inbox.'}, status = status.HTTP_200_OK)
            
        except User.DoesNotExist as exc:
            return Response({'The email address does not not match any user account.'}, status = status.HTTP_400_BAD_REQUEST)
    
