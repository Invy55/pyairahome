from .airahome import AiraHome

# Version is automatically set by setuptools-scm from git tags
try:
    from ._version import version as __version__
except ImportError:
    # Fallback for development installs without _version.py
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("pyairahome")
    except PackageNotFoundError:
        __version__ = "0.0.0+unknown"

__all__ = ['AiraHome']