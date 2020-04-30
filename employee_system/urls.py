from django.conf.urls import url,include
from rest_framework import routers
from employee_system.views import EmployeeViewSet, LeaveViewSet

router = routers.SimpleRouter()
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'leave', LeaveViewSet, basename='leave')
urlpatterns = [
    url(r'^', include(router.urls)),
]