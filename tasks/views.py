from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from braces.views import LoginRequiredMixin
from .models import Task, Job


class TaskViewSet(LoginRequiredMixin, ModelViewSet):
    """Task model view set"""
    model = Task


class JobViewSet(LoginRequiredMixin, ModelViewSet):
    """Job model view set"""
    model = Job


class RepositoryViewSet(LoginRequiredMixin, ViewSet):
    """Repository view set"""
    allowed_methods = ['GET']

    def list(self, request: Request, *args, **kwargs) -> Response:
        """List available repositories"""
        request.user
        return Response([{'a': 1}])
