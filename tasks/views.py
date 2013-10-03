from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from .models import Task, Job


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
