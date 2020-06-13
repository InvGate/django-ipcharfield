from setuptools import setup, find_packages
import sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import ipcharfield

setup(
    name="django-ipcharfield",
    version=ipcharfield.__version__,
    url="https://github.com/InvGate/django-ipcharfield/",
    author="Leutwyler Nicolas",
    author_email="ramshellcinox@gmail.com",
    license="MIT",
    description="IPs with str storage for django models allowing stringlike operations such as icontains",
    long_description=open('README.md').read(),
    keywords="ip, models, django",
    packages=["ipcharfield"],
    setup_requires=["setuptools"],
    install_requires=("setuptools", "netaddr", "django",),
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",),
)
