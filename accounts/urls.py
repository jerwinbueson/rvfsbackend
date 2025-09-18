from django.urls import path
from .views import (CSRFTokenView, 
LoginView, 
LogoutView, 
AuthCheckView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf/', CSRFTokenView.as_view(), name='csrf'),
    path('auth-check/', AuthCheckView.as_view(), name='auth-check'),
]