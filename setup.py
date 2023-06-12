# SPDX-FileCopyrightText: 2022 Manuel Weiss <manuel.weiss@bht-berlin.de>
#
# SPDX-License-Identifier: MIT

# https://stackoverflow.com/a/60740179
# (note that even with pyproject.toml this is still useful to make `python setup.py sdist` work out-of-the-box)
from setuptools import dist

dist.Distribution().fetch_build_eggs(["Cython", "numpy"])

import site
import sys
from distutils.command.sdist import sdist
from distutils.errors import DistutilsExecError

import numpy as np
from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

# import eigency

# workaround for develop mode (pip install -e) with PEP517/pyproject.toml cf. https://github.com/pypa/pip/issues/7953
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]


ext_modules = cythonize(
    [Extension(
        "digit_interface.low_level_api",
        sources=[
            "digit_interface/low_level_api.pyx",
        ],
        libraries = ["digit_interface/cpp/libartl/libartl.a",],
        extra_compile_args=["-O0", "-pipe", "-v"],
        language="c++",
        extra_objects=["digit_interface/cpp/libartl/libartl.a"],
    ),
    ]
)
# if sys.platform == "linux":
#     ext_modules[0].extra_compile_args += ["-std=c++17"]
#     ext_modules[0].extra_link_args += ["-std=c++17"]

class make_libartl(sdist):
    def run(self):
        print("Running custom sdist command to build libartl")
        try:
            self.spawn(["make", "digit_interface/cpp/libartl"]) 
            self.spawn(["-C libartl libartl.a", "digit_interface/cpp/"])
        except DistutilsExecError:
            self.warn("Failed to run cmake")
        # run the default build_ext command
        sdist.run(self)



for m in ext_modules:
    m.include_dirs.insert(0, np.get_include())

setup(
    name="digit_interface",
    version="0.0.1",
    description="Digit robot interface package",
    # long_description=open("README.rst").read(),
    # long_description_content_type="text/x-rst",
    # url="https://github.com/dlaidig/vqf/",
    # project_urls={
    #     "Documentation": "https://vqf.readthedocs.io/",
    # },
    author="Manuel Weiss",
    author_email="manuel.weiss@bht-berlin.de",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    cmdclass={"sdist": make_libartl},
    package_data={
        "digit_interface": [
            "cpp/*.cpp",
            "cpp/*.hpp",
            "cpp/*.h",
            "cpp/*.c",
            "cpp/libartl/*.c",
            "cpp/libartl/*.h",
            "cpp/CMakeLists.txt",
        ]
    },
    zip_safe=False,
    install_requires=["numpy >= 1.23.2", "cython", "setuptools>=65.0.2"],
    python_requires=">=3.7",  # needed for dataclasses in PyVQF
    extras_require={
        # pip3 install --user -e ".[dev]"
        "dev": [
            "tox",
            "pytest",
            "flake8",  # https://github.com/tholo/pytest-flake8/issues/81
        ],
    },
    ext_modules=ext_modules,
    include_dirs=[
        np.get_include(),
    ]
)
