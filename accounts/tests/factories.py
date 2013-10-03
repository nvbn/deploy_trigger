import factory
from ..models import User


class UserFactory(factory.DjangoModelFactory):
    """User factory"""
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'user {}'.format(n))
