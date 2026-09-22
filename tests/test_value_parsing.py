import base64

import pytest

from turboenv.main import TurboEnv


@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("AGE", 30),
        ("AGE_INVALID", "some age"),
        ("AGE_NONE_EXISTENT", None)
    ]
)
def test_integer_valid(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    if env_value == "AGE_INVALID":
        with pytest.raises(ValueError):
            instance.integer(env_value)
    else:
        assert instance.integer(env_value) == expected

@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("BOOL_ENV_TRUE", True),
        ("BOOL_ENV_FALSE", False),
        ("BOOL_ENV_1", True),
        ("BOOL_ENV_0", False),
        ("BOOL_ENV_EMPTY", ""),
        ("BOOL_ENV_NONE_EXISTENT", None)
    ]
)
def test_bool_valid(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    if expected is None:
        assert instance.boolean(env_value) is expected
    elif expected == "":
        with pytest.raises(ValueError):
            instance.boolean(env_value)
    else:
        assert instance.boolean(env_value) is expected


@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("STR_ENV", "Hello, World!"),
        ("NON_EXISTENT_ENV", "DefaultValue")
    ]
)
def test_str(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    assert instance.string(env_value, default=expected) == expected


@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("HOSTS", ["A", "B", "C"]),
        ("NON_EXISTENT_ENV", None),
        ("HOSTS_SINGLE", ["A"]),
        ("HOSTS_INVALID_FORMAT", ["A - B % C"]),
    ]
)
def test_array(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    result = instance.array(env_value)
    if expected is None:
        assert result is None
    else:
        assert result is not None
        assert result == expected

@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("HOSTS", ["A", "B", "C"]),
    ]
)
def test_str_list(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()
    assert instance.str_list(env_value) == expected

    for item in expected:
        assert item in instance.str_list(env_value)


@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("HOSTS_NUM", [1, 2, 3]),
    ]
)
def test_int_list(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()
    assert instance.int_list(env_value) == expected

    for item in expected:
        assert isinstance(item, int)


def test_get():
    instance = TurboEnv()
    instance.load_envs()
    value = instance.get("BOOL_ENV")
    assert isinstance(value, str)


def test_secret():
    instance = TurboEnv()
    instance.load_envs()

    secret = base64.b64encode(b'my_secret_password').decode('utf-8')
    instance(DB_PASSWORD=secret)

    secret_value = instance.secret("DB_PASSWORD")
    assert secret_value == "my_secret_password"


@pytest.mark.parametrize(
    "description,env_value,expected",
    [
        ("No cast", "DATABASE_CONFIG", {
            "HOST": "localhost",
            "PORT": "5432",
            "USER": "admin",
            "PASSWORD": "secret"
        }),
        ("With cast", "DATABASE_CONFIG", {
            "HOST": "localhost",
            "PORT": 5432,
            "USER": "admin",
            "PASSWORD": "secret"
        }),
    ]
)
def test_dict(description, env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    if description == "With cast":
        config = instance.json(env_value, cast_values={"port": int})
        assert config == expected
    else:
        config = instance.json(env_value)
        assert config == expected


@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("API_ENDPOINTS", ["https://api.example.com", "https://api.example.org"]),
        ("API_ENDPOINTS_INVALID", []),
        ("API_ENDPOINTS_INSECURE", []),
    ]
)
def test_url_list(env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    if env_value == "API_ENDPOINTS_INSECURE":
        with pytest.raises(ValueError):
            assert instance.url_list(env_value, secured=True)
    elif env_value == "API_ENDPOINTS_INVALID":
        with pytest.raises(ValueError):
            assert instance.url_list(env_value)
    else:
        assert instance.url_list(env_value) == expected

        for item in expected:
            assert item in instance.url_list(env_value)


@pytest.mark.parametrize(
    "env_value,expected",
    [
        ("PATH_ENV", "temp_file.txt"),
        ("PATH_ENV_NON_EXISTENT", "fake-path")
    ]
)
def test_path(tmp_path, env_value, expected):
    instance = TurboEnv()
    instance.load_envs()

    if env_value == "PATH_ENV_NON_EXISTENT":
        with pytest.raises(FileNotFoundError):
            instance.path(env_value)
    else:
        # Create a temporary file
        temp_file = tmp_path / "temp_file.txt"
        temp_file.write_text("Hello, World!")

        # Set the environment variable to the path of the temporary file
        instance(**{env_value: str(temp_file)})

        path_value = instance.path(env_value)
        assert path_value == tmp_path / expected
