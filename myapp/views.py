# Create your views here.
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Image, SubscriptionPlan
from .serializers import UserSerializer, ImageSerializer, SubscriptionPlanSerializer,RegisterSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ImageViewSet(viewsets.ModelViewSet):
    print('heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeey')
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsBetaPlayer]
        return super().get_permissions()

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

# Custom permission classes for role-based access
class IsBetaPlayer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'beta_player'

class IsCompanyUserOrGrowthSubscriber(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['company_user', 'growth_plan_subscriber']
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]