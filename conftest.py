import pytest


@pytest.fixture
def instance_fixture():
    from src.turboenv.main import TurboEnv
    instance = TurboEnv()
    instance(REDIS_URL='redis://localhost:6379')
    return instance
