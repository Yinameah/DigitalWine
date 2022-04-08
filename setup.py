from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in digitalwine/__init__.py
from digitalwine import __version__ as version

setup(
	name="digitalwine",
	version=version,
	description="A frappe app for wine maker.",
	author="Aurélien Cibrario",
	author_email="aurelien.cibrario@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
