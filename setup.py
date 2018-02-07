import importlib
from setuptools import find_packages, setup

package = 'quartermaster'
meta = importlib.import_module('.meta', package)

setup(
    name=package,
    version=meta.__version__,
    packages=find_packages(),

    python_requires='~=3.6',
    install_requires=['discord.py>=0.15.0'],

    entry_points={
        'console_scripts': [f'{package} = {package}:main'],
    },

    author=meta.__author__,
    author_email=meta.__email__,
    description='The "Solitude Of War" Discord bot',
    license=meta.__license__,
    url='https://github.com/Mannheimd/Quartermaster',
)
