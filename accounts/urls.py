from django.urls import path
from .views import (CSRFTokenView, 
LoginView, 
LogoutView, 
AuthCheckView,
UserProfileView,
CreateUserView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf/', CSRFTokenView.as_view(), name='csrf'),
    path('auth-check/', AuthCheckView.as_view(), name='auth-check'),
    path('users/me', UserProfileView.as_view(), name='user-profile'),
    path('users/create', CreateUserView.as_view(), name='create-user'),
]