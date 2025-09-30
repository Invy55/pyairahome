from .airahome import AiraHome

# Version is automatically set by setuptools-scm from git tags
try:
    from ._version import version as __version__
except ImportError:
    # Fallback for development installs without _version.py
    from importlib.metadata import version
    __version__ = version("pyairahome")

__all__ = ['AiraHome']