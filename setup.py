from setuptools import (
    setup,
    find_packages,
)

setup(
    name='loaded',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    maintainer='Julien Kauffmann',
    maintainer_email='julien.kauffmann@freelan.org',
    version=open('VERSION').read().strip(),
    description=(
        "A network-distributed, language-agnostic build agent."
    ),
    long_description="""\
Loaded creates a mesh of network-distributed build agents.
""",
    packages=find_packages(exclude=[
        'tests',
    ]),
    install_requires=[
        'six==1.9.0',
        'click==5.1',
        'colorama==0.3.3',
        'tornado==4.2.1',
        'voluptuous==0.8.7',
        'PyYAML==3.11',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'loaded = loaded.main:main_loaded',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
    ],
)
