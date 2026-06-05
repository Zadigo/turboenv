from src.main import TurboEnv, _load_file
import pathlib
import base64


def test_load_file():
    result = _load_file(pathlib.Path('.env'))
    with result as lines:
        assert isinstance(lines, list)


class TestTurboEnv:
    def test_implementation(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        assert len(instance._cache.keys()) > 0
        assert len(instance._files) == 1
        assert instance.only is None
        assert instance.fail_on_missing is False
        assert instance.skip_empty is False

    def test_implementation_with_only(self):
        instance = TurboEnv(only="BOOL_")
        instance.load_envs('.env')

        for key in instance._cache.keys():
            assert key.startswith("BOOL_")

    def test_implementation_with_call(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        instance(RANDOM_VALUE="123")

        assert instance._cache.get("RANDOM_VALUE") == "123"

    def test_bool_valid(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.bool("BOOL_ENV") is True
        assert instance.bool("BOOL_ENV_2") is True

    def test_str(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.string("STR_ENV") == "Hello, World!"
        assert instance.string("NON_EXISTENT_ENV",
                               default="DefaultValue") == "DefaultValue"

    def test_array(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        assert instance.array("HOSTS") == ["A", "B", "C"]

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
        assert isinstance(value, bool)

    def test_secret(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        secret = base64.b64encode(b'my_secret_password').decode('utf-8')
        instance(DB_PASSWORD=secret)

        secret_value = instance.secret("DB_PASSWORD")
        assert secret_value == "my_secret_password"

    # def test_namespace(self):
    #     instance = TurboEnv()
    #     instance.load_envs('.env')
    #     namespace = instance.namespace("TEST_NAMESPACE")
    #     assert isinstance(namespace, TurboEnv)


class TestExceptions:
    def test_bool_invalid_exception(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        try:
            instance.bool("AGE")
        except ValueError as e:
            assert str(e) == "Value for AGE is not a valid boolean: 30"

    def test_list_invalid_exception(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        try:
            instance.list("HOSTS", cast=str)
        except ValueError as e:
            assert str(
                e) == "Value 'D' in HOSTS is not valid according to the provided validation function."

    def test_file_not_found_exception(self):
        instance = TurboEnv()
        try:
            instance.load_envs('non_existent_file.env')
        except FileNotFoundError as e:
            assert str(e) == "File non_existent_file.env not found."

    def test_bool_invalid(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        try:
            instance.bool("AGE")
        except ValueError as e:
            assert str(e) == "Value for AGE is not a valid boolean: 30"
