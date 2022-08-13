from setuptools import setup, find_packages

import thtagger.ui

setup(
    name="thtagger",
    version=thtagger.ui.__version__,
    license="GPL2",
    description="A easy to use music metadata tagger",
    long_description="A easy to use music metadata tagger based on PySide6 and Mutagen",
    url="https://github.com/weilinfox/haku-thtagger",
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'requests',
        'mutagen',
        'PySide6'
    ],
)
