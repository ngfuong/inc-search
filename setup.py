from setuptools import setup, find_packages


def get_install_requires():
    with open('requirements.txt') as f:
        return [req.strip() for req in f]


setup(name='inc_search', version='1.0',
      install_requires=get_install_requires(), packages=find_packages())
