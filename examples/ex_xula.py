
import gizflo as gz
from gizflo.boards import get_board
from blink import m_blink

def run_xula():
    # get a board to implement the design on
    brd = get_board('xula2')
    brd.add_port('toggle', pins=('R7',))
    brd.add_reset('reset', active=0, async=True, pins=('R15',))
    flo = gz.flo.ISE(top=m_blink, brd=brd)
    flo.run()

if __name__ == '__main__':
    run_xula()