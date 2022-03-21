from setuptools import setup, find_packages

setup(
    name='aleatorpy',
    author='Gabriel Van Zandycke',
    author_email="gabriel.vanzandycke@hotmail.com",
    url="https://github.com/gabriel-vanzandycke/pseudo_random",
    licence="LGPL",
    python_requires='>=3.6',
    description="",
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
)
