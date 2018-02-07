"""
Provides metadata for the package.

Needed to expose metadata in __init__.py for package setup, without
importing the whole structure.
"""

# explict __all__ as dunder variables are not usually included in a wild import
__all__ = ['__author__', '__email__', '__maintainer__', '__license__', '__version__']

__author__ = 'Christopher Manders, Matthew Parnell'
__email__ = 'cmanders159@gmail.com, matt@parnmatt.co.uk'
__maintainer__ = __author__
__license__ = 'MIT'
__version__ = '0.3.0-dev'
