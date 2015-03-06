

from pprint import pprint

import gizflo as gz
from gizflo.boards import get_board
from blink import m_blink


def run_pone():
    brd = get_board('pone')
    brd.add_port_name('toggle', 'wingC', 7, drive=6)
    flo = gz.flo.ISE(brd=brd, top=m_blink)
    flo.run()
    info = flo.get_utilization()
    pprint(info)

if __name__ == '__main__':
    run_pone()