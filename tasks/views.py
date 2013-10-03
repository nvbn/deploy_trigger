import json
from rest_framework import status
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from .models import Task, Job
from .jobs import perform_job


class TaskViewSet(LoginRequiredMixin, ModelViewSet):
    """Task model view set"""
    model = Task

    def get_queryset(self):
        """Return only user owned tasks"""
        return self.model.objects.filter(
            user=self.request.user,
        )


class JobViewSet(LoginRequiredMixin, ModelViewSet):
    """Job model view set"""
    model = Job

    def get_queryset(self):
        """Return only user owned tasks"""
        return self.model.objects.filter(
            task__user=self.request.user,
        )


class RepositoryViewSet(LoginRequiredMixin, ViewSet):
    """Repository view set"""
    allowed_methods = ['GET']

    def list(self, request: Request, *args, **kwargs) -> Response:
        """List available repositories"""
        github_user = request.user.github.get_user()
        avatar = github_user.avatar_url
        return Response([
            {
                'name': repo.full_name,
                'avatar': avatar,
            }
            for repo in github_user.get_repos('owner')
        ])


class JobTriggerViewSet(ViewSet):
    """Job trigger view set"""
    allowed_methods = ['POST']

    def create(self, request: Request, *args, **kwargs):
        """Create job by trigger"""
        try:
            task = Task.objects.get(name=self._get_repository(request))
        except Task.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        self._trigger_job(task)
        return Response({}, status=status.HTTP_201_CREATED)

    def _get_repository(self, request: Request) -> str:
        """Get repository name"""
        return '{}/{}'.format(
            request.DATA['repository']['owner']['name'],
            request.DATA['repository']['name'],
        )

    def _trigger_job(self, task: Task):
        """Trigger task job"""
        job = Job.objects.create(
            task=task,
            triggered=Job.TRIGGERED_PUSH,
        )
        perform_job.delay(job.id)
