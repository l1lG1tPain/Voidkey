from setuptools import setup, find_packages

setup(
    name="voidkey",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "voidkey=voidkey:main",
        ],
    },
    description="Ultimate security tool for Linux",
    author="Your Name",
    license="MIT"
)
