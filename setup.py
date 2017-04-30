from distutils.core import setup

setup(
    name='vectortween',
    version='0.0.1',
    packages=['vectortween'],
    url='',
    license='MIT',
    author='stefaan himpe',
    author_email='stefaan.himpe@gmail.com',
    description='some tweening for use with libraries like gizeh and moviepy',
    requires=['pytweening', 'sympy', 'numpy', 'scipy']
)
