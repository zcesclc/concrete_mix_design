# setup.py
from setuptools import setup, find_packages

setup(
    name="concrete_mix_optimization",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scikit-learn',
        'deap',
        'matplotlib'
    ],
    python_requires='>=3.8',
)