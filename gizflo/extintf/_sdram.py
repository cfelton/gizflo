
from ._clock import Clock
from ._extintf import _extintf

class SDRAM(_extintf):
    """
    Define the interface to SDRAMs.  This includes single and 
    double data rate SDRAMs.
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

    default_ports = {
        'data': None,  # D0-D15, data inputs
        'addr': None,  # A0-A12, address inputs

        'dqs':  None,  # data strobe
        'udqs': None,  # data strobe, upper byte
        'ldqs': None,  # data strobe, lower byte

        'dqm':  None,  # data mask
        'udqm': None,  # upper data mask
        'ldqm': None,  # lower data mask

        'bs':   None,  # bank select  (bs == ba)
        'ba':   None,  # bank address

        'ras':  None,  # row refresh, normally active-low
        'cas':  None,  # column refresh, normally active-low
        'we':   None,  # write-enable, normally active-low
        'cs':   None,  # chip-select, normally active-low
        'cke':  None,  # clock enable, normally active-high
        'clk':  None,
        'clkp': None,  # ddr positive clock
        'clkn': None,  # ddr negative clock
    }

    def __init__(self, *ports, **params):

        # is this DDR SDRAM or SDR SDRAM (ddr=0)
        if 'ddr' in params:
            self.ddr = params['ddr']
        else:
            self.ddr = 0

        # walk through the ports and update
        self._ports = dict(self.default_ports)
        for pp in ports:
            self._ports[pp.name] = pp

        # misc parameters
        self._params = dict(params)

        # update any of the timing information
        self._timing = dict(self.default_timing)
        for k,v in params.items():
            if k in self._timing:
                self._timing[k] = v
