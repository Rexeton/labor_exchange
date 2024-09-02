from datetime import datetime

import factory
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from models import User


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Faker("pystr")
    name = factory.Faker("pystr")
    email = factory.Faker("pystr")
    is_company = factory.Faker("pybool")


class UserUpdateFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    name = factory.Faker("pystr")
    email = factory.Faker("pystr")
    is_company = factory.Faker("pybool")


class UserCreateFactory(factory.BaseDictFactory):
    class Meta:
        model = User

    name = factory.Faker("pystr")
    email = factory.Faker("pystr")
    password = factory.Faker("pystr")
    password2 = password
    is_company = factory.Faker("pybool")
