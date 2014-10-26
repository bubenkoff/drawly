"""Setuptools entry point."""
from setuptools import setup


setup(
    name='drawly',
    install_requires=[
        'setuptools',
    ],
    entry_points={'console_scripts': [
        'manage=manage:manager.run',
    ]},
)
