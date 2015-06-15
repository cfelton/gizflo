
__version__ = "0.0.2"
__version_info__ = tuple([int(num) for num in __version__.split('.')])

from .boards import get_board
from . import toolchain as flo
