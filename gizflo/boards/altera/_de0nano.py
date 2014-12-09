#
# Copyright (c) 2013-2014 Jos Huisken, Christopher L. Felton
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
from ...toolchain import Quartus

class DE0Nano(_fpga):
    vendor = 'altera'
    family = 'Cyclone IV E'
    device = 'EP4CE22F17C6'
    speed = '6'
    _name = 'de0nano'

    default_clocks = {
        'clock': dict(frequency=50e6, pins=('R8',))
    }

    default_resets = {
        'reset': dict(active=0, async=True, pins=('J15',))
    }
    
    default_ports = {
        'led': dict(pins=('L3', 'B1', 'F3', 'D1',
                          'A11', 'B13', 'A13', 'A15',))
    }

    def get_flow(self):
        return Quartus(brd=self)