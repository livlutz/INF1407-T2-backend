from django.urls import path
from accounts import views
from django.urls import include

app_name = 'accounts'

urlpatterns = [
    path('token-auth/', views.CustomAuthToken.as_view(), name='token-auth'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset/confirm/', views.CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),
]