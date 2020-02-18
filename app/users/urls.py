from django.urls import path

from users import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = "users"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
