"""Having this structure with the project name allows us to control the imports,
    and limit the access to the internal modules.
"""

from .hstrader import HsTrader, __version__
from ..config import Config, Strategy
