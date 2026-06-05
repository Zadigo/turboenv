# Turbo Env

TurboEnv is a Python library that provides a simple and efficient way to manage environment variables in your applications. It allows you to easily load environment variables from .env files, access them in your code, and handle different environments (development, testing, production) with ease.

## Installation

```python

```

## Loading Environment variables

## Automatic detection 

When `load_envs` is first called, it looks for any `.env` located in the absolute path of the file that is calling it. If it finds one, it loads the environment variables from that file in the `default` namespace.

```python
from turboenv import TurboEnv

env = TurboEnv()
env.load_envs()
```

You can also specify the path to the `.env` file and the namespace you want to load it into.

```python
from turboenv import TurboEnv

env = TurboEnv()
env.load_envs('path/to/.env')

env.string('DB_USER')  # Accesses the DB_USER variable from the default namespace
```

## Accessing Environment Variables

Once the environment variables are loaded, you can access them in multiple different manners including typecasting their values to a specific one:

### Get method

Tries to get the value of the environment variable with the given name. If the variable is not found, an `exceptions.MissingEnvVariableError` is raised.

```python
db_user = env.get("DB_USER")
db_password = env.get("DB_PASSWORD")
```

### Boolean method

Returns the boolean value of the environment variable with the given name:

```python
db_password = env.boolean("USE_DB")
```

### String method

Returns the string value of the environment variable with the given name:

```python
db_password = env.string("DB_PASSWORD")
```

### Array method

Returns a list of strings by splitting the value of the environment variable with the given name using a specified separator (default is comma):

```python
allowed_hosts = env.array("ALLOWED_HOSTS", cast=str)
```

### String List method

Returns a list of strings by splitting the value of the environment variable with the given name using a specified separator (default is comma):

```python
allowed_hosts = env.str_list("ALLOWED_HOSTS")
```

### Interget List method

Returns a list of integers by splitting the value of the environment variable with the given name using a specified separator (default is comma):

```python
allowed_ports = env.int_list("ALLOWED_PORTS")
```

### Domain List method

Returns a list of domain names by splitting the value of the environment variable with the given name using a specified separator (default is comma):

```python
allowed_domains = env.domain_list("ALLOWED_DOMAINS")
```

### URL List method

Returns a list of URLs by splitting the value of the environment variable with the given name using a specified separator (default is comma):

```python
allowed_urls = env.url_list("ALLOWED_URLS")
```


### Secret method

Returns the value of the environment variable with the given name, decoded from base64:

```python
db_password = env.secret("DB_PASSWORD")
```

### Random Value

Returns a random value of the specified type. Supported types are: `string`, `integer`, `boolean`, `array`, `domain`, and `url`.

```python
random_string = env.random_value("string")
```

## Conditionals

Conditionals are used to guarantee the integrity of your environment variables by checking if they meet certain conditions. If the conditions are not met, an exception is raised.

### Depends On

Requires certain environment variables to be set in order for the application to run.

```python
env.conditional("DB_USER").depends_on(values=["DB_PASSWORD"])
```

### To Be

Requires the value of the environment variable to be equal to a specified value.

```python
env.conditional("DB_USER").to_be("admin")
```

### Not To Be

Requires the value of the environment variable to not be equal to a specified value.

```python
env.conditional("DB_PASSWORD").not_to_be("password")
```

### To Exist

Requires the environment variable to be present.

> Note
> This does not check if the value of the environment variable is empty or not, it only checks if it is present in the environment.

```python
env.conditional("DB_USER").to_exist()
```

### To Not Be Empty

Requires the value of the environment variable to not be empty.

```python
env.conditional("DB_PASSWORD").to_not_be_empty()
```

### To Contain 

Requires the value of the environment variable to contain a specified substring.

```python
env.conditional("ALLOWED_HOSTS").to_contain("example.com")
```

### Path To Exist

Requires the value of the environment variable to be a valid path that exists in the file system.

```python
env.conditional("CONFIG_PATH").path_to_exist()
```
