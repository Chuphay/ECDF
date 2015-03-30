try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'name' : 'ECDF',
    'description' : 'Empirical Cumulative Distribution Function',
    'url' : 'https://github.com/Chuphay/ECDF',
    'author' : 'David Plotz',
    'author_email' : 'chuphay@gmail.com',
    'version' : '0.1',
    'packages' : ['ecdf','tests'],
    'long_description' : open('README.md').read(),
}

setup(**config)
