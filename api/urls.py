from django.urls import path,include
from api.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns =[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register-user/', UserRegistrationView.as_view(), name='register'),
    path('login-user/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update-profile/', UserProfileUpdate.as_view(), name='update-profile'),
    path('user-change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('user-password-reset/', UserResetPasswordView.as_view(), name='user-password-reset'),

    path('top-companies/<company_type>/', TopCompaniesView.as_view(), name='top-companies'),
    path('delete-company/<slug>/', DeleteCompanyView.as_view(), name='delete-company'),
    path('add-company/', AddCompanyView.as_view(), name="add-company"),
    
]
