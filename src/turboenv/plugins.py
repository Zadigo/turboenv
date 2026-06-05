from src.turboenv.typings import TypeTurboEnv

CACHE_SCHEMES = {
    'dbcache': 'django.core.cache.backends.db.DatabaseCache',
    'dummycache': 'django.core.cache.backends.dummy.DummyCache',
    'filecache': 'django.core.cache.backends.filebased.FileBasedCache',
    'locmemcache': 'django.core.cache.backends.locmem.LocMemCache',
    'memcache': 'django.core.cache.backends.memcached.MemcachedCache',
}


def django_plugin(instance: TypeTurboEnv):
    """A plugin for Django projects that loads environment variables from .env files 
    and sets them in the system environment.
    """


