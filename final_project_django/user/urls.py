from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("user/",views.UserList.as_view()),
    path("user/token/",TokenObtainPairView.as_view()),
    path("user/refresh/",TokenRefreshView.as_view()),
]