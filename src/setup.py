# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='atlantis',
    version='0.1',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
    ],
    description='Decorator framework and common decorators for python.',
    extras_require={
        'test': ['fixtures'],
    },
    install_requires=[
    ],
    packages=[
        'atlantis',
        'atlantis.views',
    ],
    url='https://github.com/CooledCoffee/decorated/',
)
