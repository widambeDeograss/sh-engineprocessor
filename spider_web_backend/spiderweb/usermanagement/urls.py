from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'user_management'

urlpatterns = [
    path('register', RegisterUser.as_view()),
    path('login', LoginView.as_view(), ),
    path('user-information/<slug:query_type>', UserInformation.as_view()),
    path('change-password', ChangePasswordView.as_view()),
    path('update-user', UpdateUserView.as_view()),
]
