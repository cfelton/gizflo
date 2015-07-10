
from setuptools import setup, find_packages
from gizflo import __version__

# The README is probably a little too long for the
# pipy stuff.

desc =  \
"""
Automated FPGA toolflow for MyHDL modules.
"""

setup(name='gizflo',
      version=__version__,
      author="Christopher Felton",
      author_email="chris.felton@gmail.com",
      license="LGPL",
      description="automated #fpga toolflow for #myhdl modules",
      keywords="myhdl FPGA tools",
      url="http://github.com/cfelton/gizflo",
      packages=find_packages(),
      long_description=desc,
      )
