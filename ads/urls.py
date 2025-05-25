from django.urls import include, path
from rest_framework import routers
from ads.views import AdViewSet, ProposalViewSet

router = routers.DefaultRouter()
router.register(r'ads', AdViewSet)
router.register(r'exchanges', ProposalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
