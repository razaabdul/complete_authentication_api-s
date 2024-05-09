from rest_framework.routers import DefaultRouter
from .views import *

router=DefaultRouter()
router.register(r"user",Userview,basename="user")
urlpatterns = router.urls