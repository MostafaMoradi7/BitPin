from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = "api"
urlpatterns = [
    path(
        "register/",
        views.UserRegistrationView.as_view(),
        name="user-register",
    ),
    path(
        "auth/",
        TokenObtainPairView.as_view(),
        name="token-obtain-pair",
    ),
    path(
        "contents/",
        views.CreateContentAPIView.as_view(),
        name="create-content",
    ),
    path(
        "contents/",
        views.ContentsListAPIView.as_view(),
        name="show-all-contents",
    ),
    path(
        "contents/<int:pk>/",
        views.ContentDetailAPIView.as_view(),
        name="show-content-detail",
    ),
    path(
        "vote/",
        views.VoteCreateUpdateView.as_view(),
        name="vote",
    ),
]
