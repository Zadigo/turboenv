import os

import pytest

os.environ.setdefault("BOOL_ENV_TRUE", "True")
os.environ.setdefault("BOOL_ENV_FALSE", "False")
os.environ.setdefault("BOOL_ENV_1", "1")
os.environ.setdefault("BOOL_ENV_0", "0")
os.environ.setdefault("BOOL_ENV_EMPTY", "")

os.environ.setdefault("STR_ENV", "Hello, World!")

os.environ.setdefault("HOSTS", "A,B,C")
os.environ.setdefault("HOSTS_SINGLE", "A")
os.environ.setdefault("HOSTS_INVALID_FORMAT", "A - B % C")
os.environ.setdefault("HOSTS_NUM", "1,2,3")

os.environ.setdefault("AGE", "30")
os.environ.setdefault("AGE_INVALID", "thirty")

os.environ.setdefault("DATABASE_CONFIG", "host=localhost,port=5432,user=admin,password=secret")

os.environ.setdefault("REDIS_URL", "redis://localhost:6379")

os.environ.setdefault("API_ENDPOINTS", "https://api.example.com,https://api.example.org")
os.environ.setdefault("API_ENDPOINTS_INVALID", "google")
os.environ.setdefault("API_ENDPOINTS_INSECURE", "http://google.com")

os.environ.setdefault("PATH_ENV", "temp_file.txt")

@pytest.fixture
def instance_fixture():
    from src.turboenv.main import TurboEnv
    instance = TurboEnv()
    instance.load_envs()
    return instance
