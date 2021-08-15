from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register('', views.UsersViewSet)
router.register('create', views.CreateUserViewSet)
# router.register('add-image-at-registration', views.ImageUserUpdateViewSet)
