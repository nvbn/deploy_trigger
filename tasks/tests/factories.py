import factory
from accounts.tests.factories import UserFactory
from ..models import Task, Job


class TaskFactory(factory.DjangoModelFactory):
    """Task factory"""
    FACTORY_FOR = Task

    repository = factory.Sequence(lambda n: 'repository/{}'.format(n))
    user = factory.SubFactory(UserFactory)
    branch = factory.Sequence(lambda n: 'branch{}'.format(n))
    name = factory.Sequence(lambda n: 'name{}'.format(n))
    server = factory.Sequence(lambda n: 'server@host:{}'.format(n))
    script = factory.Sequence(lambda n: 'script{}'.format(n))


class JobFactory(factory.DjangoModelFactory):
    """Job factory"""
    FACTORY_FOR = Job

    task = factory.SubFactory(TaskFactory)
    triggered = Job.TRIGGERED_PUSH
