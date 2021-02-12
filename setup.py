from setuptools import setup

setup(
    name="KillOrphanProcess",
    version="1.0",
    py_modules=['killorphanprocess'],
    install_requires=[
        'Click',
        'psutil'
    ],
    entry_points='''
         [console_scripts]
         killorphanprocess=killorphanprocess:cli
    ''',


)