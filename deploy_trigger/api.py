from rest_framework import routers
from tasks.views import TaskViewSet, JobViewSet, RepositoryViewSet


router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('jobs', JobViewSet)
router.register('repositories', RepositoryViewSet, base_name='Repository')
