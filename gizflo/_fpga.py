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
import shutil
import inspect
from random import randint
from copy import copy

import myhdl

from extintf import _port
from extintf import Clock
from extintf import Reset


class _fpga(object):
    """ """
    vendor = "" # FPGA vendor, Altera, Xilinx, Lattice
    device = "" # FPGA device type
    family = "" # FPGA family

    # relate ports to the hardware
    default_clocks = {}
    default_resets = {}
    default_ports = {}
    default_extintf = {}

    def __init__(self):
        
        # default attributes
        self.top = None        # top-level myhdl module
        self.top_name = None   # resulting name, project name etc.
        self.top_params = None # top-level parameters

        self._clocks = {}
        self._resets = {}
        self._ports = {}
        self._extintfs = {}

        # walk through the default settings
        for k,v in default_clocks.iteritems():
            self.add_clock(k, v)
        for k,v in default_resets.iteritems():
            self.add_reset(k, v)
        for k,v in default_ports.iteritems():
            self.add_port(k, v)
        for k,v in default_extintf.iteritems():
            self.add_extintf(k, v)


    def has_top(self):
        """ a top-level is set """
        return self.top is not None


    def set_top(self, top, **params):
        self.top = top
        self.top_params = params


    def _remove_embed_attr(self, pins, pattr):
        """ removed an embedded pin attribute def if present.
        """
        for v in pins:
            if isinstance(v, dict):
                pattr = v
                pins.remove(v)
                break
        return pattr


    def add_clock(self, name, frequency=1, pins=None, **pattr):
        assert isinstance(pin, (str,int))
        self.clocks[name] = _port(name, pins, frequency=frequency, **pattr)

        
    def add_reset(self, name, active, async, pins, **pattr):
        assert isinstance(active, bool)
        assert active in (0,1,)
        self._resets[name] = _port(name, pints, 
                                   active=active, 
                                   async=async, **pattr)


    def add_port(self, name, pins, **pattr):
        """ add a port definition
        
        A port definition maps a port (an HDL top-level signal name)
        to a pin on the physical device including any attributes of 
        the pin / signal.

        Example: 
          brd.add_port("gpio", pins=(23,24,25,26,), PULLUP='PULLUP')

        It is acceptable to have ports with the same names.
        """
        if isinstances(pints, (str, int)):
            pins = [pins,]
        assert isinstance(pins, (list,tuple)), \
            "pins must be a list/tuple of pins (or a single str/int)"
        pins = list(pins)
        pattr = self._remove_embed_attr(pins, pattr)
        # make sure the pin list is a number or string
        for v in pins:
            assert isinstance(v, (str, int))
        # @todo: raise an error vs. 
        assert not self._ports.has_key(name)
        self._ports[name] = _port(name, pins, **pattr)


    def add_port_name(self, name, port, slc=None, **pattr):
        """ add a new name, *name*, to an existing port, *port*.
        This function is used when the default port name is known
        but not the pins (if the pins are known use add_port).
        A port name is linked to a default port name or a subset
        (slice) is linked to the new name.  

        Example: brd.link_port_name('wingC', 'led', 7)
        where wingC is a 16-bit port bit-vector

        To extract a range from the port, the slice class has to
        be used, example:
        brd.link_port_name('wingC', 'MSB', slice(16,8))
        """
        
        p = self._ports[port]
        if slc is None:
            pins = p.pins
        else:
            assert isinstance(slc, (slice, int)), \
                "slice (slc) needs to be None or int/slice"
            pins = p.pins[slc]
        kws = p.pattr.copy()
        kws.update(pattr)
        self.add_port(name, pins, **kws)

        
    def rename_port(self, port, name, slc=None, **pattr):
        """ rename a *port* to a new *name*
        This function is useful for *bootstrapping*, bootstrapping
        uses the port names that exist in the object and doesn't
        have a method to select from multiple definitions.  Also,
        useful when the top-level HDL has conflicts.
        """
        pass

        
    def add_extintf(self, name, extintf):
        """
        """
        self._extintfs[name] = extintf


    def _get_name(self, name=None):
        """ determine which name should be used """
        if name is None:
            if self.top_name is not None:
                name = self.top_name
            else:
                name = self.top.func_name
        return name


    def get_portmap(self, name=None, top=None, **kwargs):
        """ given a top-level map the port definitions 
        This module will map the top-level MyHDL module ports
        to a board definition.

        Typical usage:
            brd = gizflo.get_board(<board name>)
            portmap = brd.get_portmatp(top=m_myhdl_module)
            myhdl.toVerilog(m_myhdl_module, **portmap)
        """
        if top is not None:
            self.top = top
        name = self._get_name(name)

        # get teh top-level ports and parameters
        pp = inspect.getargspec(self.top)

        # all of the arguments (no default values) are treated as
        # ports.  This doesn't mean it needs to be a port but it
        # is convention that ports are the arguments and parameters
        # are keyword arguments.  A parameter can exist in this 
        # list but it can't be empty ...
        hdlports = {}
        if pp.defaults is not None:
            pl = len(pp.args)-len(pp.defaults)
        else:
            pl = len(pp.args)
        for pn in pp.args[:pl]:
            hdlports[pn] = None
        params = {}
        for ii,kw in enumerate(pp.args[pl:]):
            params[kw] = pp.defaults[ii]

        # see if any o fth eports or parameters have been overridden
        if self.top_params is not None:
            for k,v in self.top_params.iteritems():
                if hdlports.has_key(k):
                    hdlports[k] = v
            for k,v in self.top_params.iteritems():
                if params.has_key(k):
                    params[k] = v

        for k,v in kwargs.items():
            if hdlports.has_key(k):
                hdlports[k] = v
        for k,v in kwargs.items():
            if params.has_key(k):
                params[k] = v

        # @todo: log this information, some parameters can be too large
        #    to be useful dumpin to scree (print).
        # log.write("HDL PORTS   %s" % (hdlports,))
        # log.write("HDL PARAMS  %s" % (params,))

        # match the fpga ports to the hdl ports, not if a port is
        # a keyword argument in the top-level this will fail
        # @todo: this matching code needs to be enhanced, this should
        #    always match a top-level port to a port def.
        for port_name,port in self.ports.items():
            if hdlports.has_key(port_name):
                hdlports[port_name] = port.sig
                port.inuse = True

        for k,v in hdlports.items():
            assert v is not None, "Error unspecified port %s"%(k)
        
        # combine the ports and params
        pp = hdlports.copy()
        pp.update(params)

        return pp