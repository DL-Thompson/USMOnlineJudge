
from setuptools import setup

setup(
	name='USMOnlineJudge',
	version='1.0',
	packages=['judge'],
	include_package_data=True,
	zip_safe=False,
	install_requires=['Flask']
)
