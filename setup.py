from setuptools import setup
from setuptools import find_packages, findall


PACKAGE = "tmweixin"
NAME = "tmweixin"
DESCRIPTION = "A sdk to develop weixin-based app with django"
AUTHOR = "zhongkunchen"
AUTHOR_EMAIL = "[zhongkunchen@126.com]"
URL = ""
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("docs/README.md").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=["tmweixin"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False, requires=['django', 'requests']
)
