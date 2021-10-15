from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('create', views.CreateGroupViewSet)
router.register('', views.GroupInformationViewSet)
