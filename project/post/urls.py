from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet

app_name = "post"
default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(default_router.urls)),
]