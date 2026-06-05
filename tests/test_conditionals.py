from src.turboenv.main import TurboEnv, Conditionals
import pytest
import pathlib


async def test_conditional_success():
    instance = TurboEnv()
    instance(
        REDIS_URL='redis://localhost:6379',
        REDIS_USERNAME='user',
        REDIS_PASSWORD='pass'
    )

    instance = Conditionals(instance, 'REDIS_URL')
    try:
        instance.depends_on(['REDIS_USERNAME', 'REDIS_PASSWORD'])
    except Exception as e:
        assert isinstance(e, Exception)


async def test_conditional_fails():
    instance = TurboEnv()
    instance(REDIS_URL='redis://localhost:6379')

    instance = Conditionals(instance, 'REDIS_URL')
    try:
        instance.depends_on(['REDIS_USERNAME', 'REDIS_PASSWORD'])
    except Exception as e:
        assert isinstance(e, Exception)


@pytest.fixture
def instance_fixture():
    instance = TurboEnv()
    instance(REDIS_URL='redis://localhost:6379')
    return instance


class TestToBe:
    async def test_is_valid(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        try:
            instance.to_be('redis://localhost:6379')
        except Exception as e:
            assert isinstance(e, Exception)

    async def test_is_invalid(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        try:
            instance.to_be('redis://invalid:6379')
        except Exception as e:
            assert isinstance(e, Exception)


class TestNotToBe:
    async def test_is_valid(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        instance.not_to_be('redis://@localhost:6379')

    async def test_is_invalid(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        try:
            instance.not_to_be('redis://localhost:6379')
        except Exception as e:
            assert isinstance(e, Exception)


class TestToExist:
    async def test_exists(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        instance.to_exist()

    async def test_does_not_exist(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'MISSING_VAR')
        try:
            instance.to_exist()
        except Exception as e:
            assert isinstance(e, Exception)


class TestToNotBeEmpty:
    async def test_not_empty(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        instance.to_not_be_empty()

    async def test_empty(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'EMPTY_VAR')
        try:
            instance.to_not_be_empty()
        except Exception as e:
            assert isinstance(e, Exception)


class TestToContain:
    async def test_contains(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        instance.to_contain('localhost')

    async def test_does_not_contain(self, instance_fixture: TurboEnv):
        instance = Conditionals(instance_fixture, 'REDIS_URL')
        try:
            instance.to_contain('invalid')
        except Exception as e:
            assert isinstance(e, Exception)


class TestPathToExist:
    async def test_path_exists(self, instance_fixture: TurboEnv):
        instance_fixture(SOME_PATH=pathlib.Path(__file__))
        instance = Conditionals(instance_fixture, 'SOME_PATH')
        instance.path_to_exist()

    async def test_path_does_not_exist(self, instance_fixture: TurboEnv):
        instance_fixture(NON_EXISTENT_PATH=pathlib.Path('/non/existent/path'))
        instance = Conditionals(instance_fixture, 'NON_EXISTENT_PATH')
        try:
            instance.path_to_exist()
        except Exception as e:
            assert isinstance(e, Exception)
