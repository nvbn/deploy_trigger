from rest_framework import routers
from tasks.views import TaskViewSet, JobViewSet


router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('jobs', JobViewSet)
