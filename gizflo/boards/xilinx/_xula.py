#
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

from ..._fpga import _fpga

class Xula(_fpga):
    vendor = 'xilinx'
    family = 'spartan3A'
    device = 'XC3S200A'
    package = 'VQ100'
    speed = '-4'
    _name = 'xula'

    default_clocks = {
        'clock': dict(freqeuncy=12e6, pins=(43,)),
        'chan_clk' : dict(frequency=1e6, pins=(44,))
    }

    default_ports = {
        'chan' : dict(pins=(36,37,39,50,52,56,57,61,  # 0-7
                            62,68,72,73,82,83,84,35,  # 8-15
                            34,33,32,21,20,19,13,12,  # 17-23
                            07,04,03,97,94,93,89,88)) # 24-31
    }


class Xula2(_fpga):
      vendor = 'xilinx'
      family = 'spartan6'
      device = 'XC6SLX25'
      package = 'FTG256'
      speed = '-2'
      _name = 'xula2'

      default_clocks = {
          'clock': dict(frequency=12e6, pins=('A9',)),
          'chan_clk': dict(frequency=1e6, pins=('T7'))
      }

      default_ports = {
          'chan': dict(pins=('R7','R15','R16','M15','M16','K15',  #0-5
                             'K16','J16','J14','F15','F16','C16', #6-11
                             'C15','B16','B15','T4','R2','R1',    #12-17
                             'M2','M1','K3','J4','H1','H2',       #18-23
                             'F1','F2','E1','E2','C1','B1',       #24-29
                             'B2','A2',) )
      }
