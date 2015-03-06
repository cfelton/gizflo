#
# Copyright (c) 2015 Christopher Felton
# Copyright (c) 2013 Alexander Hungenberg
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

from ..._fpga import _fpga
from ...extintf._extintf import _extintf
from ...extintf._port import Port
from ...extintf._sdram import SDRAM
from ...toolchain import ISE

VCCO = 'LVCMOS33'

class Pone(_fpga):
    vendor = 'xilinx'
    family = 'spartan3e'
    device = 'XC3S500e'
    package = 'VQ100'
    speed = '-4'
    _name = 'pone'

    default_clocks = {
        'clock': dict(frequency=32e6, pins=(89,), iostandard='LVCMOS25')
        }

    default_ports = {
        'wingA': dict(pins=(18, 23, 26, 33, 35, 40, 53, 57, 60, 62,
                            65, 67, 70, 79, 84, 86,), iostandard=VCCO),
        'wingB': dict(pins=(85, 83, 78, 71, 68, 66, 63, 61, 58, 54,
                            41, 36, 34, 32, 25, 22),
                      iostandard=VCCO),
        'wingC': dict(pins=(91, 92, 94, 95, 98, 2, 3, 4, 5, 9,
                            10, 11, 12, 15, 16, 17),
                      iostandard=VCCO),
        
        'jtag_tms': dict(pins=(75, ),  iostandard='LVTTL', drive='8', slew='fast'),
        'jtag_tck': dict(pins=(77, ),  iostandard='LVTTL', drive='8', slew='fast'),
        'jtag_tdi': dict(pins=(100,),  iostandard='LVTTL', drive='8', slew='fast'),
        'jtag_tdo': dict(pins=(76, ),  iostandard='LVTTL', drive='8', slew='fast'),
        'flash_cs': dict(pins=(24, ),  iostandard='LVTTL', drive='8', slew='fast'),
        'flash_ck': dict(pins=(50, ),  iostandard='LVTTL', drive='8', slew='fast'),
        'flash_si': dict(pins=(27, ),  iostandard='LVTTL', drive='8', slew='fast'),
        'flash_so': dict(pins=(44, ),  iostandard='LVTTL', drive='8', slew='fast', pullup=True),        
    }


    def get_flow(self, top=None):
        return ISE(brd=self, top=top)
