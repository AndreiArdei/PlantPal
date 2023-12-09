from setuptools import setup

setup(
    name='plantpal-control',
    version='0.0.1',
    packages=['plantpal', 'plantpal.input', 'plantpal.output'],
    install_requires=[
        'gpiozero==1.6.2',
        'smbus2==0.4.1'
    ]
)
