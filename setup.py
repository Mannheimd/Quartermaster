from setuptools import find_packages, setup

setup(
    name='quartermaster',
    version='0.3.0-dev',
    packages=find_packages(),

    python_requires='~=3.6',
    install_requires=['discord.py>=0.15.0'],

    entry_points={
        'console_scripts': ['quartermaster = quartermaster:main'],
    },

    author='Christopher Manders, Matthew Parnell',
    author_email='cmanders159@gmail.com, matt@parnmatt.co.uk',
    description='The "Solitude Of War" Discord bot',
    license='MIT',
    url='https://github.com/Mannheimd/Quartermaster',
)
