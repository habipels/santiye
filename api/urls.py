from django.urls import path
from . import views
app_name = "api"
urlpatterns = [#
 path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
 path('dashboard/', views.homepage_api, name='homepage-api'),
]
#
