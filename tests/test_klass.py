from src.main import turbo, Value, TurboEnv, _load_file
import pathlib


def test_load_file():
    result = _load_file(pathlib.Path('.env'))
    with result as lines:
        assert isinstance(lines, list)


class TestTurboEnv:
    def test_implementation(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        assert len(instance._cache.keys()) > 0

    def test_implementation_with_only(self):
        instance = TurboEnv(only="BOOL_")
        instance.load_envs('.env')

        for key in instance._cache.keys():
            assert key.startswith("BOOL_") or key == "BOOL_"

    def test_implementation_with_call(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        instance(RANDOM_VALUE="123")

        assert instance._cache.get("RANDOM_VALUE") == "123"

    def test_call(self):
        instance = turbo()

    def test_bool_valid(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.bool("BOOL_ENV") is True
        assert instance.bool("BOOL_ENV_2") is True

    def test_bool_invalid(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        try:
            instance.bool("AGE")
        except ValueError as e:
            assert str(e) == "Value for AGE is not a valid boolean: 30"

    def test_str(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.str("STR_ENV") == "Hello, World!"
        assert instance.str("NON_EXISTENT_ENV",
                            default="DefaultValue") == "DefaultValue"

    def test_list(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.list("HOSTS") == ["A", "B", "C"]

    def test_list_with_validation(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        def validate_host(host: str) -> bool:
            return host in ["A", "B", "C"]

        assert instance.list("HOSTS", validate=validate_host) == [
            "A", "B", "C"]

    def test_str_list(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.str_list("HOSTS") == ["A", "B", "C"]

    def test_exists(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.exists("BOOL_ENV") is True
        assert instance.exists("NON_EXISTENT_ENV") is False

    def test_get(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        value = instance.get("BOOL_ENV")
        assert isinstance(value, Value)

    def test_namespace(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        namespace = instance.namespace("TEST_NAMESPACE")
        assert isinstance(namespace, TurboEnv)


def test_value_klass():
    value = turbo.str("test")
    assert value == "TurboEnv"
