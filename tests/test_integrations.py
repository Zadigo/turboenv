import os
from subprocess import call
import pathlib


class TestWithDjangoIntegration:
    def test_django_integration(self):
        value = call([
            'python',
            str(pathlib.Path(__file__).parent.parent.joinpath('manage.py')),
            'check'
        ])
        assert value == 0
