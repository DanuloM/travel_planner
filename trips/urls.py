from rest_framework_nested import routers
from .views import TravelProjectViewSet, PlaceViewSet

router = routers.DefaultRouter() # type: ignore
router.register(r'projects', TravelProjectViewSet, basename='project')

projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'places', PlaceViewSet, basename='project-places')

urlpatterns = router.urls + projects_router.urls