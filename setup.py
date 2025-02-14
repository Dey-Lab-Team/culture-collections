from setuptools import setup

setup(
    name="culture-collections",
    version="0.0.1",
    description="Python files to create a MoBIE project for culture collections",
    author="Jonas Hellgoth",
    author_email="jonas.hellgoth@embl.de",
    packages=["culture_collections"],  # same as name
    install_requires=["numpy", "elf", "mobie"],  # external packages as dependencies
)
