
from _clock import Clock
from _extintf import _extintf

class SDRAM(_extintf):
    """
    """
    
    # the timing atrribute captures all the time fields of the 
    # SDRAM controller.  These are used to setup the constraints
    # as well as being passed to the SDRAM controller HDL.
    # All timing fields are in nano-seconds.
    default_timing = { 
        'init': 200000.0,   # min init interval
        'ras':  45.0,       # min interval between active precharge commands
        'rcd':  20.0,       # min interval between active R/W commands
        'ref':  64000000.0, # max refresh interval
        'rfc':  65.0,       # refresh operation duration
        'rp':   20.0,       # min precharge command duration
        'xsr':  75.0,       # exit self-refresh time
    }

    