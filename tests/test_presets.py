
from turboenv.presets import EnvironmentPresets


def test_load_preset(instance_fixture):
    d = EnvironmentPresets(instance_fixture)

    result = d.django.redis_url()
    assert result.startswith("redis://")

