
from __future__ import print_function

from pprint import pprint

import gizflo as gz
from gizflo.boards import get_board
from blink import m_blink

def run_nano():
    brd = get_board('de0nano_soc')
    brd.add_port('toggle', pins=("W15",))
    flo = gz.flo.Quartus(brd=brd, top=m_blink)
    flo.run(use='vhdl')
    info = flo.get_utilization()
    pprint(info)

if __name__ == '__main__':
    run_nano()