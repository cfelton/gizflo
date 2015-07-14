
from pprint import pprint

import gizflo as gz
from gizflo.boards import get_board
from blink import m_blink

def run_nano():
    brd = get_board('de0nano')
    brd.add_port('toggle', pins=("A15",))
    flo = gz.flo.Quartus(brd=brd, top=m_blink)
    flo.run()
    info = flo.get_utilization()
    pprint(info)

if __name__ == '__main__':
    run_nano()