from .settings import SETTINGS
import time
from functools import wraps
from contextlib import contextmanager

_warned = set()

def warn_once(msg):
    """Print a warning only once."""
    if msg not in _warned:
        _warned.add(msg)
        print(f"[WARNING] {msg}")



def debug_print(msg, level="info"):
    if not SETTINGS.system.verbose:
        return
    
    levels = ["info", "debug", "trace"]
    
    if levels.index(level) <= levels.index(SETTINGS.system.debug_level):
        print(f"[{level.upper()}] {msg}")

def dump_object(obj):
    """Print internal fields of an object for debugging."""
    if SETTINGS.system.verbose:
        print("[OBJECT DUMP]")
        for key, val in vars(obj).items():
            print(f"  {key}: {val}")

def timed(func):
    """
    Decorator that measures execution time of a function, but only
    prints the timing result when SETTINGS.system.verbose is True.

    Example:
        @timed
        def compute():
            ...
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # If debugging is off → run normally
        if not SETTINGS.system.verbose:
            return func(*args, **kwargs)

        # Debugging on → measure time
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()

        print(f"[TIMED] {func.__name__}: {end - start:.6f} s")
        return result

    return wrapper