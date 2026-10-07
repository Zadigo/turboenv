import pytest


def test_load_preset(instance_fixture):
    result = instance_fixture.presets.django.redis_url()
    assert result.startswith("redis://")


DJANGO_ENV_SETTINGS = pytest.mark.parametrize(
    'setting',
    [
        'DEBUG',
        'DEBUG_PROPAGATE_EXCEPTIONS',
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'EMAIL_USE_TLS',
        'EMAIL_USE_SSL',
        'EMAIL_SSL_CERTFILE',
        'EMAIL_SSL_KEYFILE',
        'EMAIL_TIMEOUT',
        'DEFAULT_FROM_EMAIL',
        'DISSALOWED_USER_AGENTS'
    ]
)


@DJANGO_ENV_SETTINGS
def test_django_preset_settings(setting, instance_fixture):
    match setting:
        case 'DEBUG':
            assert instance_fixture.presets.django.debug is not None
            assert instance_fixture.presets.django.debug
        case 'DEBUG_PROPAGATE_EXCEPTIONS':
            assert instance_fixture.presets.django.debug_propagate_exceptions is None
        case 'EMAIL_BACKEND':
            assert instance_fixture.presets.django.email_backend == ''
        case 'EMAIL_HOST':
            assert instance_fixture.presets.django.email_host == ''
        case 'EMAIL_PORT':
            assert instance_fixture.presets.django.email_port is None
        case 'EMAIL_HOST_USER':
            assert instance_fixture.presets.django.email_host_user == ''
        case 'EMAIL_HOST_PASSWORD':
            assert instance_fixture.presets.django.email_host_password == ''
        case 'EMAIL_USE_TLS':
            assert instance_fixture.presets.django.email_use_tls is None
        case 'EMAIL_USE_SSL':
            assert instance_fixture.presets.django.email_use_ssl is None
        case 'EMAIL_SSL_CERTFILE':
            assert instance_fixture.presets.django.email_ssl_certfile == ''
        case 'EMAIL_SSL_KEYFILE':
            assert instance_fixture.presets.django.email_ssl_keyfile == ''
        case 'EMAIL_TIMEOUT':
            assert instance_fixture.presets.django.email_timeout is None
        case 'DEFAULT_FROM_EMAIL':
            assert instance_fixture.presets.django.default_from_email == ''
        case 'DISSALOWED_USER_AGENTS':
            assert instance_fixture.presets.django.dissalowed_user_agents is None
        case _:
            pass

