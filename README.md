# Python Virtual Enivorment Creator

Creates a virtual environment for Python.

## Installing And Build

```sh
git clone https://github.com/isacolak/py-venvcrtr
cd py-venvcrtr
python make.py
```

### Usage

Help

```sh
py_venvcrtr -h
```

Returns list of python executables

```sh
py_venvcrtr -pyl
```

Returns list of python versions

```sh
py_venvcrtr -pyvl
```

Example of creating a simple venv

```sh
py_venvcrtr venv
```

Example of creating a simple venv with a different executable

```sh
py_venvcrtr venv -py {executable_path}
```

Example of creating a simple venv with a different version

```sh
py_venvcrtr venv -pyv {version}
```

Example of creating a simple venv with libraries

```sh
py_venvcrtr venv python-switch ...
```
