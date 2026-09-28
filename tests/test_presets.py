
from turboenv.main import TurboEnv


def test_load_preset(instance_fixture):
    d = TurboEnv()

    result = d.presets.django.redis_url()
    assert result.startswith("redis://")

