from rest_framework import routers
from django.urls import URLPattern, path 
from django.conf.urls import include
from .views import FunderViewSet, LoanOptionViewSet, LoanAppViewSet, FundOptionViewSet, FundAppViewSet, LoanerViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('FundOptions', FundOptionViewSet)
router.register('FundApplications', FundAppViewSet)
router.register('LoanOptions', LoanOptionViewSet)
router.register('LoanApplications', LoanAppViewSet)
router.register('Loaner', LoanerViewSet)
router.register('Funder', FunderViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]