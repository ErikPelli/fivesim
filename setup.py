from setuptools import setup, find_packages

setup(
    name='5sim',
    version='1.0.0',
    description='Python API client for 5sim.net',
    url='https://github.com/ErikPelli/5sim',
    author='Erik Pellizzon',
    author_email='erikpellizzon@gmail.com',
    license='MIT',
    keywords=[
        'number',
        'telephone-numbers',
        '5sim',
        'fivesim',
        'python-5sim'
    ],
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Typing :: Typed',
    ],
)