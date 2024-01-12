from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("logout/", views.UserLogoutView.as_view(), name="user_logout"),
    path("profile/", views.profile, name="profile"),
]
