from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from users import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', views.UserView.as_view(), name="signup"),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="users_id"),
    path("achieve/<int:achieve_id>/", views.AchievementView.as_view(), name="achievement"),
]
