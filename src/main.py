from typing import Callable, Generator
from src.typings import TypeAny
from collections import OrderedDict
import pathlib
from contextlib import contextmanager
from urllib.parse import urlparse


@contextmanager
def _load_file(path: pathlib.Path, encoding: str = 'utf-8') -> Generator[list[str], None, None]:
    with path.open(encoding=encoding) as f:
        lines = f.readlines()
        yield lines


class Value[T]:
    def __init__(self, value: T):
        self.value = value

    def depends_on(self, *args: str) -> "Value[T]":
        return self

    def failif(self, condition: Callable[[T], bool], message: str) -> "Value[T]":
        return self


class TurboEnv:
    """A class for managing environment variables with support for 
    loading from files, type casting, and conditional logic.

    Example usage:

        from src.main import TurboEnv

        env = TurboEnv()
        env.load_envs('.env')

        debug_mode = env.bool('DEBUG_MODE', default=False)
        database_url = env.str('DATABASE_URL')
        allowed_hosts = env.str_list('ALLOWED_HOSTS', default=[])

    Variables can separated by namespaces using the `namespace` method. Variables that do not specify a namespace 
    are loaded in the global namespace and are accessible directly from the main instance.

        from src.main import TurboEnv

        env = TurboEnv()
        env.load_envs(('test', '.env'), ('prod', '.env.prod'))   

        test_envs = env.namespace('test')
        database_url = test_envs.str('URL')
    """

    _cache: OrderedDict[str, TypeAny] = OrderedDict()

    def __init__(self, fail_on_missing: bool = False, only: str = None, skip_empty: bool = False):
        self.fail_on_missing = fail_on_missing
        self.only = only
        self.skip_empty = skip_empty

    def __call__(self, **defaults: TypeAny) -> "TurboEnv":
        self._cache.update(defaults)
        return self

    @classmethod
    def new(cls, **envs: TypeAny) -> "TurboEnv":
        instance = cls()
        instance._cache.update(envs)
        return instance

    def load_envs(self, *args: str):
        """Loads environment variables from the specified files. 
        If no files are specified, it defaults to loading from a 
        file named `.env` in the current directory.

        Arguments:
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

    def bool(self, name: str, default: bool = None) -> bool:
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

    def str(self, name: str, default: str = None) -> str:
        value = self._cache.get(name, None)
        if value is None:
            return str(default)
        return str(value)

    def list(self, name: str, default: list[str] = None, cast: Callable[[str], TypeAny] = str) -> list[str | int]:
        value = self._cache.get(name, None)
        if value is None:
            return default

        return [cast(item.strip()) for item in value.split(',')]

    def str_list(self, name: str, default: list[str] = None) -> list[str]:
        return self.list(name, default=default, cast=str)

    def int_list(self, name: str, default: list[int] = None) -> list[int]:
        return self.list(name, default=default, cast=int)

    def domain_list(self, name: str, default: list[str] = None) -> list[str]:
        domains = self.url_list(name, default=default)
        for domain in domains:
            parsed = urlparse(domain)
            if parsed.path and parsed.path != '/':
                raise ValueError(
                    f"Value for {name} is not a valid domain: {domain}")
        return domains

    def url_list(self, name: str, default: list[str] = None) -> list[str]:
        urls = self.list(name, default=default, cast=str)

        for url in urls:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(
                    f"Value for {name} is not a valid URL: {url}")
        return urls

    def exists(self, name: str) -> bool:
        return name in self._cache

    def get(self, name: str, default: TypeAny = None) -> Value:
        return Value(True)

    def namespace(self, name: str) -> "TurboEnv":
        return self.new(**self._namespace_cache(name))

    def conditional(self):
        return self


turbo = TurboEnv()
