# Copyright (c) 2014 Christopher Felton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
from __future__ import print_function

class _toolflow(object): 

    def __init__(self, top, brd, path=None):
        """
        Provided a myhdl top-level module and 
        """

        self._path = path if path is not None else '.'
        self._fpga = brd
        self._top_name = top.func_name
        self.tcl_name = self.top_name + '.tcl'
        self._hdl_file_list = set()
        self.logfn = None

        
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, p):
        self._path = p

    @property
    def fpga(self):
        return self._fpga

    @fpga.setter
    def fpga(self, brd):
        self._fpga = fpga


    def pathexist(self, pth):
        if os.path.isfile(pth):
            pth,fn = os.path.split(pth)
        fpth = ''
        path_split = os.path.split(pth)
        for ppth in pth.split(os.path.sep):
            fpth = os.path.join(fpth,ppth)
            if not os.path.isdir(fpth):
                print("path create %s" % (fpth,))
                os.mkdir(fpth)

        return os.path.isdir(pth)
        

    def create_project(self, filename=None):
        """ Create a project file if needed
        """
        pass

    def create_flow_script(self, filename=None):
        """ Create the tool-flow script  if needed.
        """
        pass

    def create_constraints(self, filename=None):
        """ Create the constraints
        """
        pass

    def add_files(self, fn):
        """ Add additional files to the tool-flow
        """
        pass


    def run(self, use='verilog', filename=None):
        """ Execute the tool-flow
        """
        pass