# Digit Python Interface - Low-Level API Cython Wrapper

A lightweight Cython wrapper enabling Python integration for the Agility Digit Low-Level API.

## Installation

1. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv .venv
    source venv/bin/activate
    ```

1. Install the Agility Python SDK ([available through your ar-control simulator](http://localhost:8080/doc/software/jsonapi.html#python-sdk))

    ```bash
    pip install agility-1.1.4-py3-none-any.whl
    ```

1. Build the underlying C++ library (`libartl`):

    *Note: The `setup.py` uses a custom `sdist` command to trigger the Makefile for the agility lib. If you are not on Linux, please verify the location of the compiled library afterwards.*

    ```bash
    python3 setup.py sdist
    ```

    *(Alternatively, you can run the make command directly: `make -C digit_interface/cpp/libartl libartl.a`)*

1. Build and install the Digit Interface package:

    ```bash
    pip install -e .
    ```

    *Development Note: If you make changes to the `.pyx` files and need to manually recompile the Cython extensions in-place without reinstalling the whole package, you can run:*

    ```bash
    python3 setup.py build_ext --inplace
    ```
