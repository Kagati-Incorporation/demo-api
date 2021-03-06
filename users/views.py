from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserAuthTokenSerializer,
    UserSerializer,
    UserRegisterSerializer,
)

User = get_user_model()


class UserAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    http_method_names = ['get', 'put', 'patch', ]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_active', 'is_staff', ]
    search_fields = ['full_name', 'email', 'phone_number']

    @action(methods=['PUT'], detail=True, url_path='remove-admin-status')
    def remove_admin_status(self, request, pk):
        user = self.get_object()
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return Response(
            {
                'message': "Admin Status Removed"
            }, status.HTTP_202_ACCEPTED)

    @action(methods=['PUT'], detail=True, url_path='promote-to-admin')
    def promote_to_admin(self, request, pk):
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = False
        user.save()
        return Response(
            {
                'message': "Promoted to Admin"
            }, status.HTTP_202_ACCEPTED)

    @action(methods=['PUT'], detail=True, url_path='promote-to-superuser')
    def promote_to_superuser(self, request, pk):
        user = self.get_object()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return Response(
            {
                'message': "Promoted to Superuser"
            }, status.HTTP_202_ACCEPTED)


class UserProfileAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.none()
    http_method_names = ['get', 'put', 'patch', ]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def paginate_queryset(self, queryset):
        return None


class RegisterUserAPIView(APIView):
    """
    API View for registration.
    """
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = UserSerializer(user).data
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'Success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': data,
            },
            status.HTTP_201_CREATED
        )


class ObtainAuthTokenView(ObtainAuthToken):
    serializer_class = UserAuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            email = serializer.initial_data['username']
            user = get_object_or_404(User, email=email)
            if not user.is_active:
                return Response(
                    {
                        'message': 'You account is currently under review. It will be activated real soon by Homework Team.'
                    },
                    status.HTTP_200_OK
                )
        except:
            pass
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        return Response(
            {
                'message': 'Success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            },
            status.HTTP_200_OK
        )
