
class _extintf(object):
    """ base class for external interface definitions.

    An external interface is like a mini-board definition, it is
    a collection of port definitions and associated attributes. 
    The external intefaces are configured with higher-level 
    definitions that are applicate to the interface.

    An external interface needs the ports and pins.
    """
    default_ports = {}
    default_clocks = {}
    default_resets = {}

    def __init__(self, *ports, **params):
        """ 
        An external interface will 
        """
        pass
    

    