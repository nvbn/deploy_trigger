from rest_framework import routers
from tasks.views import (
    TaskViewSet,
    JobViewSet,
    RepositoryViewSet,
    JobTriggerViewSet,
)


router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('jobs', JobViewSet)
router.register('repositories', RepositoryViewSet, base_name='Repository')
router.register('triggers', JobTriggerViewSet, base_name='Trigger')
