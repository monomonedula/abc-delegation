from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="abc_delegation",
    version="0.1",
    description="Tool for automated implementation of delegation pattern with ABC",
    long_description=readme(),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="decorator delegation ABC",
    url="http://github.com/monomonedula/abc-delegation",
    author="Vladyslav Halchenko",
    author_email="valh@tuta.io",
    license="MIT",
    packages=["abc_delegation"],
    install_requires=["markdown"],
    test_suite="nose.collector",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    long_description_content_type='text/markdown',
)
