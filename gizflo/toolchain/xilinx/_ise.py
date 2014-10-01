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

import sys
import os
from time import gmtime, strftime
import subprocess
from pprint import pprint

from .._toolflow import _toolflow
from ..._fpga import _fpga
from ...extintf import Clock

_default_pin_attr = {
    'NET': None,
    'LOC': None,
    'IOSTANDARD': None,
    'SLEW': None,
    'DRIVE': None
}

class ISE(_toolflow):
    """
    """

    def __init__(self, top, brd, path='./xilinx/'):
        """
        Give a top-level module (function) and a board definition
        create an instance of the ISE tool-chain.
        """
        _toolflow.__init__(self, top, brd, path)
        #self.reports = _ise_parse_reports(self)
        brd.set_top(top)    
    

    def add_files(self, fn):
        if isinstance(fn, str):
            fn = {fn}
        if isinstance(fn, (list, tuple, set)):
            if not all(isinstance(ff, str) for ff in fn):
                raise ValueError("Individual filenames must be strings")
        else:
            raise ValueError("Argument must be a string or a list/tuple/set of strings")
            
        self._hdl_file_list.update(set(fn))

        
    def create_constraints(self, filename=None):
        self.ucf_file = os.path.join(self._path, filename+'.ucf')
        ustr = ""
        ustr += "#\n"
        for port_name, port in self.ports.items():
            if port.inuse:
                _pins = port.pins

                for ii, pn in enumerate(_pins):
                    if len(_pins) == 1:
                        ustr += "NET \"%s\" " % port_name
                    else:
                        ustr += "NET \"%s<%d>\" " % (port_name, ii)

                    # pure numeric pins need a preceeding "p" otherwise
                    # use the string defined
                    if isinstance(pn, str):
                        ustr += "LOC = \"%s\" " % (str(pn))
                    else:
                        ustr += "LOC = \"p%s\" " % (str(pn))

                    # additional pin parameters
                    for kp, vp in port.kwargs.items():
                        if kp.lower() in ("pullup",) and vp is True:
                            ustr += " | %s " % kp
                        else:
                            ustr += " | %s = %s " % (kp, vp)
                    ustr += ";\n"

        ustr += "#\n"

        # @todo: loop through the pins again looking for clocks
        for port_name, port in self.ports.items():
            if port.inuse and isinstance(port.sig, Clock):
                period = 1 / (port.sig.frequency / 1e9)
                ustr += "NET \"%s\" TNM_NET = \"%s\"; \n" % (port_name, port_name)
                ustr += "TIMESPEC \"TS_%s\" = PERIOD \"%s\" %.7f ns HIGH 50%%;" \
                        % (port_name, port_name, period)
                ustr += "\n"
        ustr += "#\n"

        fid = open(self.ucf_file, 'w')
        fid.write(ustr)
        fid.close()
        # @todo: log setup information
        #print(ustr)

        
    def create_flow_script(self, filename=None):
        """ Create the ISE control script
        """
        # start with the text string for the TCL script
        self.tcl_script = '#\n#\n# ISE implementation script\n'
        date_time = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        self.tcl_script += '# create: %s\n' % \
                           date_time
        self.tcl_script += '# by: %s\n' % \
                           os.path.basename(sys.argv[0])
        self.tcl_script += '#\n#\n'
        
        if filename:
            fn = os.path.join(self._path, filename)
        else:
            fn = os.path.join(self._path, self.tcl_name)
            
        self.tcl_script += '# set compile directory:\n'
        self.tcl_script += 'set compile_directory %s\n' % '.'

        if self.top_name:
            self.tcl_script += 'set top_name %s\n' % self.top_name
            self.tcl_script += 'set top %s\n' % self.top_name

        self.tcl_script += '# set Project:\n'
        self.tcl_script += 'set proj %s\n' % self.top_name

        # @note: because the directory is changed everything
        #        is relative to self._path
        self.tcl_script += '# change to the directory:\n'
        self.tcl_script += 'cd %s\n' % self._path

        # @todo: verify UCF file exists
        bdir, ucffn = os.path.split(self.fpga.ucf_file)
        self.tcl_script += '# set ucf file:\n'
        self.tcl_script += 'set constraints_file %s\n' % ucffn

        self.tcl_script += '# set variables:\n'
        pj_fn = self.top_name + '.xise'
        # Create or open an ISE project (xise?)
        print('Project name : %s ' % pj_fn)
        pjfull = os.path.join(self._path, pj_fn)

        # let the TCL file be the master file, always create
        # a new project.  If a user uses this to "bootstrap"
        # the need to take care to rename the project if modfied
        # else it will be overwritten.
        if os.path.isfile(pjfull):
            os.remove(pjfull)
            #    self.tcl_script += 'project open %s \n' % (pj_fn)
        #else:
        self.tcl_script += 'project new %s\n' % pj_fn

        if self.fpga.family:
            self.tcl_script += 'project set family %s\n' % self.fpga.family
            self.tcl_script += 'project set device %s\n' % self.fpga.device
            self.tcl_script += 'project set package %s\n' % self.fpga.package
            self.tcl_script += 'project set speed %s\n' % self.fpga.speed

        # add the hdl files
        self.tcl_script += '\n'
        self.tcl_script += '# add hdl files:\n'
        self.tcl_script += 'xfile add %s\n' % ucffn
        for hdl_file in self._hdl_file_list:
            self.tcl_script += 'xfile add %s\n' % hdl_file
       
        self.tcl_script += '# test if set_source_directory is set:\n'
        self.tcl_script += 'if { ! [catch {set source_directory'
        self.tcl_script += ' $source_directory}]} {\n'
        self.tcl_script += '  project set "Macro Search Path"\n'
        self.tcl_script += ' $source_directory -process Translate\n'
        self.tcl_script += '}\n'

        # @todo : need an elgent way to manage all the insane options, 90% 
        #         of the time the defaults are ok, need a config file or 
        #         something to overwrite.  These should be in a dict or
        #         refactored or something
        #self.tcl_script += "project set \"FPGA Start-Up Clock\" \"JTAG Clock\"" \
        #                   " -process \"Generate Programming File\" \n"
        self.tcl_script += "project set \"FPGA Start-Up Clock\" \"JTAG Clock\" -process \"Generate Programming File\" \n"

        # run the implementation
        self.tcl_script += '# run the implementation:\n'
        self.tcl_script += 'process run "Synthesize" \n'
        self.tcl_script += 'process run "Translate" \n'
        self.tcl_script += 'process run "Map" \n'
        self.tcl_script += 'process run "Place & Route" \n'
        self.tcl_script += 'process run "Generate Programming File" \n'
        # close the project
        self.tcl_script += '# close the project:\n'
        self.tcl_script += 'project close\n'

        fid = open(fn, 'w')
        fid.write(self.tcl_script)
        fid.close()
            

    def run(self, use='verilog', filename=None):
        """ Execute the tool-flow """

        # determine if this is being used to kick of an existing 
        # flow script or if the files need to be generated.
        if filename:
            tcl_name = filename
        else:
            tcl_name = os.path.join(self._path, self.tcl_name)

        if not os.path.exists(self._path):
            os.mkdir(self._path)

        # convert the top-level
        cfiles = convert(self.brd, to=use)
        self.add_files(cfiles)
        self.create_constraints(filename=self.brd.top_name)
        self.create_flow_script(filename=tcl_name)

        cmd = ['xtclsh', tcl_name]
        try:
            self.logfn = 'build_ise.log'
            logfile = open(self.logfn, 'w')
            subprocess.check_call(cmd,  #shell=True,
                                  stderr=subprocess.STDOUT,
                                  stdout=logfile)
            logfile.close()
        except Exception, err:
            print(err)
            raise err

