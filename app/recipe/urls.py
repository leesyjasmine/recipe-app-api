from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# default router will register appropriate url for all the actions
router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]