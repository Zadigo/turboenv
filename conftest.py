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
os.environ.setdefault("DOMAINS", "example.com,example.org")

os.environ.setdefault("AGE", "30")
os.environ.setdefault("AGE_INVALID", "thirty")

os.environ.setdefault("DATABASE_CONFIG", "host=localhost,port=5432,user=admin,password=secret")

os.environ.setdefault("REDIS_OTHER_URL", "redis://localhost:6379")

os.environ.setdefault("API_ENDPOINTS", "https://api.example.com,https://api.example.org")
os.environ.setdefault("API_ENDPOINTS_INVALID", "google")
os.environ.setdefault("API_ENDPOINTS_INSECURE", "http://google.com")

os.environ.setdefault("PATH_ENV", "temp_file.txt")

os.environ.setdefault("URL_ENV", "https://example.com")


@pytest.fixture
def instance_fixture():
    from src.turboenv.main import TurboEnv

    instance = TurboEnv()
    instance.load_envs()
    
    return instance


@pytest.fixture
def env_file_fixture(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "BOOL_ENV_TRUE=True\n"
        "BOOL_ENV_FALSE=False\n"
        "BOOL_ENV_1=1\n"
        "BOOL_ENV_0=0\n"
        "BOOL_ENV_EMPTY=\n"
        "STR_ENV=\"Hello, World!\"\n"
        "HOSTS=A,B,C\n"
        "HOSTS_SINGLE=A\n"
        "HOSTS_INVALID_FORMAT=\"A - B % C\"\n"
        "HOSTS_NUM=1,2,3\n"
        "AGE=30\n"
        "AGE_INVALID=thirty\n"
        "DATABASE_CONFIG=host=localhost,port=5432,user=admin,password=secret\n"
        "REDIS_OTHER_URL=redis://localhost:6379\n"
        "API_ENDPOINTS=https://api.example.com,https://api.example.org\n"
        "API_ENDPOINTS_INVALID=google\n"
        "API_ENDPOINTS_INSECURE=http://google.com\n"
        "PATH_ENV=temp_file.txt\n"
        "URL_ENV=https://example.com\n"
    )

    return env_file
