from django.urls import path
from rest_api.account.views import EmailTokenObtainPairView, LoginView, LogoutView, SignUpView, UserListView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get-users/', UserListView.as_view(), name='get_users'),

    # path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),

    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
