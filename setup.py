from setuptools import setup

setup(
    name='dtreeplacement-web',
    version='0.1',
    packages=['dtreeplacement-web'],
    url='https://github.com/Renophaston/dtreeplacement-web',
    license='The MIT License (MIT)',
    author='Renophaston',
    author_email='',
    description='Third attempt at a replacement for the way I use Treeline, web-interface',
    zip_safe=False,
    install_requires=['Flask','SQLAlchemy']
)
