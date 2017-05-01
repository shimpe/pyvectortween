from distutils.core import setup
import sys

if sys.version_info[0] < 3:
    sys.exit("Sorry. Python 2 is currently not supported.")

setup(
    name='vectortween',
    version='0.0.1',
    packages=['vectortween'],
    url='',
    license='MIT',
    author='stefaan himpe',
    author_email='stefaan.himpe@gmail.com',
    description='vector animation library with tweening',
    requires=['pytweening', 'sympy', 'numpy', 'scipy']
)
