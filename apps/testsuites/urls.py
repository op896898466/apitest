from rest_framework import routers

from .views import TestsuitesViewSet

router = routers.DefaultRouter()
router.register(r'testsuites', TestsuitesViewSet)

urlpatterns = [

]
urlpatterns += router.urls
