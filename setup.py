from setuptools import setup, find_packages

setup(
    name="ccv",
    version="0.0.5",

    description='FFI bindings to libccv',
    long_description=open('README.md').read(),
    url='https://github.com/gpip/py-ccv',
    author='Guilherme Polo',
    author_email='gp@instaprint.me',

    setup_requires=['cffi>=1.3.0', 'pytest-runner==2.6.2'],
    install_requires=['cffi>=1.3.0'],
    tests_require=['pytest==2.8.7'],
    extras_require={
        'util': ['Pillow==3.2.0']
    },

    packages=find_packages(),
    cffi_modules=[
        "build_wrapper.py:ffi"
    ],
    zip_safe=False,

    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries"
    ]
)
