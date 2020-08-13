from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from trippit_backend.api.serializers import UserSerializer

class UserViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
