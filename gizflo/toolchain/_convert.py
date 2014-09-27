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


import myhdl
from myhdl import toVerilog
from myhdl import toVHDL


def convert(top, brd, use='verilog'):
    """ Wrapper around the myhdl conversion functions
    """
    name = brd.top_name
    pp = brd.
    # convert with the ports and parameters        
    if use.lower() == 'verilog':
        if name is not None:
            myhdl.toVerilog.name = name
        myhdl.toVerilog(self.top, **pp)
        self.name = name
        self.vfn = "%s.v"%(name)
    elif to.lower() == 'vhdl':
        if name is not None:
            myhdl.toVHDL.name = name
        myhdl.toVHDL(self.top, **pp)
        self.name = name
        self.vfn = "%s.vhd"%(name)
    else:
        raise ValueError("Incorrect conversion target %s"%(to))

    # make sure the working directory exists
    assert self.pathexist(self._path)

    # copy files etc to the working directory
    tbfn = 'tb_'+self.vfn
    ver = myhdl.__version__
    # remove special characters from the version
    for sp in ('.', '-', 'dev'):
        ver = ver.replace(sp,'')
    pckfn = 'pck_myhdl_%s.vhd'%(ver)
    for src in (self.vfn,tbfn,pckfn):
        dst = os.path.join(self._path,src)
        print('   checking %s'%(dst))
        if os.path.isfile(dst):
            print('   removing %s'%(dst))
            os.remove(dst)
        if os.path.isfile(src):
            print('   moving %s --> %s'%(src,self._path))
            shutil.move(src,self._path)

    if to.lower() == 'verilog':
        filelist = (self.vfn,)
    elif to.lower() == 'vhdl':
        filelist = (self.vfn, pckfn,)

    return filelist

    