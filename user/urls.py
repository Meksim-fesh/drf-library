from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user.views import CreateUserView, ManageUserView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="user-create"),
    path("me/", ManageUserView.as_view(), name="user-manage"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

app_name = "user"
