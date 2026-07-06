from ._constant_attrib import ConstantAttrib
from ._env_mod import ENVMod
from ._logwrap import logwrap
from ._method_monitor import MethodMonitor
from ._remote_attrib import RemoteAttrib
from ._super_with import SuperWith
from ._supress_errors import suppress_errors

__version__ = '1.2.2'
__description__ = "Simple mods for python classes."
__authors__ = [
    {"name": "devixa-dev", "email": "hmohammad2520@gmail.com"},
]
__keywords__ = [
    "python",
    "class",
    "mods",
    "modification",
    "descriptors",
    "methods",
    "methodmod",
    "methodobserve",
]

__all__ = [
    'ConstantAttrib',
    'ENVMod',
    'logwrap',
    'MethodMonitor',
    'RemoteAttrib',
    'SuperWith',
    'suppress_errors',
]