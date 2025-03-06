import rest_framework.routers

from custom_auth.api import viewsets

router = rest_framework.routers.SimpleRouter()
router.register("user", viewsets.UserViewSet)

