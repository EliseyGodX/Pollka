from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import UserAccountSerializer, UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserAccountView(RetrieveAPIView):
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
