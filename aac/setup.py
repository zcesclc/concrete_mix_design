from setuptools import setup, find_packages

setup(
    name="aac_mix_optimization",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.23.5",
        "pandas>=1.5.3",
        "scikit-learn>=1.0.2",
        "deap>=1.3.1", 
        "matplotlib>=3.5.0",
    ],
    python_requires=">=3.9",
)
