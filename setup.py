from setuptools import setup, find_packages

setup(
    name="alarm",
    version="0.1",
    packages=find_packages(),
    package_data={
        'alarm': ['*.txt']
    },
    install_requires=['appscript'],
    author="Raymond Zeng",
    description="Command line alarm clock hooked into iTunes",
    keywords="itunes",
    url="https://github.com/raymondzneg/alarm-cli",
    entry_points={
        'console_scripts': [
            'alarm = alarm.alarm:main'
        ]
    }
)
