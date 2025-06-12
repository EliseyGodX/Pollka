from django.urls import path
from users.views import UserAccountView, UserRegistrationView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('account/', UserAccountView.as_view(), name='account')
]
