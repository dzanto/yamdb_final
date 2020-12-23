from random import choice
from string import ascii_letters

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, api_view, permission_classes

from .models import User
from .permissions import SiteAdminPermission
from .serializers import UserSerializer
from django.conf import settings

generator = default_token_generator


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    email = request.data.get('email')
    user = get_object_or_404(User, email=email)
    code = request.data.get('confirmation_code')
    if generator.check_token(user, code):
        refresh = RefreshToken.for_user(user)
        tokens = {'refresh': str(refresh),
                  'access': str(refresh.access_token)}
        return Response(tokens, status.HTTP_200_OK)

    return Response({"message": "неверный код подтверждения."},
                    status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def email_confirmation(request):
    email = request.data.get('email')
    if not email:
        return Response(status.HTTP_400_BAD_REQUEST)

    user = User.objects.get_or_create(email=email)[0]
    if not user.username:
        user.username = 'User_' + ''.join(
            choice(ascii_letters) for i in range(6))
    username = user.username

    user.save()
    code = generator.make_token(user)

    send_mail(
        subject='Ваш код аутентификации в Yamdb',
        message='Сохраните код! Он понадобится вам для получения токена.\n'
                f'confirmation_code:\n{code}\n'
                f'username: {username}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return Response({"message": "код был отправлен на указанную почту: "
                                f"{email}"}, status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, SiteAdminPermission]

    def get_permissions(self):
        if self.action in ('profile', None):
            return [IsAuthenticated()]
        return super().get_permissions()

    def perform_update(self, serializer):
        serializer.save(data=self.request.data)

    @action(methods=['GET', 'PATCH'], detail=True)
    def profile(self, request):
        if request.method == 'PATCH':
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(email=user.email, role=user.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
