"""Service layer package initialization.

Only re-exports the ``bot`` and ``dp`` objects from :mod:`mybot`.  The
instances themselves are created in ``mybot.__init__`` to avoid
duplication.
"""

from mybot import bot, dp

__all__ = ["bot", "dp"]
