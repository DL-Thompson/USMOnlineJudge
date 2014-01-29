
from setuptools import setup

setup(
	name='USM Online Judge',
	version='1.0',
	long_description=__doc__,
	packages=['judge'],
	include_package_data=True,
	zip_safe=False,
	install_requires=['Flask']
)
