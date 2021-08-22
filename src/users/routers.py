from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register('me', views.MeUserInformationVewSet)
router.register('create', views.CreateUserViewSet)
router.register('', views.UsersViewSet)
