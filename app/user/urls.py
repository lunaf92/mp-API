from django.urls import path
from django.conf.urls import include
from .views import CreateUserView

app_name = "user"

urlpatterns = [path("create/", CreateUserView.as_view(), name="create")]
