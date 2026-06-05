# Project overview

TurboEnv is a Python package designed to facilitate the manipulation of environment files and environment variables in any Python project.

* The source code is available under the [src/turboenv](src/turboenv) directory and contains three main modules: `main`, `exceptions`, and `typings`.

# Commands

## Environment setup

* Create a virtual environment using `uv` ([uv documentation](https://docs.astral.sh/uv/)): `uv venv .venv`
* Sync the dependencies: `uv sync` then `uv lock` (if you want to update the lock file)
* Activate the virtual environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)

## Build

* Build the package: `uv build`
* Check the version of the package with: `uv version`

# Code style guidelines

* Use the latest Python version 3.x and the latest PEP 8 style guide for Python code ([PEP 8](https://www.python.org/dev/peps/pep-0008/)).

# Testing instructions

* Run the tests: `pytest`

# Security considerations

* 
