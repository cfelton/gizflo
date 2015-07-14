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


import os
import time
import shutil

import myhdl
from myhdl import toVerilog
from myhdl import toVHDL

from .._fpga import _fpga

def convert(brd, top=None, name=None, use='verilog', path='.'):
    """ Wrapper around the myhdl conversion functions
    This function will use the _fpga objects get_portmap function
    to map the board definition to the 

    Arguments
      top  : top-level myhld module
      brd  : FPGA board definition (_fpga object)
      name : name to use for the generated (converted) file
      use  : User 'verilog' or 'vhdl' for conversion
      path : path of the output files
    """
    assert isinstance(brd, _fpga)

    name = brd.top_name if name is None else name
    pp = brd.get_portmap(top=top)

    # convert with the ports and parameters        
    if use.lower() == 'verilog':
        if name is not None:
            myhdl.toVerilog.name = name
        myhdl.toVerilog.no_testbench = True
        myhdl.toVerilog(brd.top, **pp)
        brd.name = name
        brd.vfn = "%s.v"%(name)
    elif use.lower() == 'vhdl':
        if name is not None:
            myhdl.toVHDL.name = name
        myhdl.toVHDL(brd.top, **pp)
        brd.name = name
        brd.vfn = "%s.vhd"%(name)
    else:
        raise ValueError("Incorrect conversion target %s"%(use))

    # make sure the working directory exists
    #assert brd.pathexist(brd.path)
    time.sleep(2)

    # copy files etc to the working directory
    tbfn = 'tb_' + brd.vfn
    ver = myhdl.__version__
    # remove special characters from the version
    for sp in ('.', '-', 'dev'):
        ver = ver.replace(sp,'')
    pckfn = 'pck_myhdl_%s.vhd'%(ver)
    for src in (brd.vfn,tbfn,pckfn):
        dst = os.path.join(path, src)
        print('   checking %s'%(dst))
        if os.path.isfile(dst):
            print('   removing %s'%(dst))
            os.remove(dst)
        if os.path.isfile(src):
            print('   moving %s --> %s'%(src, path))
            try:
                shutil.move(src, path)
            except Exception as err:
                print("skipping %s because %s" % (src, err,))

    if use.lower() == 'verilog':
        filelist = (brd.vfn,)
    elif use.lower() == 'vhdl':
        filelist = (brd.vfn, pckfn,)

    return filelist

    
