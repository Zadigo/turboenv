
from turboenv.main import TurboEnvWithPresets


def test_load_preset(instance_fixture):
    d = TurboEnvWithPresets()

    result = d.django.redis_url()
    assert result.startswith("redis://")

