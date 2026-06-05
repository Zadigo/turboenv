from typing import Callable, Generator, Optional
from src.turboenv.typings import TypeAny
from collections import OrderedDict
import pathlib
from contextlib import contextmanager
from urllib.parse import urlparse
from src.turboenv import exceptions
import os
import string
import random
import base64


@contextmanager
def _load_file(path: pathlib.Path, encoding: str = 'utf-8') -> Generator[list[str], None, None]:
    with path.open(encoding=encoding) as f:
        lines = f.readlines()
        yield lines


class Conditionals[T = TypeAny]:
    def __init__(self, instance: 'TurboEnv', name: T):
        self.instance = instance
        self._name = name

    def value(self) -> T:
        return self.instance._cache.get(self._name, None)

    def depends_on(self, values: list[str] = []) -> 'Conditionals[T]':
        """Blocks the execution of the code until the specified environment variables exist. 
        If any of the specified environment variables do not exist, it raises an ExceptionGroup 
        containing all the MissingEnvVariableError instances for the missing variables.

        A typical use case for this method is when you have environment variables that depend on each other,
        like in the case of a database URL that depends on the existence of a database host, port, username, and password.

        Example usage::

            from turboenv import TurboEnv
            env = TurboEnv()
            env.load_envs('.env')

            # This will block until the environment variables DB_HOST, DB_PORT, DB_USER, and DB_PASSWORD exist
            env.conditional('DATABASE_URL').depends_on(['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD'])

            env.string('DATABASE_URL')  # This will now work because the required environment variables exist

        Args:
            values (list[str]): A list of strings representing the names of the environment variables to check for existence.

        Raises:
            ExceptionGroup: If any of the specified environment variables do not exist, an ExceptionGroup is raised containing all the MissingEnvVariableError instances for the missing variables.
        """
        errors: list[exceptions.MissingEnvVariableError] = []
        for name in values:
            if not self.instance._exists(name):
                errors.append(exceptions.MissingEnvVariableError(name))

        if errors:
            variables = ', '.join(values)
            raise ExceptionGroup(
                f"{self._name} is missing one or many dependencies: {variables}", errors)

        return self

    def to_be(self, expected: T) -> 'Conditionals[T]':
        value = self.value()
        if value != expected:
            raise exceptions.ConditionalError(value, expected, "to be")
        return self

    def not_to_be(self, expected: T) -> 'Conditionals[T]':
        value = self.value()
        if value == expected:
            raise exceptions.ConditionalError(
                value, expected, "not to be")
        return self

    def to_exist(self) -> 'Conditionals[T]':
        value = self.value()
        if value is None:
            raise exceptions.ConditionalError(value, None, "exist")
        return self

    def to_not_be_empty(self) -> 'Conditionals[T]':
        value = self.value()
        if value is None or value == "":
            raise exceptions.ConditionalError(
                value, None, "not be empty")
        return self

    def to_contain(self, expected: T) -> 'Conditionals[T]':
        value = self.value()
        if not isinstance(value, (list, str)):
            raise TypeError(
                "Value must be a list or a string to use to_contain")

        value = self.value()
        if expected not in value:
            raise exceptions.ConditionalError(value, expected, "contain")
        return self

    def path_to_exist(self) -> 'Conditionals[T]':
        value = self.value()
        if not isinstance(value, (str, pathlib.Path)):
            raise TypeError(
                "Value must be a string or a pathlib.Path to use path_to_exist")

        value = self.value()
        if value is None:
            raise exceptions.ConditionalError(
                self._name, None, "exist as a path")

        path = pathlib.Path(value)
        if not path.exists():
            raise FileNotFoundError(
                f"Path from env variable {self._name} does not exist")
        return self


class NamespaceValues[T= OrderedDict[str, TypeAny]]:
    _cache: T = OrderedDict()

    def __init__(self, name: str, values: T):
        """
        Arguments:
            name (str): The name of the namespace.
            values (T): The values of the namespace.
        """
        self.name = name
        self._cache = values
        # ".env" file that was used to load the values
        # for this namespace, if any
        self.file: Optional[pathlib.Path] = None


class TurboEnv:
    """A class for managing environment variables with support for 
    loading from files, type casting, and conditional logic.

    Example usage:

        from src.main import TurboEnv

        env = TurboEnv()
        env.load_envs('.env')

        debug_mode = env.boolean('DEBUG_MODE', default=False)
        database_url = env.string('DATABASE_URL')
        allowed_hosts = env.str_list('ALLOWED_HOSTS', default=[])

    Variables can separated by namespaces using the `namespace` method. Variables that do not specify a namespace 
    are loaded in the global namespace and are accessible directly from the main instance.

        from src.main import TurboEnv

        env = TurboEnv()
        env.load_envs(('test', '.env'), ('prod', '.env.prod'))   

        test_envs = env.namespace('test')
        database_url = test_envs.str('URL')

    Args:
        fail_on_missing (bool): If True, raises a FileNotFoundError if any of the specified files do not exist. Defaults to False.
        only (str): If specified, only loads environment variables that start with this prefix. Defaults to None.
        skip_empty (bool): If True, skips empty lines in the environment files. Defaults to False.
    """

    _cache: OrderedDict[str, TypeAny] = OrderedDict()

    def __init__(self, fail_on_missing: bool = False, only: str = None, skip_empty: bool = False):
        self.only = only
        self.fail_on_missing = fail_on_missing
        self.skip_empty = skip_empty
        self._files: set[pathlib.Path] = set()

    def __call__(self, **defaults: TypeAny) -> "TurboEnv":
        self._cache.update(defaults)
        return self

    def __repr__(self) -> str:
        return f"TurboEnv(cache={len(self._cache)}, files={len(self._files)})"

    @property
    def has_files(self) -> bool:
        return len(self._files) > 0

    @classmethod
    def new(cls, **envs: TypeAny) -> "TurboEnv":
        instance = cls()
        instance._cache.update(envs)
        return instance

    def _exists(self, name: str) -> bool:
        """Checks if the specified environment variable exists in the cache.
        Used for internal checks and conditional logic."""
        return name in self._cache

    def load_envs(self, *args: str):
        """Loads environment variables from the specified files. 
        If no files are specified, it defaults to loading from a 
        file named `.env` in the current directory.

        Args:
            *args (str): A variable number of string arguments representing the file paths to load.

        Raises:
            FileNotFoundError: If `fail_on_missing` is set to True and any of the specified files do not exist.
        """
        if not args:
            args = ('.env',)

        for filename in args:
            path = pathlib.Path(filename)

            if self.fail_on_missing:
                if not path.exists():
                    raise FileNotFoundError(f"File {filename} does not exist")

            if path.exists():
                self._files.add(path)

                with _load_file(path) as lines:
                    for line in lines:
                        if line == "\n":
                            continue

                        # Set the values that we read from the
                        # file into the cache
                        key, value = line.strip().split('=', 1)

                        if self.only is not None:
                            if not key.startswith(self.only):
                                continue

                        self._cache[key] = value

            # Once the files are loaded, check the system environment
            # variables. They will override the values from the files
            # if they exists in the system environment.
            # for key, value in self._cache.items():
            #     if key in system_environ:
            #         self._cache[key] = system_environ[key]

            system_environ = os.environ
            skip_keys = list(system_environ.keys())
            # Set the environment variables from the cache into the system environment
            # This is necessary for the environment variables to be accessible from
            # the system environment,
            for key, value in self._cache.items():
                if key in skip_keys:
                    continue
                os.environ.setdefault(key, value)

            # In the specific case of Docker environments for example,
            # since .env files are not used, load all the environment variables
            # from the system environment if no files were specified and no files were loaded.
            for key, value in system_environ.items():
                self._cache[key] = value

    def get(self, name: str) -> TypeAny:
        """A strict version of the `get` method that raises a KeyError 
        if the specified environment variable does not exist."""
        try:
            return self._cache[name]
        except KeyError as e:
            raise exceptions.MissingEnvVariableError(name) from e

    def boolean(self, name: str, default: bool = None) -> bool:
        booleans = ['true', '1', 'yes', 'on', 'false', '0', 'no', 'off']

        value = self._cache.get(name, None)
        if value is None:
            return default

        if value.lower() in booleans[:4]:
            return True
        elif value.lower() in booleans[4:]:
            return False
        else:
            raise ValueError(
                f"Value for {name} is not a valid boolean: {value}")

    def string(self, name: str, default: str = None) -> str:
        value = self._cache.get(name, None)
        if value is None:
            return str(default)
        return str(value)

    def array(self, name: str, default: list[str] = None, cast_values: Callable[[str], TypeAny] = str) -> list[str | int]:
        """Returns a list of values for the given environment variable name. The values are 
        expected to be comma-separated in the environment variable.

        Args:
            name (str): The name of the environment variable to retrieve.
            default (list[str], optional): The default value to return if the environment variable is not set. Defaults to None.
            cast_values (Callable[[str], TypeAny], optional): A function to cast each value in the list. Defaults to str.
        """
        value = self._cache.get(name, None)
        if value is None:
            return default

        return [cast_values(item).strip() for item in value.split(',')]

    def str_list(self, name: str, default: list[str] = None) -> list[str]:
        """Returns a list of strings for the given environment variable name. 

        Example usage::

            from turboenv import TurboEnv

            env = TurboEnv()
            env.load_envs('.env')

            allowed_hosts = env.str_list('ALLOWED_HOSTS')
            # allowed_hosts will be a list of strings, e.g. ["localhost", "example.com"]

        Args:
            name (str): The name of the environment variable to retrieve.
            default (list[str], optional): The default value to return if the environment variable is not set. Defaults to None.
        """
        return self.array(name, default=default, cast_values=str)

    def int_list(self, name: str, default: list[int] = None) -> list[int]:
        """Returns a list of integers for the given environment variable name.

        Example usage::

            from turboenv import TurboEnv

            env = TurboEnv()
            env.load_envs('.env')

            port_numbers = env.int_list('PORT_NUMBERS')
            # port_numbers will be a list of integers, e.g. [80, 443, 8080]
        """
        return self.array(name, default=default, cast_values=int)

    def domain_list(self, name: str, default: list[str] = None) -> list[str]:
        """Returns a list of domains for the given environment variable name.

        Example usage::

            from turboenv import TurboEnv

            env = TurboEnv()
            env.load_envs('.env')

            allowed_domains = env.domain_list('ALLOWED_DOMAINS')
            # allowed_domains will be a list of domains, e.g. ["example.com", "example.org"]
        """
        domains = self.url_list(name, default=default)
        for domain in domains:
            parsed = urlparse(domain)
            if parsed.scheme and parsed.path:
                raise ValueError(
                    f"Value for {name} is not a valid domain: {domain}")
        return domains

    def url_list(self, name: str, default: list[str] = None) -> list[str]:
        """Returns a list of URLs for the given environment variable name.

        Example usage::

            from turboenv import TurboEnv

            env = TurboEnv()
            env.load_envs('.env')

            api_endpoints = env.url_list('API_ENDPOINTS')
            # api_endpoints will be a list of URLs, e.g. ["https://api.example.com", "https://api.example.org"]
        """
        urls = self.array(name, default=default, cast_values=str)

        for url in urls:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(
                    f"Value for {name} is not a valid URL: {url}")
        return urls

    def secret(self, name: str):
        """Returns the value of the specified secret environment variable. 
        The value is expected to be base64-encoded.

        Example usage::

            from turboenv import TurboEnv

            env = TurboEnv()
            env.load_envs('.env')

            db_password = env.secret('DB_PASSWORD')
            # db_password will be the decoded value of the DB_PASSWORD environment variable

        Args:
            name (str): The name of the secret environment variable to retrieve.

        Raises:
            ValueError: If the specified secret environment variable is not set or if its value is not a valid base64-encoded string.
        """
        value = self._cache.get(name, None)
        if value is None:
            raise ValueError(f"Secret {name} is not set")

        try:
            # Decode the value from base64
            decoded_value = base64.b64decode(value).decode('utf-8')
        except Exception as e:
            raise ValueError(
                f"Value for {name} is not a valid base64-encoded string: {value}") from e
        else:
            return decoded_value

    def random_value(self, name: str, is_secret: bool = False) -> str:
        """Create an environment variable with a random value.

        Example usage::

            from turboenv import TurboEnv

            env = TurboEnv()
            random_api_key = env.random_value('API_KEY', is_secret=True)
            # random_api_key will be a random string that is base64-encoded, e.g. "c29tZS1yYW5kb20tc3RyaW5n"
        """
        # To avoid regenerating the random value every time,
        # we can check if the value already exists in the cache
        if name in self._cache:
            return self._cache[name]

        random_value = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=32
            )
        )
        if is_secret:
            random_value = base64.b64encode(
                random_value.encode('utf-8')).decode('utf-8')

        self._cache[name] = random_value
        os.environ.setdefault(name.upper(), random_value)
        return random_value

    # def namespace(self, name: str) -> "TurboEnv":
    #     return self.new(**self._namespace_cache(name))

    def conditional(self, name: str):
        """
        Returns a Conditionals instance for the specified environment variable name, 
        allowing you to apply conditional logic on the value of the environment variable.

        Args:
            name (str): The name of the environment variable to apply the conditional logic on.
        """
        self.get(name)
        return Conditionals(self, name)
