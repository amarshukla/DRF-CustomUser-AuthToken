from django.conf.urls import url
from django.urls import include, path

from .views.users import UserCreateAPIView, UserLoginAPIView

urlpatterns = [
    url(r'^users/register/$', UserCreateAPIView.as_view(), name='user-register'),
    url(r'^rest-auth/', include('rest_auth.urls')),
]
