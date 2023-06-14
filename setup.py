from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="scr_constants",
    version="0.0.1",
    # py_modules = ['constants.py',],
    packages=['scr', 'constants'],
    # install_requires=requirements,
)
