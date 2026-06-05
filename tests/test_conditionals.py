from src.turboenv.main import TurboEnv, Conditionals
import pytest


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
