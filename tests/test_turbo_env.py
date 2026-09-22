import os
import pathlib

import pytest

from src.turboenv.main import TurboEnv, _load_file, expand


def test_load_file():
    result = _load_file(pathlib.Path('.env'))
    with result as lines:
        assert isinstance(lines, list)


@pytest.mark.parametrize(
    "testcase,expected",
    [
        (
            "without casting",
            {
                "HOST": "localhost",
                "PORT": "5432",
                "USER": "admin",
                "PASSWORD": "secret"
            }
        ),
        (
            "with casting",
            {
                "HOST": "localhost",
                "PORT": 5432,
                "USER": "admin",
                "PASSWORD": "secret"
            }
        )
    ]
)
def test_dict(testcase, expected):
        instance = TurboEnv()
        instance(DATABASE_CONFIG="host=localhost,port=5432,user=admin,password=secret")

        if testcase == "with casting":
            result = instance.json("DATABASE_CONFIG", cast_values={"port": int})
            assert result == expected
        else:
            result = instance.json("DATABASE_CONFIG")
            assert result == expected

def test_new_class_method():
    instance = TurboEnv.new(DATABASE_URL="postgres://localhost")
    assert instance._cache.get("DATABASE_URL") == "postgres://localhost"


def test_domain_list():
    instance = TurboEnv()
    instance.load_envs('.env')

    result = instance.domain_list("DOMAINS")
    assert result == ["example.com", "example.org"]

def test_url_list():
    instance = TurboEnv()
    instance.load_envs('.env')
    
    result = instance.url_list("URLS")
    assert result == ["http://api.example.com", "https://api.example.org"]


def test_url_list_secured():
    instance = TurboEnv()
    instance.load_envs('.env')
    
    with pytest.raises(ValueError):
        instance.url_list("URLS", secured=True)

        
class TestTurboEnv:
    def test_implementation(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        assert len(instance._cache.keys()) > 0
        assert len(instance._files) == 0
        assert not instance.has_files
        assert instance.fail_on_missing is False
        assert instance.skip_empty is False

    def test_implementation_with_call(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        instance(RANDOM_VALUE="123")

        assert instance._cache.get("RANDOM_VALUE") == "123"

    def test_caching(self):
        instance = TurboEnv()

        for _ in range(2):
            instance.load_envs('.env')


class TestExceptions:
    def test_bool_invalid_exception(self):
        instance = TurboEnv()
        instance.load_envs('.env')
        try:
            instance.boolean("AGE")
        except ValueError as e:
            assert str(e) == "Value for AGE is not a valid boolean: 30"

    def test_list_invalid_exception(self):
        instance = TurboEnv()
        instance.load_envs('.env')

        try:
            instance.str_list("HOSTS")
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
            instance.boolean("AGE")
        except ValueError as e:
            assert str(e) == "Value for AGE is not a valid boolean: 30"


def test_loaded_in_system_variables():
    instance = TurboEnv()
    instance.load_envs('.env')

    assert os.getenv("BOOL_ENV") == "True"


def test_expand():
    instance = TurboEnv()
    instance.load_envs('.env')

    expanded_value = expand(instance, "DICT_ENV_FROM_ENV")
    assert expanded_value is not None
    assert expanded_value == 'host=localhost,port=5432,user=admin,password=secret'
