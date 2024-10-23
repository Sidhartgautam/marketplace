from django.urls import path
from .views import HomeView, GetUserBalance,UserRegistrationView

urlpatterns = [
     path('home/', HomeView.as_view(), name='home'),
     path('balance/', GetUserBalance.as_view(), name='get_user_balance'),
      path('register/', UserRegistrationView.as_view(), name='user-register'),
]
