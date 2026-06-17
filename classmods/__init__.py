from ._decorators import logwrap, suppress_errors
from ._descriptors import ConstantAttrib, RemoteAttrib
from ._env_mod import ENVMod
from ._method_monitor import MethodMonitor
from ._super_with import SuperWith

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
    'RemoteAttrib',
    'ENVMod',
    'MethodMonitor',
    'logwrap',
    'suppress_errors',
    'SuperWith',
]