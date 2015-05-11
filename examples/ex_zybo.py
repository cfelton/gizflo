
from pprint import pprint

import gizflo as gz
from gizflo.boards import get_board
from blink import m_blink

def run_zybo():
    # get a board to implement the design on
    brd = get_board('zybo')
    brd.add_port('toggle', pins=('R7',))
    brd.add_reset('reset', active=0, async=True, pins=('R15',))
    flow = gz.flo.Vivado(brd=brd, top=m_blink)
    flow.run()
    info = flo.get_utilization()
    pprint(info)

if __name__ == '__main__':
    run_zybo()