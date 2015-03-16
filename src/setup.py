# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='atlantis',
    version='0.1',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries',
    ],
    description='Smart furniture framework.',
    extras_require={
        'test': ['fixtures2'],
    },
    install_requires=[
        'decorated',
        'inflection',
        'loggingd',
        'metaweb >= 1.4',
        'mqueue',
    ],
    packages=[
        'atlantis',
        'atlantis.core',
        'atlantis.views',
    ],
    package_data={
        'atlantis': ['templates/*.html'],
    },
    url='https://github.com/CooledCoffee/atlantis/',
)
