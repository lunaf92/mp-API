from django.urls import path
from .views import CreateUserView, CreateTokenView, RetrieveUpdateSelfView

app_name = "user"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("token/", CreateTokenView.as_view(), name="token"),
    path("self", RetrieveUpdateSelfView.as_view(), name="self")
]
