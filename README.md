# Turbo Env

TurboEnv is a Python library that provides a simple and efficient way to manage environment variables in your applications. It allows you to easily load environment variables from .env files, access them in your code, and handle different environments (development, testing, production) with ease.

## Installation

```python

```

## Loading Environment variables

## Automatic detection 

When the class is first called, it looks for any `.env` located in the absolute path of the file that is calling it. If it finds one, it loads the environment variables from that file in the `default` namespace.

```python
from turboenv import TurboEnv

env = TurboEnv()
print(env.default)  # Access the default namespace
```
