from rest_framework.viewsets import ModelViewSet
from braces.views import LoginRequiredMixin
from .models import Task, Job


class TaskViewSet(LoginRequiredMixin, ModelViewSet):
    """Task model view set"""
    model = Task


class JobViewSet(LoginRequiredMixin, ModelViewSet):
    """Job model view set"""
    model = Job
