# Python Virtual Enivorment Creator

Creates a virtual environment for Python.

## Installing And Build

```sh
git clone https://github.com/isacolak/python-venvcrtr
cd python-venvcrtr
python make.py
```

### Usage

Help

```sh
venvcrtr -h
```

Returns list of python executables

```sh
venvcrtr -pyl
```

Returns list of python versions

```sh
venvcrtr -pyvl
```

Example of creating a simple venv

```sh
venvcrtr venv
```

Example of creating a simple venv with a different executable

```sh
venvcrtr venv -py {executable_path}
```

Example of creating a simple venv with a different version

```sh
venvcrtr venv -pyv {version}
```

Example of creating a simple venv with libraries

```sh
venvcrtr venv python-switch ...
```
