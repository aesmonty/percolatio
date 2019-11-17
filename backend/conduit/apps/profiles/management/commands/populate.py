from django.core.management.base import BaseCommand
from conduit.apps.profiles.models import Profile

from conduit.apps.profiles.models import Profile
from django_fakery import factory


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def createUser(self):
        obj = factory.m(Profile)()
        print(obj)

    def handle(self, *args, **options):
        self.createUser()
