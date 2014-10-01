
from myhdl import *

def m_blink(clock, reset, toggle):
    MAX_CNT = int(clock.frequency)
    cnt = Signal(intbv(0,min=0,max=MAX_CNT))
    @always_seq(clock.posedge, reset=reset)
    def hdl():
        if cnt == MAX_CNT-1:
            cnt.next = 0
            toggle.next = not toggle
        else:
            cnt.next = cnt + 1

    return hdl
