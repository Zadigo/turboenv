import pathlib

import pytest

from src.turboenv.exceptions import ConditionalError
from src.turboenv.main import Conditionals, TurboEnv


async def test_conditional_instance():
    instance = TurboEnv()
    instance(
        REDIS_URL='redis://localhost:6379',
        REDIS_USERNAME='user',
        REDIS_PASSWORD='pass'
    )

    instance = Conditionals(instance, 'REDIS_URL')

    try:
        return_value = instance.depends_on(
            ['REDIS_USERNAME', 'REDIS_PASSWORD']
        )
    except Exception as e:
        assert isinstance(e, Exception)

    assert isinstance(return_value, Conditionals)


async def test_conditional_fails():
    instance = TurboEnv()
    instance(REDIS_URL='redis://localhost:6379')

    instance = Conditionals(instance, 'REDIS_URL')

    try:
        instance.depends_on(['REDIS_USERNAME', 'REDIS_PASSWORD'])
    except Exception as e:
        assert isinstance(e, Exception)


class TestToBe:
    @pytest.mark.parametrize(
        'testcase,value',
        [
            (
                'valid', 'redis://localhost:6379'
            ),
            (
                'invalid', 'redis://invalid:6379'
            )
        ]
    )
    async def test_to_be_condition(self, instance_fixture: TurboEnv, testcase, value):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        if testcase == 'valid':
            instance.to_be(value)
        else:
            with pytest.raises(ConditionalError ):
                instance.to_be(value)


class TestNotToBe:
    @pytest.mark.parametrize(
        'testcase,value',
        [
            (
                'valid', 'redis://invalid:6379'
            ),
            (
                'invalid', 'redis://localhost:6379'
            )
        ]
    )
    async def test_not_to_be_condition(self, instance_fixture: TurboEnv, testcase, value):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        if testcase == 'valid':
            instance.not_to_be(value)
        else:
            with pytest.raises(ConditionalError):
                instance.not_to_be(value)


class TestToExist:
    @pytest.mark.parametrize(
        'testcase,value',
        [
            (
                'valid', 'REDIS_URL'
            ),
            (
                'invalid', 'REDIS_URL_INVALID'
            )
        ]
    )
    async def test_to_exist_condition(self, instance_fixture: TurboEnv, testcase, value):
        instance = Conditionals(instance_fixture, value)

        if testcase == 'valid':
            instance.to_exist()
        else:
            with pytest.raises(ConditionalError):
                instance.to_exist()


class TestToNotBeEmpty:
    @pytest.mark.parametrize(
        'testcase,value',
        [
            (
                'valid', 'REDIS_URL'
            ),
            (
                'invalid', 'EMPTY_VAR'
            )
        ]
    )
    async def test_not_empty(self, instance_fixture: TurboEnv, testcase, value):
        instance = Conditionals(instance_fixture, value)

        if testcase == 'valid':
            instance.to_not_be_empty()
        else:
            with pytest.raises(ConditionalError):
                instance.to_not_be_empty()


class TestToContain:
    @pytest.mark.parametrize(
        'testcase,value',
        [
            (
                'valid', 'localhost'
            ),
            (
                'invalid', 'invalid'
            )
        ]
    )
    async def test_contains(self, instance_fixture: TurboEnv, testcase, value):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        if testcase == 'valid':
            instance.to_contain(value)
        else:
            with pytest.raises(ConditionalError):
                instance.to_contain(value)


CURRENT_PATH = pathlib.Path(__file__).parent

class TestPathToExist:
    @pytest.mark.parametrize(
        'testcase,value',
        [
            (
                'valid', CURRENT_PATH
            ),
            (
                'invalid', CURRENT_PATH.joinpath('invalid')
            )
        ]
    )
    async def test_path_exists(self, instance_fixture: TurboEnv, testcase, value):
        instance_fixture(SOME_PATH=str(value))
        instance = Conditionals(instance_fixture, 'SOME_PATH')

        if testcase == 'valid':
            instance.path_to_exist()
        else:
            with pytest.raises(FileNotFoundError):
                instance.path_to_exist()
