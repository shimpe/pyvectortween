from distutils.core import setup
from setuptools import find_packages

setup(
    name='vectortween',
    version='0.0.4',
    packages=find_packages(exclude=['build', 'dist', 'docs', 'tests']),
    python_requires='>=3',
    url='https://github.com/shimpe/pyvectortween',
    keywords=["tween", "animation"],
    license='MIT',
    author='stefaan himpe',
    author_email='stefaan.himpe@gmail.com',
    description='animation library with tweening',
    long_description='animation library with tweening',
    install_requires=['pytweening', 'sympy', 'numpy', 'scipy'],
    classifiers=["Development Status :: 4 - Beta",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 3 :: Only",
                "Topic :: Artistic Software",
                "Topic :: Software Development :: Libraries",
                "Topic :: Software Development :: Libraries :: Python Modules"]
)
