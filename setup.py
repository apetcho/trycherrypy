from setuptools import find_packages, setup

setup(
    name="trycherrypy",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "cherrypy",
    ],
    include_package_data=True,
)
