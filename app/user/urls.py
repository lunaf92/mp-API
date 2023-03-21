from django.urls import path
from django.conf.urls import include
from .views import CreateUserView, CreateTokenView

app_name = "user"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("token/", CreateTokenView.as_view(), name="token"),
]
